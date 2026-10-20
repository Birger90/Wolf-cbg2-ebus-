# Protokollnotizen Wolf CGB-2 / BM-2 am eBus

Alle Angaben stammen aus Mitschnitten des ebusd-Logs vom 19.10.2026 an der eigenen Anlage und aus den
genannten Quellen. Was nicht selbst beobachtet wurde, ist als solches markiert.

## Telegrammformate (Nutzdaten nach PBSB)

| Richtung | Beispiel (hex) | Bedeutung |
|---|---|---|
| ISM7 liest Therme | `ff 08 5022 03 82 882a` | Prüfbyte 82, TN 0x2a88 = 10888 |
| ISM7 liest 5 TNs | `ff 08 5022 0b 71 1600 4801 6f01 7201 7301` | Prüfbyte 71 über alle 10 Bytes, Antwort 10 Bytes |
| BM-2 liest Therme | `30 08 5022 03 cc 0d00` | festes Präfix `cc`, TN 13 (Vorlauf) |
| ebusd offiziell | `31 08 5022 03 00 0d00` | Präfix `00`, wird ebenfalls beantwortet |
| BM-2 schreibt Therme | `30 03 5023 05 4f f402 0003` | Prüfbyte 4f (CRC), TN 756, Wert 0x0300 |
| BM-2 Broadcast | `30 fe 5023 05 44 2300 0000` | TN 35 Freigabe Parallelbetrieb = 0 |
| ISM7 schreibt BM-2 | `ff 30 5023 09 b0 1300 f401 5d01 0000` | TN 19 WW-Soll = 500 = 50,0 °C, Anhang TN 349 = 0 |
| ebusd schreibt BM-2 (funktioniert) | `31 35 5023 05 b1 1300 f401` | TN 19 = 50,0 °C, 5 Byte an Slave 35 |

## Prüfbyte

```python
def shift8(c):
    for _ in range(8):
        c = ((c << 1) & 0xFF) ^ 0x5C if c & 0x80 else (c << 1) & 0xFF
    return c

def wolf_crc(data):          # data = alle Bytes nach dem Prüfbyte
    c = 0
    for b in data:
        c = shift8(c) ^ b
    return c
```

Beobachtete Werte vs. berechnet (Auszug, vollständig in `tools/wolf_crc.py`):

| Nutzdaten | beobachtet | berechnet |
|---|---|---|
| `1300 f401 5d010000` | b0 | b0 |
| `1300 8a02 5d010000` (65,0 °C, zweimal gesendet) | 6c | 6c |
| `1300 2201 5d010000` (29,0 °C) | 00 | 00 |
| `160048016f0172017301` (Blocklesen) | 71 | 71 |
| `f4020003` (BM-2 Write) | 4f | 4f |

Folgerung: Das Prüfbyte hängt nur vom Inhalt ab (gleicher Wert = gleiches Byte), nicht von Zeit oder Zähler.

## Schreibversuche, chronologisch

| Zeit | Telegramm | Absender | Ergebnis |
|---|---|---|---|
| 18:48 | 9 Byte an `30`, Wert 60,0 | 31 | kein ACK, Wert bleibt 50 |
| 18:49 | 9 Byte an `30`, bit-identisch zum ISM7 | 31 | kein ACK |
| 20:20, 20:23 | 9 Byte an `30` | ff (`--address=ff`, ISM7 parallel am Bus) | kein ACK |
| 21:05 | 9 Byte an `30`, Bus-Debug | 31 | BM-2 antwortet gar nicht (kein ACK, kein NAK), 3 Versuche |
| 21:17 | 9 Byte an `35` | 31 | kein ACK, Wert unverändert |
| 21:20 | **5 Byte an `35`, CRC b1** | 31 | `read timeout`, aber Wert 60 → **50** (Cloud 21:21 bestätigt) |
| 21:45 | 5 Byte an `35`, Wert 60, CRC 0a | 31 | erster Versuch nicht angekommen, zweiter Versuch 21:47 → **60** |
| 22:02 | 5 Byte an `35`, Prüfbyte absichtlich `00` | 31 | Wert → **50**, BM-2 prüft das Prüfbyte beim Schreiben nicht |
| 22:03 | 5 Byte an `35`, Prüfbyte `00`, Wert 60 | 31 | Wert → **60** |
| 22:3x | Therme: 9 Byte an `03` mit Anhang `9d010000` (offizielles ebusd-Format), HG07 = 2 | 31 | HG07 bleibt 1 |
| 22:4x | **Therme: 5 Byte an `03`, CRC `ac`** (`ac 4201 0200`) | 31 | ebusd `done` (ACK), HG07 → **2** |
| 20.10. 06:11 | Therme: 5 Byte an `03`, Prüfbyte `00` (`00 4201 0100`) | 31 | `read timeout`, HG07 bleibt 2 → **Therme prüft das Prüfbyte** |
| 06:18 | Therme: 5 Byte an `03`, CRC `48` (`48 4201 0100`) | 31 | HG07 → **1** |
| 20:42 | **Mischermodul: 5 Byte an Slave `52`, CRC `80`** (`80 4201 0600`) | 31 | ebusd `sent write` (ACK, kein Timeout), PumpOverrun 5 → **6**; 20:42:49 `… 0500` → **5** |
| 19.10. 23:05 | BM-2: Programmwahl DHK TN 10100 = 2 (`d4 7427 0200`) | 31 | HkProgram → Permanent, Heizkreis Heizbetrieb, Brenner an |
| 20.10. 06:00 | BM-2: TN 10100 = 1 (`30 7427 0100`) | 31 | HkProgram → Auto |

