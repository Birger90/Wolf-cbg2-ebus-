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

## Vorfall 20.10.2026, 22:22–22:50: Außentemperatur ungültig, Anlage in AT-Frostschutz

| Zeit | Beobachtung |
|---|---|
| bis 22:06:35 | Master `0f` sendet jede Minute `fe 0700` nur mit Außentemperatur (Zeit/Datum `ff`): 10,695 °C; `bm2/Outsidetemp` 10,6 °C |
| 22:07:05 / 22:07:28 | Tests: 9-Byte-Schreibtelegramm an `35` (ignoriert) und ein `Datetime`-Broadcast von ebusd (`31 fe 0700`, 10,6; 22:08:00; 20.10.2026) |
| 22:18 | ebusd-Neustart, Log 22:08–22:22 nicht verfügbar |
| ab 22:22:35 | `0f` sendet **-127,977** (ungültig) |
| 22:26:50 | `bm2/Outsidetemp` (TN 10195) → `-`; später auch `OutsidetempAvg` (BM-2, MK) |
| 22:30:15 | `RcTarget`-Broadcast von `f1`: Außentemperatur 51,203 statt 10,598 |
| 22:32:38–58 | `MkStatus`/`HkStatus` → **AT_Frostschutz**, Therme → **Frostschutz**, Pumpe 55 %, Brenner aus, `Operation` off/5 °C: **keine Heizung**, nur Frostschutz; Warmwasser unabhängig (Speicher 58,7 °C) |
| 22:38:10 | ISM7-Abfrage TN 1 am BM-2 (`ff 35 5022 03 5c 01 00`) antwortet **15** statt 0 → BM-2 zeigt „T außen"; Birger quittiert 22:43, Störung kommt sofort wieder |
| 22:50:35 | `0f` sendet wieder gültig: 10,148 °C – **von selbst**, vor allen weiteren Tests |
| 22:55:19 | ISM7 schreibt Partymodus (App): `ff 30 5023 15 71 a627 0100 a727 0117 a827 3435 a927 0117 aa27 3335` – 21 Byte, 5 TN/Wert-Paare in einem Telegramm an Master `30` |
| 22:55:18 / 22:56:55 | `bm2/Outsidetemp` 10,1 °C, TN 1 = 0 („keine Störung"), `HkDemand` Partymodus, Therme Heizbetrieb Soll 46 °C |

Fakten: Die Außentemperatur dieser Anlage kommt ausschließlich vom Master `0f` (Hypothese Funkempfänger, nicht
verifiziert). Ohne gültigen Wert: beide Heizkreise AT-Frostschutz, keine Wärmeanforderung. Birger hat eine neue
Batterie für den Funkaußenfühler bestellt; der Ausfall dauerte 28 min.

Nicht verifiziert: Ursache des Ausfalls. Der ebusd-Broadcast von 22:07:28 liegt zeitlich davor; das BM-2 ignoriert
Broadcasts von `31` nachweislich (siehe unten), ob der Empfänger `0f` darauf reagiert, bleibt offen. Der Wert kam ohne
weiteres Zutun zurück. Konsequenz bleibt: keine Broadcasts von ebusd.

### Test „Ersatz-Außentemperatur per eBus" (Freigabe Birger 22:50, Ergebnis negativ)

ebusd sendete 22:55:11 und 22:56:17 exakt die Form von `0f` (`fe 0700`: 5,7 °C als D2B, dann 7× `ff`; Log
`sent update-read Broadcast Datetime QQ=31: 5.699;-:-:-;-.-.-`). `bm2/Outsidetemp` blieb 4 s und 9 s später bei 10,1 °C
(Wert von `0f`). Das BM-2 übernimmt die Außentemperatur also nicht von Master `31`. Schreibdefinition entfernt, das
getrennte Mitlesen von `0f` bleibt (`u,Broadcast,,OutsidetempRadio,…,0f,fe,0700`).

### Zweiter Test: Ersatzwert mit Absenderadresse `0f` (Freigabe Birger 23:10, Ergebnis **positiv**)

MQTT kann keine fremde Absenderadresse setzen (ebusd `mqtthandler.cpp` ruft `readFromBus()` immer mit der eigenen
Adresse auf; die QQ-Spalte der CSV gilt nur für passive Nachrichten). Deshalb: ebusd mit `--enablehex`, in Home Assistant
`shell_command.ebusd_cmd` (sendet eine Zeile an den TCP-Kommandoport 8888 der App `b4d7ad18-ebusd`, Antwort als
`service_response.stdout`; dafür `configuration.yaml` ergänzt und HA neu gestartet, Sicherung in `homeassistant/backup/`).

| Zeit | Aktion | Ergebnis |
|---|---|---|
| 23:14:0x | `read -f -c bm2 Outsidetemp` | 10.1 |
| 23:14:20 | `hex -s 0f fe0700099a0affffffffffffff` (10,6 °C als D2B `9a 0a`, Rest `ff`, Absender `0f`) | `done broadcast` |
| 23:14:2x | `read -f -c bm2 Outsidetemp` | **10.6** – vom BM-2 übernommen |
| 23:14:35 | echter Empfänger `0f` sendet 10,148 | – |
| 23:14:4x | `read -f -c bm2 Outsidetemp` | 10.1 – wieder der echte Wert |

Folgerung: Das BM-2 filtert nach Absenderadresse `0f`, nicht nach Inhalt. Mit `-s 0f` lässt sich bei einem Ausfall des
Funkfühlers ein Ersatzwert einspeisen. Offen/Risiko: Sendet der echte Empfänger gleichzeitig (gleiche Adresse), gibt es eine
Buskollision; deshalb nur in der Mitte zwischen zwei Empfänger-Telegrammen senden (Empfänger sendet bei ca. hh:mm:35).
Ob das BM-2 bei einem echten Ausfall (Empfänger sendet -127,977) dem Ersatzwert oder dem ungültigen Wert folgt, ist nicht
getestet – beide kämen von `0f`, es zählt vermutlich der jeweils letzte.

Alternative, von Birger selbst geprüft: Programmwahl „Permanent" → Therme geht in Heizbetrieb (zeitgleich war die
Außentemperatur wieder da, Anteil nicht trennbar).

### Störungscode gefunden: TN 1

