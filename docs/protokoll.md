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
  Hypothese: `f0` ist ein zweites BM-2-artiges Bediengerät (z. B. das BM-2 bzw. Bedienmodul des Mischerkreises).
  Nicht verifiziert.
- Einmalige ISM7-Abfragen (wohl beim Verbindungsaufbau der Wolf-App), Antworten gegen die Wolf-Datenbank geprüft:

| Adresse | TN | Wolf-DB-Name | Rohwert | Deutung |
|---|---|---|---|---|
| `08` | 10878 | Herstelljahr | `0x13` = 19 | vermutlich 2019 (Jahreszahl ohne Jahrhundert, nicht verifiziert) |
| `08` | 10877 | Herstellwoche | `0x2c` = 44 | KW 44 |
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