## Parametertest 20.10.2026 (script.heizung_parametertest)

Jeder schreibbare Parameter: lesen, Wert+1 schreiben, zurücklesen, Originalwert schreiben, zurücklesen.
Therme über `HgRaw` mit berechnetem Prüfbyte, BM-2/MK über die statischen Nachrichten (Präfix `00`).

| Gerät | Parameter | Ergebnis |
|---|---|---|
| Therme (03) | HG01, HG04, HG07, HG08, HG09, HG15, HG16, HG17, HG22, HG25, HG33, HG38, HG39, HG60 | alle 14: Schreiben OK, Rücksetzen OK (HG07/HG09 je ein Wiederholversuch) |
| BM-2 (35) | WwSoll, WwMin, HkDaytemp, HkCurveBasetemp, HkCurveStart, HkCurveNormoutside, HkCurveFlowtemp, HkSetpointcorr, HkWintersummer, HkEcoabs | alle 10: Schreiben OK, Rücksetzen OK |
| MK (86) | MkDaytemp, MkCurveBasetemp, MkCurveStart, MkCurveNormoutside, MkCurveFlowtemp, MkSetpointcorr, MkWintersummer, MkEcoabs | alle 8 OK; MkSetpointcorr brauchte im Testlauf einen zweiten Versuch (erstes Telegramm verloren, Wiederholung 06:39 angekommen) |

Nicht getestet (absichtlich): Programmwahl (nur der einmalige Notfall-Schreibvorgang oben), 1x Warmwasser (löst eine
Speicherladung aus), HG02/HG03/HG12 (Gas), HG21/HG62 (liefern `unknown`).

## Parametertest 20.10.2026, 20:43–20:56 (41 Parameter, nach WLAN-Wechsel des Adapters)

| Gerät | Ergebnis |
|---|---|
| Therme (03), 16 Parameter inkl. HG02/HG03 | 15 OK; HG08 übersprungen (kein Lesewert im 4-s-Fenster nach dem ebusd-Neustart) |
| Mischermodul (52), 5 Parameter | **alle 5 OK** (TvMin, TvMax, CurveDistance, PumpOverrun, MixerPband), Schreiben über `MmRaw` mit CRC, ACK vom Modul |
| BM-2 (35), 11 Parameter | 8 OK; WwSoll, HkDaytemp, HkCurveStart: erstes Telegramm nicht angekommen (Wert blieb), Rücksetzen OK |
| Mischerkreis (86), 10 Parameter | 6 OK; MkSparfaktor, MkSetpointcorr, MkWintersummer, MkEcoabs: erstes Telegramm nicht angekommen, Rücksetzen OK |

Deutung: Therme und MM quittieren (ACK) und das Skript wiederholt bis zum bestätigten Rücklesewert, deshalb 0 Verluste.
BM-2 und MK liefern kein ACK (`read timeout`), die statischen Schreibzeilen senden einmal ohne Wiederholung: 7 von 21
Telegrammen gingen verloren (am Morgen bei leerem Bus 1 von 18). Konsequenz: auch BM-2/MK nur mit Rücklesen und
Wiederholung schreiben (siehe Skripte).

