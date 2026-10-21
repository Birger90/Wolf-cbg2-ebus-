# Fehlercodes Wolf CGB-2 (DTID 180000) und BM-2 (DTID 220000)

Quelle: `fault_messages.xml` aus der Wolf-Smartset-Parameterdatenbank (zivillian/ism7mqtt, src/ism7config/Resources).
Zuordnung Code -> Text, wie sie die Smartset-App anzeigt. Auf dem eBus ist der Übertragungsweg des Codes noch nicht beobachtet
Auf dem eBus: aktueller Störungscode = TN 1 (Lesen `5022` mit Prüfbyte `5c`, Antwort UIN), vom ISM7 alle 15 s an `08`, `35` und `52` abgefragt; beobachtet am 20.10.2026: BM-2 meldete 15 (Außenfühler) während „T außen“. ebusd: `fault.csv` (`FaultCode` in hc/bm2/mm). Eine Fehlerhistorie gibt es in keinem der Geräte (Wolf-Datenbank `device.xml`: `HasOwnFaultMessageHistory` = false für CGB-2, BM-2, MM); die Historie entsteht nur in der App bzw. in Home Assistant.


## CGB-2 (DTID 180000) - 58 Codes

| Code | Text |
|---|---|
| 1 | STB Übertemperatur |
| 2 | TB Übertemperatur |
| 3 | dt-eSTB-Drift |
| 4 | Keine Flammenbildung |
| 5 | Flammenausfall |
| 6 | Übertemperatur Vorlauf |
| 7 | Abgasfühler Übertemperatur |
| 8 | Abgasklappe schaltet nicht |
| 9 | Fehlercode unbekannt |
| 10 | eSTB Fühler defekt |
| 11 | Flammenvortäuschung |
| 12 | Kesselfühler defekt |
| 13 | Abgastemperaturfühler defekt |
| 14 | Speicherfühler defekt |
| 15 | Außenfühler defekt oder Wärmeerzeuger vom Netz getrennt |
| 16 | Rücklauffühler defekt |
| 18 | Externer Sicherheitskreis |
| 19 | Öldrucksensor defekt |
| 20 | Ventiltest fehlgeschlagen |
| 22 | Luftdruck |
| 23 | Luftdruck |
| 24 | Drehzahl nicht erreicht |
| 26 | Stillstand-Drehzahl nicht erreicht |
| 27 | Warmwasserauslauffühler defekt |
| 30 | Parameter CRC Fehler |
| 32 | 24V Überwachung |
| 35 | BCC nicht korrekt aufgesteckt |
| 36 | BCC defekt |
| 37 | BCC nicht kompatibel |
| 38 | Parametersatz des FA fehlerhaft |
| 39 | BCC Systemfehler |
| 40 | Fehler Strömung- /Druckerhöhungsprüfung |
| 41 | Strömungsüberwachung |
| 42 | Kondensatpumpe |
| 44 | Abgasdruckschalter |
| 52 | Max. Speicherladezeit |
| 53 | IO-Regelabweichung |
| 54 | SCOT Aktoren |
| 55 | SCOT Systemfehler |
| 56 | Kalibration Werksgrenze |
| 57 | Kalibration Abweichung |
| 58 | Kalibration Timeout |
| 59 | Kalibration Werksgrenze |
| 60 | Syphon verstopft |
| 66 | Öldruck zwei Mal nicht erreicht |
| 67 | Verhältnis Öldruck zu Pumpendrehzahl zwei Mal unplausibel |
| 78 | Sammlerfühler defekt |
| 83 | Öldruck erreicht Ruhewert nicht |
| 84 | Ölpumpe erreicht keinen Stillstand |
| 85 | Relaistest fehlgeschlagen |
| 86 | Zünddruck drei Mal nicht erreicht |
| 90 | Kommunikation zwischen Regelungsplatine und Feuerungsautomat gestört |
| 95 | Prog. Mode |
| 96 | Entriegelung |
| 98 | Flammenverstärker |
| 99 | Systemfehler |
| 107 | Druck Heizkreis |
| 116 | ESM (E1) |

## BM-2 (DTID 220000) - 3 Codes

| Code | Text |
|---|---|
| 15 | Außenfühler defekt oder Wärmeerzeuger vom Netz getrennt |
| 92 | BM2-System fehlt |
| 133 | Modul nicht kompatibel |

## MM (DTID 40000) - 7 Codes

| Code | Text |
|---|---|
| 52 | Max. Speicherladezeit |
| 70 | Defekter Mischerkreis-/Rücklauffühler |
| 71 | Defekter Speicher-, Puffer- oder Bypassfühler an E1 |
| 79 | Defekter Rücklauf- oder Bypassfühler (E2) |
| 81 | EEPROM Fehler |
| 91 | Bus-Adresse |
| 97 | Defekte Bypasspumpe |

## Abgleich mit der Anleitung CGB-2-14/20/24 (3063421_202106, Kap. 41/42; von Birger hochgeladen 21.10.2026)

- Störcodes: Die Anleitung bestätigt die Codes der Wolf-Datenbank (u. a. 01–05, 12–16, 20, 24, 26, **27 Warmwasserauslauffühler**,
  52–55, 90, 95, 96, 98, 99, 107, 116) und nennt zusätzlich **255 „Fehlercode unbekannt“** (in der Wolf-DB-Liste nicht enthalten).
  Die Codes 28 „Gasdruckwächter“ und 225 aus der Anleitung der CGB-2-68/75/100 (8616991_202111) stehen in der Anleitung
  der 24-kW-Therme nicht – sie gelten für unsere Therme nicht nachweislich.
- **Warnmeldungen** (Kap. 42, eigene Liste, müssen nicht quittiert werden): 1 Feuerungsautomat gewechselt, 2 Druck Heizkreis,
  3 Parameter ausgelesen (Werkseinstellung), 4 Keine Flammenbildung (beim letzten Startversuch), 5 Flammenausfall,
  24 Drehzahl Gebläse unter/über Grenze, 43 Viele Brennerstarts, 53 IO-Regelabweichung, 54 GLV Aktoren,
  55 GLV Systemfehler, 58 Kalibration Timeout, 68 GPV Offset, 69 Adaption nicht möglich.
  Die Nummern überschneiden sich mit Störcodes (4, 5, 24, 53–55, 58) → ein Code allein unterscheidet nicht zwischen Warnung
  und Störung. Ob und wie Warnungen über TN 1 übertragen werden, ist nicht beobachtet.
