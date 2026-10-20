# Fehlercodes Wolf CGB-2 (DTID 180000) und BM-2 (DTID 220000)

Quelle: `fault_messages.xml` aus der Wolf-Smartset-Parameterdatenbank (zivillian/ism7mqtt, src/ism7config/Resources).
Zuordnung Code -> Text, wie sie die Smartset-App anzeigt. Auf dem eBus ist der Übertragungsweg des Codes noch nicht beobachtet
(Kandidat: Broadcast `ControlCmd` PBSB 0802, Felder `device`/`error`; in der Wolf-Parameterdatenbank hat keines der Geräte CGB-2, BM-2, MM eine eigene Fehlerhistorie).


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