## Uhr des BM-2: Lesen ja, Stellen nein (20.10.2026, 21:52–22:08)

Gelesen: TN 10161 `Time` = 5401 → 21:25 bei realer Zeit 21:19, TN 10160 `Date` = 13619 → 20.10.2026. Zusätzlich sendet das
BM-2 (Master `30`) jede Minute den Standard-Broadcast `fe 0700` (ebusd `Broadcast Datetime`), z. B. `-;22:13:10;20.10.2026`
um 22:06:58 → die BM-2-Uhr geht 6 min 12 s vor. Das ISM7 (`ff`) liest TN 10160 jede Minute, korrigiert die Uhr aber nicht.

Schreibversuche, alle ohne Wirkung (Rücklesen unverändert, BM-2-Broadcast unverändert):

| Zeit | Telegramm an `35` | Ergebnis |
|---|---|---|
| 21:53:00/07/14 | `00 b1 27 35 15` (TN 10161 = 21:53, Präfix 00, 3× über `script.heizung_ebus_schreiben`) | `read timeout`, Time bleibt 5435 |
| 21:56:00 | `11 b1 27 38 15` (CRC korrekt) | ignoriert |
| 22:07:05 | `71 b1 27 07 16 b0 27 33 35` (9 Byte: Time + Date mit CRC, Form des ISM7) | ignoriert |
| 22:07:28 | Broadcast `31 fe 0700` `10.6;22:08:00;20.10.2026` (ebusd `Broadcast/Datetime/set`) | BM-2 sendet 22:07:58 weiter 22:14:10 |

Wolf-Parameterdatenbank: „Uhrzeit"/„Datum" (PTID 220032/220033) sind `ReadOnly=True`; die schreibbar markierten
„Uhrzeit BM2"/„Datum BM2" (330004/330005, dieselben TNs) sind nur Anzeigefelder im Party-/Urlaubsdialog
(`sub_dialogs.xml`, `BM2PartyProgramTemplate`). Folgerung: Die Uhr des BM-2 lässt sich über den eBus nicht stellen,
nur am Gerät. In Home Assistant bleibt die Überwachung (`sensor.heizung_bm_2_uhrabweichung`, Hinweis ab 2 min).
Ob das ISM7/Wolf Link home die Uhr auf anderem Weg synchronisieren kann, konnte ich nicht verifizieren (keine Quelle).

Nebenbefund: Solange Party-/Urlaubsmodus deaktiviert sind, führt das BM-2 `PartyStart`/`HolidayStart` = aktuelle Uhrzeit
und `PartyEnd`/`HolidayEnd` = aktuelle Uhrzeit + 3 h nach (Datum entsprechend).

## Partymodus über den eBus (20.10.2026, 22:23–22:31)

| Zeit | Aktion | Beobachtung |
|---|---|---|
| 22:23:26 | `00 a6 27 01 00` an `35` (TN 10150 = 1) | PartyMode → Aktiviert (Rücklesen 3 s später); BM-2 setzt Start = jetzt, Ende = jetzt + 3 h; 22:25:44 `HkDemand` = **Partymodus**; Therme 22:27 kurz Heizbetrieb/Softstart |
| 22:26:21–35 | zweiter Skriptlauf: Mode = 1 (schon aktiv), dann `PartyEndDate` = 13619 (heute), dann `PartyEnd` = 22:56 | `HkDemand` → **Automatik_aus**, Partymodus intern beendet, Flag PartyMode blieb Aktiviert |
| 22:29:13 | TN 10150 = 0 | PartyMode → Deaktiviert |
| 22:30:0x | TN 10150 = 1 allein | 22:30:13 `HkDemand` = Partymodus |
| 22:30:2x | `PartyEnd` = 5894 (23:06) über die statische Schreibzeile | übernommen, `HkDemand` bleibt Partymodus |
| 22:30:5x | `PartyEndDate` = 13619 | übernommen, `HkDemand` bleibt Partymodus |
| 22:31:23 | TN 10150 = 0 über `script.heizung_partymodus` (beenden) | PartyMode Deaktiviert, `HkDemand` Automatik_aus |

