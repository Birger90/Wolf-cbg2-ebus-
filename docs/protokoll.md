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
| 19.10. 23:05 | BM-2: Programmwahl DHK TN 10100 = 2 (`d4 7427 0200`) | 31 | HkProgram → Permanent, Heizkreis Heizbetrieb, Brenner an |
| 20.10. 06:00 | BM-2: TN 10100 = 1 (`30 7427 0100`) | 31 | HkProgram → Auto |

## Parametertest 20.10.2026 (script.heizung_parametertest)

Jeder schreibbare Parameter: lesen, Wert+1 schreiben, zurücklesen, Originalwert schreiben, zurücklesen.
Therme über `HgRaw` mit berechnetem Prüfbyte, BM-2/MK über die statischen Nachrichten (Präfix `00`).

| Gerät | Parameter | Ergebnis |
|---|---|---|
| Therme (03) | HG01, HG04, HG07, HG08, HG09, HG15, HG16, HG17, HG22, HG25, HG33, HG38, HG39, HG60 | alle 14: Schreiben OK, Rücksetzen OK (HG07/HG09 je ein Wiederholversuch) |
| BM-2 (35) | WwSoll, WwMin, HkDaytemp, HkCurveBasetemp, HkCurveStart, HkCurveNormoutside, HkCurveFlowtemp, HkSetpointcorr, HkWintersummer, HkEcoabs | Test läuft (20.10. 06:33), Ergebnis folgt |
| MK (86) | MkDaytemp, MkCurveBasetemp, MkCurveStart, MkCurveNormoutside, MkCurveFlowtemp, MkSetpointcorr, MkWintersummer, MkEcoabs | Test läuft, Ergebnis folgt |

Nicht getestet (absichtlich): Programmwahl (nur der einmalige Notfall-Schreibvorgang oben), 1x Warmwasser (löst eine
Speicherladung aus), HG02/HG03/HG12 (Gas), HG21/HG62 (liefern `unknown`).

## Weitere Telegrammnummern

- TN 5250 (BM-2): Wartung Fälligkeitsdatum, Typ BM2Date (ism7mqtt `BM2DateConverterTemplate`):
  Tag = (v & 31) + 1, Monat = ((v >> 5) & 15) + 1, Jahr = 2000 + (v >> 9). Gelesen 13096 → 09.10.2025, identisch mit der Cloud.

## Offen / nicht verifiziert

- Warum die 9-Byte-Form des ISM7 von ebusd aus nicht angenommen wird.
- Bedeutung des Anhangs TN 349 = 0 (ISM7) bzw. TN 413 = 0 (offizielles ebusd-Format für die Therme).
- Ob der Mischerkreis (`86`) das Prüfbyte prüft: die statischen Zeilen mit Präfix `00` werden im Parametertest geprüft.

## Geräteerkennung (ebusd-Scan)

- `08`: Kromschröder, Ident ` !`, SW 2002, HW 0000
- `35`: Wolf, SW 0204, HW 0100
- `52`: Kromschröder, SW 0100
- `86`, `04`, `14`, `f6`: antworten nicht auf die Identifikationsanfrage