Das ISM7 liest alle 15 s `5c 01 00` (Prüfbyte 5c = CRC von `01 00`, also TN 1) auf `08`, `35` und `52`. Antworten:
Therme 0, Mischermodul 0, BM-2 **15** während der „T außen"-Störung und 0 danach. TN 1 ist in der Wolf-Parameterdatenbank
für CGB-2/BM-2/MM nicht enthalten (nur für CWL als „Lüftungsstufe"), passt aber exakt zur Fehlertabelle (15 = Außenfühler
defekt). Deshalb `fault.csv` mit `FaultCode` für hc/bm2/mm (r5, Präfix 5c → die ISM7-Abfragen werden passiv mitgelesen,
im Log `received poll-read bm2 FaultCode QQ=ff: 15`). In HA: `sensor.heating_ebusd_{hc,bm2,mm}_faultcode` (Zahl),
`sensor.heizung_storung_{therme,bm_2,mischermodul}` (Klartext über Makro `wolf_fault_text`), Automation
„Heizung: Stoerungscode" (Push bei Code ≠ 0 und Entwarnung).

## Busanalyse 20.10.2026, 23:15–23:28 (alle noch unbekannten Telegramme)

Grundlage: ~900 als `unknown` geloggte Telegramme, Telegrammnummern gegen die Wolf-Datenbank (alle Gerätetypen) geprüft.

### Neu dekodiert und in ebusd übernommen

| Telegramm | Inhalt | Beleg | ebusd |
|---|---|---|---|
| `30 fe 0301`, 14 Byte, alle 30 s | BM-2-Status: Byte 1–2 aktuelle Außentemperatur ×10 (SIN), Byte 3–4 Raumtemperatur ×10 (`0080` = kein Fühler), Byte 6 Störungscode | `65 00` = 10,1; um 23:18:30 `ce ff` = **−5,0** direkt nach dem Testwert; 22:43 Byte 6 = `0f` = 15 während „T außen“ | `Broadcast BmStatus` |
| `03 fe 0503`, 8 Byte | Feuerungsautomat: Byte 5 Kesseltemperatur ×2, Byte 6 Rücklauf, Byte 7 Warmwasser | 3 Messpunkte + 23:27 `25.0;25;57` | `Broadcast FaStatus` |
| TN 371 an `08` (BM-2 liest laufend) | Ausgänge als Bitfeld: Bit 4 Heizkreispumpe, Bit 5 3-Wege-Ventil, Bit 6 A1, Bit 7 Speicherladepumpe (Wolf-DB CGB-2); Bit 1/2 bei anderen Geräten Gasventil 1/2 | 21:18 Brenner ein: 22 = Bit 1,2,4; 23:28 aus: 4 = Bit 2 | `hc Outputs` |

### Dekodiert, aber nicht übernommen (nur Doku)

ISM7-Blockabfragen (`ff … 5022 0b`, 5 TN je Telegramm, Antwort 10 Byte), Inhalt jeweils plausibel geprüft:
- an `08`: TN 554/10010/10013/10067/10068 (Brennerstunden 15400, Druck, Abgas 29,0, Betriebsart 13 Standby, Brennerstatus 0);
  TN 22/328/367/370/371 (Rücklauf 26,0, Typ 33 = CGB-2, Modulation 0, Brenner 0, Ausgänge 4);
  TN 2/3/12/13/14 (Kesselsoll 5,0, WW-Soll 10,0, Außen `0080`, Vorlauf 25,1, WW 57,5)
- an `35`: TN 10158/10159/10164/10165/10179, 10145/10150/10155/10156/10157, 10101/10109/10117/10119/10134, 19/5249/5250/5266/10100
- an `86`: dieselben HK-TNs für den Mischerkreis
- Einzelabfragen ISM7: TN 550–553 (Starts/Netzstunden), 10071 (Pumpe), 10888 („erweiterte Statistik aktiv“, Antwort `0080`), an `52` TN 86 und 87 (Antwort 0, nicht in der Datenbank)

BM-2 (`30`) liest an `08` zusätzlich (Prefix `cc`, Wolf-DB-Namen soweit vorhanden): 10063 IO-Istwert (3), 10006 Eingang E1
(65088 = „Geöffnet“), 10806/10807 Eingang E3/E4 (`0080`), 10804/10805 Funktion A3/A4 (0), 2751 Funktion A1 (1), 10033
Anlagenkonfiguration (1), 10096 WW-Schnellstart (0), 10833 Status EA-Modul (0 = nicht vorhanden), 10007 Sammlertemperatur
(`0080`), 10876 Heizkreisdurchfluss (`0080`, nur CGB-2 38–100 kW), 1113 (`1516` = 5653; bei COB „Brennerstunden 2. Stufe“,
für CGB-2 nicht dokumentiert), 12057, 10870, 10090, 10083, 10039, 10711, 10084, 10074, 10073, 10034, 10003, 10002, 5000
(nicht in der Datenbank für CGB-2). An `52`: 756, 2593 Konfiguration (3), 711 Konstanttemperatur (750 → 75,0), 45 (150 → 15,0),
14 (`0080`). An `ff`: TN 10920/10921 (SmartHome-System, Plug-in-Version; ohne Antwort, `ff` ist Master).

BM-2-Broadcasts `30 fe 5023` (Schreiben an alle): TN 35 = 0 (Parallelbetrieb), TN 10830 = 0, TN 2560 = 20 (beide nicht in der DB für BM-2).

### Noch offen

- `5014` (`30 → 50` und `f0 → 52`), Antwort 9 Byte: Byte 3–4 sind beim MM (`52`) die Mischervorlauftemperatur als D2B
  (21:18 `4d 24` = 36,30 °C = ebusd mm/Flowtemp 36,3; 23:22 `00 19` = 25,0); bei `50` steht dort `00 9c` (ungültig → kein
  Fühler). Byte 8–9 beim MM `6e 28` = 40,43 (Hypothese: Mischer-Soll). `50` antwortet, ist aber kein bekanntes Gerät.
- `03 f1 0800`: Feuerungsautomat an Master `f1`, Format wie RcTarget (Werte `0080` = ungültig).
- Was die Master `f0`/`f1` sind (nicht verifiziert).

## Nachtmitschnitt 20./21.10.2026 (Aufbau)