Deutung: Beim Einschalten füllt das BM-2 Start/Ende selbst (Ende = Start + 3 h, ggf. nächster Tag). Ende-Datum und
Ende-Zeit sind einzeln schreibbar; liegt der zusammengesetzte Endzeitpunkt zwischen zwei Schreibvorgängen in der
Vergangenheit (hier: Datum heute + alte Zeit 01:27), beendet das BM-2 den Partymodus sofort. Deshalb erst Uhrzeit, dann
Datum (bzw. umgekehrt, wenn das neue Enddatum später liegt). Alle Zeiten gelten in der BM-2-Uhr (geht 6 min vor).
`script.heizung_partymodus` ist entsprechend aufgebaut; der Urlaubsmodus (TN 10145–10149) hat denselben Aufbau, wurde
aber nicht getestet.

Fehler in den Programmwahl-Selects behoben: eine native `state`-Bedingung rendert keine Templates (`state: "{{ option }}"`
wurde wörtlich verglichen), dadurch kam nach jeder erfolgreichen Programmwahl eine falsche Push „nicht übernommen".
Jetzt Template-Bedingung `not is_state(...)`.

## Broadcast 0503 (FaStatusRaw) – Teildekodierung, Stand 20.10.2026

`01 00 48 ff 61 29 3c 3f` (21:18, Brenner Ein, Vorlauf 48,5, Rücklauf 41,9) und `01 00 00 ff 46 24 3b 3f` (22:21, Brenner
Aus, Vorlauf 35,0, Rücklauf 36,3, Warmwasser 59,5), `01 00 40 ff 38 1c 3b 3f` (22:27, Softstart, Vorlauf 28,4, Rücklauf 28,1):

| Byte | Beobachtung | Deutung |
|---|---|---|
| 1 | immer `01` | Blocknummer |
| 2 | immer `00` | Statusbyte (Kandidat für Störung/Flags – bisher nie ≠ 0) |
| 3 | `48` bei Brenner Ein, `40` bei Softstart, `00` bei Aus | Brennerzustand/Stellgröße, nicht verifiziert |
| 4 | immer `ff` | unbekannt |
| 5 | `61`→48,5 / `46`→35,0 / `38`→28,0 | **Kesseltemperatur, Wert/2** (3 Treffer) |
| 6 | `29`→41 / `24`→36 / `1c`→28 | **Rücklauftemperatur, ganze °C** (3 Treffer) |
| 7 | `3c`→60 / `3b`→59 | Warmwassertemperatur ganze °C (Hwctemp 59,5) – plausibel, 2 Treffer |
| 8 | immer `3f` | unbekannt (nicht Außentemperatur) |

Der Rohwert läuft jetzt als `sensor.ebusd_broadcast_fastatusraw_data` in die HA-Historie (Discovery von Hand), damit bei
einer echten Störung Byte 2/3 verglichen werden können. Eine Spezifikation für 0503 habe ich nicht gefunden (die eBUS-
Spezifikation von 2004 auf mikrocontroller.net beschreibt nur 05 01/05 02).

## Vorfall 20.10.2026 ab ca. 22:20: Außentemperatur ungültig, Anlage in AT-Frostschutz

| Zeit | Beobachtung |
|---|---|
| bis 22:06:35 | Master `0f` sendet jede Minute `Broadcast Datetime` nur mit Außentemperatur: 10,695 °C (nur dieses Feld, Zeit/Datum leer); `bm2/Outsidetemp` 10,6 °C (unverändert seit 20:27) |
| 22:07:05 | Test: 9-Byte-Schreibtelegramm (Time+Date) an `35`, vom BM-2 ignoriert |
| 22:07:28 | Test: ebusd sendet selbst einen `Datetime`-Broadcast `31 fe 0700` mit `10.6;22:08:00;20.10.2026` |
| 22:18 | ebusd-Neustart (bm2.csv), Log für 22:08–22:22 nicht mehr verfügbar |
| ab 22:22:35 | `0f` sendet **-127,977** (ungültig) statt der Außentemperatur, dauerhaft (Stand 22:39) |
| 22:26:50 | `bm2/Outsidetemp` (TN 10195) → `-`/unknown, später auch `OutsidetempAvg` (BM-2 und MK) |
| 22:30:15 | `RcTarget`-Broadcast von `f1`: Außentemperatur springt von 10,598 auf **51,203** (vorher stabil) |
| 22:32:38–58 | `MkStatus` und `HkStatus` → **AT_Frostschutz**, Therme `Betriebsart` → **Frostschutz**, Heizkreispumpe 55 %, Brenner aus, Wärmeanforderung `Operation` = off/5 °C |

Fakten: Der Außentemperaturwert kommt an dieser Anlage von Master `0f` (Hypothese: Wolf-Funkempfänger des
Funkaußenfühlers, nicht verifiziert). Ohne gültige Außentemperatur gehen beide Heizkreise in AT-Frostschutz.

Nicht verifiziert: ob der von ebusd gesendete Datetime-Broadcast (22:07:28) den Empfänger gestört hat oder der
Funkfühler unabhängig davon ausgefallen ist (Batterie/Funkstrecke). Zeitliche Nähe spricht für eine Prüfung, der
Wert war aber schon 2 h konstant. Konsequenz: **keine Broadcasts mehr von ebusd senden**; die Schreibzeile
`w,Broadcast,,Datetime` bleibt nur dokumentiert und wird aus der aktiven Konfiguration entfernt.

Fehlercode-Tabelle (`docs/fehlercodes-cgb2.md`): 15 = „Außenfühler defekt oder Wärmeerzeuger vom Netz getrennt" –
gilt für den Fühler an der Therme; wie das BM-2 den Funkfühlerausfall anzeigt, ist nicht dokumentiert.

## Weitere Telegrammnummern

- TN 5250 (BM-2): Wartung Fälligkeitsdatum, Typ BM2Date (ism7mqtt `BM2DateConverterTemplate`):
  Tag = (v & 31) + 1, Monat = ((v >> 5) & 15) + 1, Jahr = 2000 + (v >> 9). Gelesen 13096 → 09.10.2025, identisch mit der Cloud.
- BM2Time (ism7mqtt `BM2TimeConverterTemplate`): Stunde = v // 256, Minute = v % 256 (entspricht ebusd-Typ `VTM`).
  Gilt für TN 10161 Time, 10141 AntilegionellaStart (3102 → 12:30), Party 10153/10151, Urlaub 10148/10146.
- BM2Date gilt auch für 10160 Date, Party 10154/10152, Urlaub 10149/10147.
- Zeitprogramme aktiv: TN 10159 (HK bzw. MK), 10158 (WW), 10157 (Zirkulation), Werte 1–3; Programmwahlschalter gemeinsam
  TN 10130; Sommer-/Winterzeit automatisch TN 10102; Absenkstopp TN 702; Antilegionellen-Wochentag TN 257 (0 Aus, 1–7 Mo–So, 8 täglich).

## Offen / nicht verifiziert


- Warum die 9-Byte-Form des ISM7 von ebusd aus nicht angenommen wird.
- Bedeutung des Anhangs TN 349 = 0 (ISM7) bzw. TN 413 = 0 (offizielles ebusd-Format für die Therme).
- Mischerkreis (`86`) nimmt Schreibtelegramme mit Präfix `00` an (Parametertest 20.10.), prüft das Prüfbyte also wie das BM-2 nicht.
- Mischermodul (`52`): Schreiben mit CRC an die Slave-Adresse funktioniert und wird quittiert (anders als bei der Therme, die
  den Master `03` braucht). Ob `52` das Prüfbyte prüft, ist nicht getestet.

## Geräteerkennung (ebusd-Scan)

- `08`: Kromschröder, Ident ` !`, SW 2002, HW 0000
- `35`: Wolf, SW 0204, HW 0100
- `52`: Kromschröder, SW 0100
- `86`, `04`, `14`, `f6`: antworten nicht auf die Identifikationsanfrage.
  Ableitung nach eBUS-Regel „Slave = Master + 5 (mod 256)" ([ebusd-Wiki eBUS background](https://github.com/john30/ebusd/wiki/eBUS-background)):
  `04` = Slave des ISM7 (`ff`), `f6` = Slave von Master `f1`, `14` = Slave von Master `0f`. `f0` und `f1` sind als Master
  im Log sichtbar (`f1` sendet `RcTarget`-Broadcasts, `f0` liest das MM mit PBSB 5014); Master `0f` wurde nie gesehen.
  Welche Geräte hinter `f0`/`f1` stecken, ist nicht verifiziert.