- `ebusd-config/listen.csv`: passive Definitionen (Typ `r` ohne Priorität, ebusd fragt nicht selbst ab) für alle bisher
  unbekannten Telegramme von BM-2 und ISM7; Discovery-Filter um `^listen$` erweitert → HA zeichnet die Rohwerte als
  `sensor.heating_ebusd_listen_*` auf. Strings (HEX) werden von der HA-Integration nicht veröffentlicht, deshalb zusätzlich
  ebusd `grab` (sammelt alle unbekannten Telegramme mit Anzahl und letztem Inhalt; Abruf `shell_command.ebusd_cmd` `grab result`).
- Auswertung um 01:30, 04:30 und 07:30.
- Vergleichsquelle: Ein anderer Nutzer (simon42-Forum, „Ebusd V5.0 mit einem Wolf BM Bediengerät“) zeigt dasselbe 0503-Format
  `03fe0503 08 01 00 40 00 38 1c 2e 09` (Kessel 0x38/2 = 28, Rücklauf 0x1c = 28) → bestätigt die Byte-Zuordnung von FaStatus.

### Durchgang 1 (21.10.2026, 01:30; Zeitraum 23:39–01:32)

Anlagenzustand im ganzen Zeitraum: Therme Standby, Brenner aus (seit 22:58), Kesselsoll 5,0, Modulation 0, Pumpe 0,
BM-2-Heizkreis „Eco“, Außentemperatur 10,3. Die Anlage kühlt aus (Vorlauf 24,8 → 23,3, Rücklauf 25,8 → 24,6,
Speicher 57,2 → 54,3). Korrelationen mit Brenner/WW-Ladung waren deshalb in diesem Durchgang nicht möglich.

**Was sich geändert hat:** von allen 48 `listen`-Sensoren nur `M5014_52_20 temp` (24,602 → 22,898 in 0,1-K-Schritten),
parallel zu Therme-Vorlauf und MM-Vorlauf → bestätigt erneut Byte 3–4 der 5014-Antwort = Mischervorlauf. Alle übrigen Rohwerte
(TN 10006, 1113, 10063, 10084, 10711, 10039, MM 2593/45/711, 5014 `temp2` 40,43, `b5` 3, `b7` 10, Adresse `50` usw.) blieben
konstant. `temp2` = 40,43 blieb auch bei ausgekühltem Mischerkreis gleich → passt zu einem Sollwert/Parameter, nicht zu einem
Messwert (Bedeutung weiter nicht verifiziert).

**Ausgänge TN 371:** Seit 23:28 durchgehend 4 (nur Bit 2) bei Brenner aus; um 21:18 bei Brenner ein 22 (Bit 1, 2, 4).
Bit 2 ist also auch bei ausgeschaltetem Brenner gesetzt → die aus anderen Wolf-Geräten übernommene Deutung
„Bit 2 = Gasventil 2“ trifft hier nicht zu. Bit 1 korreliert bisher mit Brenner ein (1 Messpunkt, nicht verifiziert).

**`grab result`, neu seit der Busanalyse:**

- Master `f0` sendet ebenfalls einen `0301`-Broadcast: `f0 fe 0301 0e 67 00 00 80 00 00 00 01 00 00 00 00 00 00`
  → gleiches Format wie beim BM-2 (`30`): Byte 1–2 = `67 00` = 10,3 °C Außentemperatur, Byte 3–4 `0080` = kein Raumfühler.
  Erste Hypothese „zweites Bediengerät“ ist **widerlegt**: Laut Birger gibt es kein zweites Bediengerät (21.10.2026, 04:04).
  Über die Nacht nur 2× gesehen (Außentemperatur `67 00` = 10,3 und `69 00` = 10,5), das BM-2 (`30`) dagegen 526×.
- **`f0` meldet sich mit derselben Kennung wie das BM-2** (ebusd-Log 21.10.2026):

  | Zeit | Absender | IdAnswer (`fe 0704`) |
  |---|---|---|
  | 03:58:49.012 | `f0` | Kromschroeder, SW 0100, HW – |
  | 03:58:49.252 | `f0` | Kromschroeder, SW 0204, HW 8080 |
  | 03:58:51.498 | `30` | Kromschroeder, SW 0100, HW – |
  | 03:58:51.738 | `30` | Kromschroeder, SW 0204, HW 8080 |

  Sonst sendet `30` alle paar Minuten nur die Kennung SW 0204/HW 8080 (03:53:21, 04:01:22). Der identische Zweierblock
  von `f0` und `30` im Abstand von 2,5 s, das gleiche `0301`-Format mit derselben Außentemperatur und die 5014-Abfrage des
  Mischermoduls (`f0 → 52` alle 15 s) passen zu der Deutung: **`f0` ist eine zweite Masteradresse des BM-2**, vermutlich für
  den Mischerkreis (das BM-2 fragt mit `30` die Adresse `50` ab, mit `f0` das Mischermodul `52`). Nicht verifiziert – keine
  Wolf-Dokumentation dazu gefunden. Nach der eBUS-Prioritätsreihenfolge ist `f0` Master Nr. 5 (Forenliste im ebusd-Repo:
  `10`/`30`/`70` = Regler 1/2/3, `50`/`51` = Mischer 1/2, [Discussion #779](https://github.com/john30/ebusd/discussions/779)).
  Die Kennung SW 0100 / HW „–“ entspricht der Softwareversion, die der ebusd-Scan für das Mischermodul `52` meldet
  (SW 0100); warum das BM-2 sie mitsendet, ist offen.
- Einmalige ISM7-Abfragen (wohl beim Verbindungsaufbau der Wolf-App), Antworten gegen die Wolf-Datenbank geprüft:

| Adresse | TN | Wolf-DB-Name | Rohwert | Deutung |
|---|---|---|---|---|
| `08` | 10878 | Herstelljahr | `0x13` = 19 | 2019 – laut Birger passend zur Therme |
| `08` | 10877 | Herstellwoche | `0x2c` = 44 | KW 44 – laut Birger passend |
| `08` | 10879 | – (nicht in der DB) | 2 | unbekannt |
| `08` | 10880 | – (nicht in der DB) | `0x6a79` = 27257 | unbekannt |
| `08` | 10075 | Warmwasserkonfiguration | 5 | Listeneintrag 5 = `DHWCoilStorNoHead` (Speicher mit Heizschlange) |
| `08` | 2651 | Funktion E1 | 0 | – |
| `08` | 410 | Firmware | `0xdc` = 220 | 2.20 (= ebusd `hc Firmware` 2.2) |
| `35` | 10185 | BM-2 Softwareversion | `0x118` = 280 | Darstellung (2.80?) nicht verifiziert; ebusd-Ident meldet SW 0204 |
| `35` | 10163 / 10162 | erkannte Geräte Low/High | 260 / `0x0800` | Bitfeld, Zuordnung nicht verifiziert |
| `35` | 10180 | Anforderung Lüftung | 8 | – |
| `35` | 10920 | SmartHome-System | 0 | – |
| `35` | 10812 | Vereinfachter Modus | 0 | – |
| `35`, `86` | 9024 / 9028 / 9007 | aktuelle Kreisart / Kühlkurve global / Raumeinfluss Kühlen | `0080` / `0080` / 0 | keine Kühlfunktion |
| `52` | 410 | Firmware | 0 | MM liefert keine Version über TN 410 |

### Durchgang 2 (21.10.2026, 04:30; Zeitraum 01:30–04:30)

Weiter ruhige Nacht: Therme durchgehend Standby, Brenner aus, **keine Brennerstarts** (BurnerStartsLow 52854 unverändert),
**keine Warmwasserladung** (Speicher 54,4 → 50,4 °C ohne Nachladung; WW-Soll der Therme nachts 10,0 → Zeitprogramm aus),
Heizkreis „Eco“, Pumpe aus, Ausgänge TN 371 weiter 4 (Bit 2). Außentemperatur 10,3 → 10,6.
Rohwerte: wieder nur `M5014_52_20 temp` (22,9 → 21,8, = Mischervorlauf) geändert; `temp2` 40,43 und alle übrigen
`listen`-Werte konstant. Neu in diesem Zeitraum nur die Kennungsmeldungen von `f0`/`30` um 03:58 (siehe oben).
Antilegionellenfunktion läuft laut Einstellung erst Freitag – in dieser Nacht nicht beobachtbar.

## Abdeckungsprüfung gegen die Wolf-Parameterliste (21.10.2026, 04:20–04:35)

Methode: Parameterlisten der Wolf-App (ism7mqtt `device.xml`/`parameter.xml`/`converter.xml`, Vorlagen CGB-2, BM-2,
DHK_BM-2, MK_BM-2, WW_BM-2, WWSystem_BM-2, ZirkSol_BM-2, MM) mit den TNs in `ebusd-config/*.csv` verglichen
(Skript im Scratchpad, Regel: Prüfbyte/TN aus der ID-Spalte). Anschließend jede fehlende, für diese Anlage relevante TN
**einmal gelesen** (`hex`, nur Lesen). Lüftung, Kühlen, SmartHome und AFB (Fernbedienung) ausgelassen – nicht vorhanden.

Achtung: Die Geräte antworten auch auf unbekannte TNs (z. B. MM auf TN 1 mit 0). Eine Antwort 0 beweist deshalb nicht,
dass es den Parameter gibt; plausible Werte ≠ 0 sprechen dafür.

| Gerät | TN | Wolf-Name | Rohwert | Wert (Typ aus converter.xml) |
|---|---|---|---|---|
| Therme `08` | 383 | Nachlaufzeit Speicherladepumpe (1–10 min) | `0300` | 3 min |
| | 384 | Max. Speicherladezeit (30–180 min) | `7800` | 120 min |
| | 65019 | eBus Einspeisung (Auto/Aus/Ein) | `0000` | 0 = Auto |
| | 10041 | Typ Pumpenregelung (Festwert/Linear/dT) | `0100` | 1 = Linear |
| | 10076 | Anlagenkonfiguration | `0100` | Schlüssel 1 → Anzeige „2“ |
| | 10014 | Drehzahl ZHP WW (15–100 %) | `5500` | 85 % |
| | 10030 | Hysterese Sammler (SS10) | `3200` | 5,0 K |
| | 10028 | Kesselübertemperatur Sammler (SS10) | `3c00` | 6,0 K |
| | 10017 | WW-Regelung (BUSCONFIG Anschluss Speicher) | `0000` | 0 |
| | 328 | Typ | `2100` | 33 = CGB-2 |
| | 370 | Brenner (Bit 3) | `0000` | Aus |
| | 10009 | Auslauftemperatur WW (SS100) | `0080` | ungültig (kein Fühler) |
| | 10802 / 10803 | Funktion Eingang E3 / E4 | `0000` | 0 = keine Funktion |
| Mischermodul `52` | 400 | RL-Solltemperatur (20–80 °C) | `2c01` | 30,0 °C |
| | 384 | Max. Speicherladezeit (0–5 h) | `0200` | 2 h |
| | 340 | Hysterese Bypassfühler | `6400` | 10,0 K |
| | 36 | Ladepumpensperre (0/1) | `0000` | 0 |
| | 383 | Nachlaufzeit Ladepumpe (0–10 min) | `0300` | 3 min |
| | 405 / 404 | dT Aus / dT Ein | `3200` / `6400` | 5,0 / 10,0 K |
| | 839 | Sperrung Brenner bei Rücklaufanhebung (0–300 s) | `0000` | 0 s |
| | 20035 | Frostschutz LH-Kreis | `1400` | 2,0 °C |
| | 320 | Speicherhysterese | `3200` | 5,0 K |
| | 308 | Warmwassermaximaltemperatur (60–80 °C) | `5802` | 60,0 °C |
| | 101 | Betriebsstatus Mischerkreis (Bit 4–7) | `0000` | 0 |
| | 3 | Warmwassersolltemperatur | `c201` | 45,0 °C |
| | 2601 / 2602 | Eingang E1 / Analogeingang E2 | `70fe` | −40,0 (offen/kein Fühler, nicht verifiziert) |
| BM-2 `35` | 10121 | Funktion des Bedienmoduls | `0000` | 0 = System |
| | 271 | Raumeinflussfaktor (1–20) | `0400` | 4 |
| | 265 | Anpassung Raumfühler (SS10) | `0000` | 0,0 K |
| | 701 | Raumtemperaturabhängige Abschaltung | `0100` | Ein |
| | 1443 | Korrektur Außentemperatur (SS10, −15…5) | `0000` | 0,0 |
| | 20018 | Reiner Raumregler | `0000` | Aus |
| | 41 / 42 | PI-Regler Raum Kp / Tn | `1400` / `0a00` | 20 / 1,0 |
| | 5264 | Wartungsmeldung Datum (BM2Date) | `2833` | 13096 → 09.10.2025 |
| | 10922 / 10923 | WS/ECO-ABS bzw. DHK gesteuert von | `0000` | BM-2 |
| BM-2 `35`, MK `86` | 9005 / 651 | Kreisart / Raumeinfluss | `0000` | Heizkreis / Aus |

Ergebnis Abdeckung (vor dieser Prüfung; „schreibbar“ = Schreibweg vorhanden und getestet):
- Therme: von 28 einstellbaren App-Parametern 16 schreibbar getestet (HG01–HG04, HG07–HG09, HG15–HG17, HG22, HG25, HG33,
  HG38, HG39, HG60), HG21 (TK-min) und 10096/10887 nur gelesen, 10 fehlten (Tabelle oben). HG10/HG12 gesperrt.
- Mischermodul: 19 einstellbar, 5 schreibbar getestet, 3 nur gelesen (Konfiguration gesperrt, 711, 45), 11 fehlten.
- BM-2/MK: Bedienparameter, Heizkurven, Programme, Party/Urlaub/1×WW schreibbar; fehlten Raumregler-Parameter (ohne
  Raumfühler wirkungslos) und Korrektur Außentemperatur; Uhr nicht stellbar.

### Abgleich mit den Anleitungen (21.10.2026, 04:30)

Quellen: Wolf CGB-2-14/20/24 Betriebsanleitung Fachkraft 3063421_202405 (Parametertabelle Kap. 23, Spalte 24 kW),
Wolf MM/MM-2 Montageanleitung und BM-2 Montageanleitung Experte (beide farko.com, von Birger verlinkt), Screenshots von
Birger aus 8616991_202111 – **das ist die Anleitung der CGB-2-68/75/100**, nicht unserer CGB-2-24; Werkseinstellungen
und Bereiche können abweichen.

Therme (gelesene Werte gegen Werkseinstellung 24 kW):

| HG | TN | gelesen | Werk 24 kW | Bemerkung |
|---|---|---|---|---|
| HG13 Funktion E1 | 2651 | 0 = keine | 0 | – |
| HG14 Funktion A1 | 2751 | 1 = Zirkulationspumpe 100 % | 0 | eingestellt (Liste aus Wolf-DB) |
| HG19 Nachlaufzeit SLP | 383 | 3 min | 3 | = Werk |
| HG20 max. Speicherladezeit | 384 | 120 min | 120 (30/Aus–300) | Wolf-DB nennt 30–180 |
| HG34 eBus-Einspeisung | 65019 | Auto | Auto | = Werk |
| HG37 Typ Pumpenregelung | 10041 | Linear | Linear | = Werk |
| HG40 Anlagenkonfiguration | 10076 (auch 10033) | Rohwert 1 → laut Wolf-DB-Liste „02“ | 01 | **Zuordnung Rohwert→Anzeige nicht verifiziert**, am BM-2 ablesen |
| HG41 Drehzahl ZHP WW | 10014 | 85 % | 85 % | = Werk |
| HG42 Hysterese Sammler | 10030 | 5,0 | 5 | = Werk |
| HG46 Kesselübertemp. Sammler | 10028 | 6,0 | 6 | = Werk |
| HG56/57 Funktion E3/E4 | 10802/10803 | 0 | – | E/A-Modul nicht vorhanden (TN 10833 = 0) |
| HG58/59 Funktion A3/A4 | 10804/10805 | 0 | – | dito |
| HG61 WW-Regelung | 10017 (Wolf-DB „BUSCONFIG Anschluss Speicher“) | 0 | Kesselfühler | Zuordnung TN↔HG61 nicht verifiziert |

Mischermodul (MI-Parameter laut MM-Anleitung): MI05 Konfiguration = TN 2593 = **3 = „Mischerkreis und direkter
Heizkreis“** (Pumpe des direkten Kreises an Ausgang A1 des MM). Gleich Werk: MI08 RL-Soll 30 (TN 400), MI09 2 h (TN 384),
MI11 10 K (TN 340), MI12 0 (TN 36), MI13 3 min (TN 383), MI14 75 °C (TN 711), MI15 5 K (TN 405), MI16 10 K (TN 404),
MI18 0 s (TN 839). Abweichend: MI17 Kesselübertemperatur Speicherladung Werk 10 K, TN 45 = 15,0 (eingestellt oder andere
Bedeutung, nicht verifiziert). MI10 Busspeisung = `EbusPower` (gesperrt). Die MM-Fehlercodes der Anleitung (FC52, 70, 71,
79, 81, 91, 97) sind identisch mit unserer Tabelle aus der Wolf-Datenbank.

BM-2 (A-Parameter laut BM-2-Anleitung Experte): Funktion BM-2 = TN 10121 = 0 = System ✓; A00 Raumeinflussfaktor 4
(TN 271 ✓ Werk); A04 Außenfühler gemittelt 3 h (TN 388); A05 Anpassung RF 0 (TN 265 ✓); A10 Parallelbetrieb (TN 35);
A11 Raumtemperatur-Abschaltung Ein (TN 701 ✓); A15 Korrektur Außentemperatur 0 K, Bereich laut Anleitung −5…+5 K
(TN 1443 = 0; Wolf-DB nennt −15…5); A16 Reiner Raumregler Aus (TN 20018 ✓); A17 P-Anteil 20 (TN 41 ✓); A18 I-Anteil 1,0
(TN 42 ✓). A00/A05/A16–A18 wirken laut Anleitung nur mit Raumfühler bzw. BM-2 als Fernbedienung im Wandsockel.

Fehlercodes/Historie: Die 68–100-kW-Anleitung nennt zusätzlich 28 „Gasdruckwächter“ und 225 „Fehlercode unbekannt“
(nicht in der Wolf-DB-Liste für CGB-2). Warnmeldungen (1, 2, 3, 4, 5, 24, 43) sind eine eigene Liste; ob sie über TN 1
kommen, ist nicht beobachtet. Das BM-2 führt eine Störungshistorie (Fachmannebene, Einträge mit Code, Datum, Uhrzeit;
Anzahl nicht angegeben). Über die Wolf-Datenbank ist sie nicht lesbar (`HasOwnFaultMessageHistory` = false), eine TN dafür
ist nicht bekannt.

### Funk-Außenfühler und Funkempfänger (Anleitung 3060938_1007, von Birger verlinkt, 21.10.2026)

Die Anleitung ist von 2007 und für WRS-/5W-Regelungen geschrieben; ob alles für das BM-2 gilt, ist nicht verifiziert.
- Außenfühler sendet alle **30 min** (der Empfänger `0f` wiederholt den Wert auf dem eBus jede Minute, beobachtet).
- Batterie 3,6 V Lithium (z. B. Saft LS 14250, Xeno XL-050F, Sonnenschein SL-350), Lebensdauer ca. 5 Jahre. Bei
  schwacher/fehlender Batterie zeigt die Regelung eine Außenfühlerstörung (passt zu Code 15 am 20.10.).
- Empfänger-LEDs: rot dauernd = keine Verbindung zum Fühler/gestörter Empfang; **gelb an = kein DCF-Empfang bzw. nicht
  synchronisiert**; grün blinkt im Sekundentakt = DCF-Empfang.
- Der Empfänger enthält eine **DCF77-Funkuhr**; laut Anleitung stellt sich die Uhr der Regelung danach nach ca. 5 min.
- Beobachtung dazu: `0f` sendet den `0700`-Broadcast mit Uhrzeit/Datum = `ff` (ungültig) → Hypothese: Der DCF-Teil des
  Empfängers ist nicht synchronisiert, deshalb läuft die BM-2-Uhr frei (+6 min). Prüfbar an der gelben LED. Nicht verifiziert.
- Forenangabe (ebusd Discussion #779, realResi): das BM nimmt Zeit-Broadcasts von `0f` oder `30` an. Ein Test
  „`0700` mit gültiger Zeit von `-s 0f`“ wäre der nächste Versuch, die BM-2-Uhr zu stellen (noch nicht gemacht).

### Uhr stellen über Absender `0f` und Wartung zurücksetzen (21.10.2026, 04:32–04:40, auf Wunsch von Birger)

- 04:32:52 `hex -s 0f fe0700099e0a55320421100326` (Außentemperatur 10,617 wie vom Empfänger, Zeit 04:32:55, Datum
  21.10.(Mi)26) → `done broadcast`. Ergebnis: **Uhr nicht übernommen** (TN 10161 um 04:37:52 = 1068 = 04:44, weiter +6 min).
  Nebenwirkung: Das BM-2 sendet seinen minütlichen Datetime-Broadcast (`30 fe 0700`, sonst jede Minute bei :58) seit
  04:31:58 **nicht mehr** (Stand 04:39). Hypothese: Das BM-2 hält jetzt eine Funkuhr am Bus für vorhanden und überlässt ihr
  die Zeit. Nicht verifiziert; ob der Broadcast von selbst wiederkommt, wird beobachtet. Außentemperatur, BmStatus,
  Störungscodes unverändert normal.
- Therme `03` sendet `fe fe01` (ebusd `Broadcast Error`) mit `E000 04:37` um 04:36:58 → die Therme führt die **richtige**
  Uhrzeit (Quelle offen).
- Wartung: TN 5250 (Fälligkeitsdatum) und TN 5264 (Wartungsmeldung Datum) über `BmRaw` (`00 82 14 34 37` bzw.
  `00 90 14 34 37`) von 13096 (09.10.2025) auf **14132 = 21.10.2027** gesetzt, beide zurückgelesen ✓, obwohl die Wolf-App
  beide als nur lesbar führt. HA: `binary_sensor.heizung_wartung_fallig` = aus.
  04:41 auf Wunsch von Birger zurückgestellt: beide wieder 13096 (09.10.2025), zurückgelesen ✓ → Schreiben und Rückstellen
  von TN 5250/5264 per `BmRaw` damit zweimal bestätigt.
- Störung quittieren: In der Wolf-Datenbank gibt es „Störung Quittieren“/„Acknowledge alarm“ nur für andere Gerätetypen
  (Lüftung CWL, WRS), nicht für CGB-2/BM-2/MM. Weg der Quittieren-Taste auf dem Bus unbekannt.

### BM-2 Betriebsanleitung für die Fachkraft ab FW 2.80 (3063305_201910, von Birger hochgeladen)

- Störung quittieren (Kap. 15.3/15.4): Statusseite „Meldung“, **Taste 4**, nur wenn eine Störung ansteht und das BM-2 im
  Heizgerät sitzt; verriegelnde Störungen zusätzlich mit Fachmanncode („RESET durchführen“). Warnungen müssen nicht
  quittiert werden; Fühlerstörungen quittiert die Regelung selbst. Welches Telegramm das BM-2 dabei sendet, ist unbekannt –
  nur bei einer echten Störung mitschneidbar.
- Meldungshistorie (Kap. 30): bis zu 40 Störungen mit Beginn und Ende (Datum/Uhrzeit), nur im Fachmann-Menü.
- A08 Wartungsmeldung (Aus/Betriebsabhängig/Datumsabhängig), A25 Wartungsmeldung Datum: Werk = heute + 1 Jahr,
  Bereich heute … heute + 2 Jahre → der gesetzte Wert 21.10.2027 liegt genau an der Obergrenze. Zurücksetzen am Gerät:
  Fachmann → „Wartungsmeldung Reset“.
- Uhrzeit/Datum: Hauptmenü → Grundeinstellungen → Uhrzeit bzw. Datum (ohne Fachmanncode); Sommer-/Winterzeit automatisch
  über den ewigen Kalender. Funkuhrmodul mit Außenfühler: „Das DCF-Zeitsignal sendet die genaue Uhrzeit und das aktuelle Datum.“

### HG40 laut Anleitung CGB-2-14/20/24 (3063421_202106, Kap. 24)

- **02 = „Ein oder mehrere Mischerkreise über Mischermodule (kein direkter Heizkreis am Brennwertgerät)“**, interne
  Gerätepumpe als Zubringerpumpe. 01 (Werk) = direkter Heizkreis am Gerät, Gerätepumpe als Heizkreispumpe.
- Unser Rohwert TN 10076 = 1 → laut Wolf-DB-Liste „02“. Das passt zur Anlage: Das Mischermodul steht auf MI05 = 3
  „Mischerkreis und direkter Heizkreis“, d. h. die Pumpe des direkten Heizkreises hängt am Ausgang A1 des MM, die Therme
  arbeitet nur als Zubringer. Die Zuordnung ist damit stimmig, am Display aber weiterhin nicht abgelesen.

### Quittieren-Test (21.10.2026, 04:47, Birger drückt „quittieren“, keine Störung aktiv)

- 04:47:09–13: ISM7 (`ff`) fragt die Kennung von `08`, `35`, `52` ab (`07 04`) – sonst nur selten.
- ab ca. 04:47:35: Therme **Nachspülen** (Brennerstatus 7, Gebläse/Modulation 60–69 %, Ausgänge TN 371 = 6), bis 04:48:20,
  dann wieder Aus. Kein Brennerstart (BurnerStartsLow unverändert).
- Ein eigenes „Quittieren“-Telegramm auf dem Bus wurde **nicht** gefunden: In `grab result` keine neue Variante von
  `30 03 0507` (Operation, 1237× gleicher Inhalt), keine Schreibtelegramme (`5023`) an `08`/`03` außer den bekannten.
  Nur einmalig neu: `f0 fe 0503 08 01 00 00 ff 2d ff 32 0a` (f0 sendet einmal das 0503-Format wie `f1`) und einzelne
  ISM7-Lesungen (MM TN 101, 383; BM-2 TN 20018).
- Deutung (nicht verifiziert): Das Nachspülen passt zu einem Neustart/Entriegeln des Feuerungsautomaten. Wenn direkt an der
  Therme (Entstörtaste) gedrückt wurde, läuft das ohne eBus. Falls am BM-2 oder in der App gedrückt wurde, muss der Befehl
  in einem Telegramm stecken, das ebusd nicht als „unbekannt“ meldet (Kandidat: Inhalt von `0507`, aber unverändert).
- Uhr: Der Datetime-Broadcast des BM-2 ist wieder da (04:46:58 → `04:53:10`, also weiter +6 min). Die Therme sendet in
  ihrem Error-Broadcast `fe fe01` um 04:36:58 „04:37“ (= echte Zeit, in der Pause des BM-2-Broadcasts, nach dem
  `0f`-Zeittelegramm) und um 04:47:00 „04:53“ (= BM-2-Zeit) → Hypothese: Die Therme übernimmt die jeweils zuletzt
  gesendete Zeit; das `0f`-Zeittelegramm hat also die Therme gestellt, nicht das BM-2. Nicht verifiziert.

### Quittieren am BM-2, zweiter Versuch mit Rohmitschnitt (21.10.2026, 04:50:46–04:52, ebusd `raw` an)

Hinweis: `grab` speichert je Nachrichtenschlüssel nur den letzten Inhalt – einmalige Telegramme können darin untergehen;
deshalb hier `raw` (jedes Telegramm im Log).
- Birger drückt am BM-2 „Quittieren“ (keine Störung aktiv). ISM7-Blocklesung 04:51:36,6/37,6: Modulation 0x41 = 65 %,
  Ausgänge 6, Brennerstatus 7 = **Nachspülen**; ebusd-Poll 04:51:28,5 noch „Aus“ → Neustart des Feuerungsautomaten
  zwischen 04:51:28,5 und 04:51:36,6 (wie beim ersten Druck 04:47).
- Im Rohmitschnitt in diesem Fenster **kein neues Telegramm an `03`/`08`**: nur die zyklischen Lesungen, `0507` mit
  unverändertem Inhalt `09 00 03 50 00 00 80 ff 14 00`, `ff`-Lesungen TN 1. Einzige Auffälligkeit ab 04:51:32,8: das BM-2
  sendet `30 9x 5012` ohne Daten nacheinander an `90`, `91` … `97` (je 3–4 Wiederholungen, keine Antwort), dazu einzelne
  abgebrochene Bytes (`<30`, `<00`).
- Gegenprobe 04:52: `hex -s 30 90501200` von ebusd gesendet → keine Antwort, **kein** Nachspülen (Brennerstatus 2× „Aus“).
  Das `5012`-Telegramm ist also nicht der Quittierbefehl (es sieht nach einer Suche nach Teilnehmern aus).
- Deutung (nicht verifiziert): Das BM-2 sitzt in der Therme; laut BM-2-Anleitung (Kap. 15.3) geht das Quittieren nur
  „wenn das BM-2 im Heizgerät montiert ist“. Wahrscheinlich läuft der Befehl über die interne Verbindung BM-2 ↔ Regelplatine
  und nicht über den eBus. Dann ist Quittieren aus Home Assistant über den eBus nicht möglich.
- `raw`-Logging wieder ausgeschaltet.

### BM-2-Uhr am Gerät gestellt (21.10.2026, 04:52, Birger)

Direkt danach sendet das BM-2 außer der Reihe den Datetime-Broadcast (04:52:51 → `04:52:10`, sonst immer bei :58);
TN 10161 um 04:53:06 = 1076 = 04:52. Abweichung damit unter 1 min (Sekunden sendet das BM-2 immer als `10`).

### Uhr am BM-2 verstellen mit Rohmitschnitt (21.10.2026, 04:55, Birger: 1 min verstellt und zurück)

- Kein Telegramm, das die Zeit an ein anderes Gerät schreibt. Das BM-2 sendet nur außer der Reihe seinen Datetime-
  Broadcast (04:55:46 → `04:54:10`). → Die Uhr liegt im BM-2 selbst; Stellen am Gerät braucht den Bus nicht.
  Danach geht die BM-2-Uhr gut 1–2 min nach (04:56:15 echt, BM-2 04:54).
- Nebenbefund, genau ein 15-s-Zyklus nach dem Verstellen:
  - `30 03 0507` (Regler → Feuerungsautomat) 04:55:40 mit Inhalt `AA 03 9b 02 00 80 ff 14 00` (Rohbytes `a9 01` =
    eBUS-Escape für `AA`) statt sonst `00 03 50 00 00 80 ff 14 00`: Byte 1 `AA` statt `00`, Byte 3–4 `029b` = 667/16 =
    **41,7 °C** statt `0050` = 5,0 °C → kurzzeitige Wärmeanforderung (Deutung Byte 1 = Betriebszustand nach eBUS-Norm
    0507, `AA` = Heizbetrieb: nicht verifiziert). 15 s später wieder `00 … 50 00`.
  - Gleichzeitig `30 71 5023 05 a8 62 00 01 00` (Schreiben TN 98 = 1 an Adresse `71`, Prüfbyte korrekt, keine Antwort,
    4 Wiederholungen), 15 s später `f4 62 00 00 00` (TN 98 = 0). TN 98 und Adresse `71` nicht zugeordnet.
  - Brenner ist nicht gestartet (zu kurz). Vermutlich hat das Verstellen der Uhr das Zeitprogramm kurz neu bewertet.
- `raw` wieder aus.

### Schreibtest neue Parameter (21.10.2026, 05:15–05:18, Freigabe Birger)

Schreiben roh über `HgRaw` (Therme, Prüfbyte), `MmRaw` (MM, Prüfbyte), `BmRaw` (BM-2, Präfix `00`), Rücklesen mit `hex`.

| Parameter | TN | Original | Test | Rücklesen | zurück | Rücklesen |
|---|---|---|---|---|---|---|
| HG19 Nachlaufzeit SLP | 383 | 3 min | 4 (`8c 7f 01 04 00`) | 4 ✓ | 3 (`44 7f 01 03 00`) | 3 ✓ |
| HG20 max. Speicherladezeit | 384 | 120 min | 130 (`d8 80 01 82 00`) | 130 ✓ | 120 (`3c 80 01 78 00`) | 120 ✓ |
| HG41 Drehzahl ZHP WW | 10014 | 85 % | 86 (`84 1e 27 56 00`) | 86 ✓ | 85 (`60 1e 27 55 00`) | 85 ✓ |
| MI08 RL-Solltemperatur | 400 | 30,0 °C | 31,0 (`09 90 01 36 01`) | 31,0 ✓ | 30,0 (`59 90 01 2c 01`) | 30,0 ✓ |
| MI09 max. Speicherladezeit | 384 | 2 h | 3 (`74 80 01 03 00`) | 3 ✓ | 2 (`28 80 01 02 00`) | 2 ✓ |
| A15 Korrektur Außentemp. | 1443 | 0,0 K | 1,0 (`00 a3 05 0a 00`) | 1,0 ✓ | 0,0 (`00 a3 05 00 00`) | 0,0 ✓ |

Alle 6 beim ersten Versuch übernommen und zurückgestellt.

### Schreibtest Gruppe 1 (21.10.2026, 05:27–05:33, Freigabe Birger „Teste 1“)

| Parameter | Gerät/TN | Original | Test | Rücklesen | zurück |
|---|---|---|---|---|---|
| HG13 Funktion E1 | 08/2651 | 0 keine | 4 Zirkomat | 4 ✓ | 0 ✓ |
| HG14 Funktion A1 | 08/2751 | 1 Zirk. 100 % | 2 Zirk. 50 % | **6** (während HG13 = 4), allein getestet 2 ✓ | 1 ✓ |
| HG21 TK-min | 08/31 | 20,0 | 21,0 | 21,0 ✓ | 20,0 ✓ |
| A04 Außenfühler gemittelt | 35/388 | 3 h | 4 | 4 ✓ | 3 ✓ |
| A07 Antilegionellen-Tag | 35/257 | 5 Freitag | 6 | 6 ✓ | 5 ✓ |
| A08 Wartungsmeldung | 35/618 | 2 datumsabh. | 1 | 1 ✓ | 2 ✓ |
| A10 Parallelbetrieb | 35/35 | 0 Aus | 1 | 1 ✓ | 0 ✓ |
| A23 Startzeit ALF | 35/10141 | 3102 (12:30) | 3103 | 3103 ✓ | 3102 ✓ |
| A26 Freigabe Smarthome | 35/10912 | 1 Ein | 0 | 0 ✓ | 1 ✓ |
| Kreisart HK / MK | 35/9005, 86/9005 | 0 Heizkreis | 1 | 1 ✓ | 0 ✓ |
| Raumeinfluss HK / MK | 35/651, 86/651 | 0 Aus | 1 | 1 ✓ | 0 ✓ |

Befund: HG13 = 4 (Zirkomat) setzt den Ausgang A1 automatisch auf 6 (Zirkomat) und sperrt ihn – genau wie in der
CGB-2-Anleitung beschrieben (HG13 Zirkomat → A1 automatisch Zirkulationspumpe, für weitere Einstellungen gesperrt).
Reihenfolge beim Zurückstellen deshalb: erst HG13, dann HG14. Alle 15 Werte wieder auf Original, zurückgelesen.

### Fachmann-Menü mit Rohmitschnitt (21.10.2026, 05:32–05:35)

- Birger ruft am BM-2 Fachmann → Heizgerät die HG-Liste auf (HG21 20,0 / HG22 85,0 / **HG23 WW-Max 65,0** / HG25 15,0).
  Im Rohmitschnitt **keine** Lesetelegramme des BM-2 an `08` für diese Parameter (nur die zyklischen Statuslesungen) →
  das BM-2 im Heizgerät liest die HG-Parameter über die interne Verbindung, nicht über den eBus. Die Methode „am Display
  aufrufen und mitschneiden“ funktioniert für Therme-Parameter deshalb nicht.
- HG23 gefunden über Probelesen: **TN 308 am BM-2 (`35`) = `8a 02` = 650 → 65,0 °C** (TN 308 heißt in der Wolf-DB beim MM
  „Warmwassermaximaltemperatur“; an `08` liefert TN 308 `0080` = ungültig). Kandidat für HG23 bzw. A14 – Bestätigung durch
  Verstellen am Display steht aus.
- **HG43 ist keine Anzeige, sondern startet die „100% Kalibration“** (Anzeige „Kali abgesch. Aus / Kali. aktiv Aus /
  HG43: Warte… OK“). Birger gewarnt, nicht bestätigen. HG43–HG45 (Kalibrierung/Gas/Abgas) werden nicht weiter untersucht.

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
