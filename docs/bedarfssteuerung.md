# Bedarfssteuerung mit Durchflussmesser (Waveshare ESP32-S3-Relay-6CH)

Firmware: [`esphome/heizung-bedarf.yaml`](../esphome/heizung-bedarf.yaml) (ESPHome, geprüft mit 2026.10.1).

## Idee

Die Wolf-Regelung weiß nicht, ob irgendein Heizkörperventil Wärme abnimmt. Ohne Bypass taktet die Therme deshalb
gegen geschlossene Ventile. Der ESP misst den Durchfluss im Heizkörperkreis und sperrt die Heizung über den Eingang
**E1 der Therme** (HG13 = 1 „Raumthermostat“: E1 offen = Heizbetrieb gesperrt), solange niemand Wärme braucht.
Im gesperrten Zustand lässt er regelmäßig die Heizkreispumpe kurz laufen und prüft, ob wieder Wasser fließt.

Fußbodenheizung und Heizkörper sind laut Betreiber immer gemeinsam offen, deshalb genügt ein Durchflussmesser im
Heizkörperkreis. Die Regelung läuft vollständig verdrahtet auf dem ESP. Home Assistant stellt nur Werte ein und zeigt an.

## Test 28.10.2026 (HG13 = 1, E1 offen, 21:15–21:22)

| Zeit | Therme | Pumpe Therme | MM A1 (Heizkörper) | MM MKP |
|---|---|---|---|---|
| 21:15 vorher | Heizbetrieb | 65 % | Ein | Aus |
| 21:16 | Nachlauf Heizkreispumpe, Brenner aus | 65 % | Ein | Aus |
| 21:18 | Standby | 0 % | Ein | Aus |
| 21:22:30 | Standby | 0 % | Aus (nach MM-Nachlauf 5 min) | Aus |
| 21:24 (HG13 = 0) | Heizbetrieb, Zünden | 65 % | Ein | Aus |

Folge: Bei gesperrter Heizung schaltet auch das MM die Heizkreispumpe ab. Für den Prüflauf ist deshalb ein Relais
an der Pumpe nötig. MKP war schon vorher aus; ihr Verhalten bei E1 offen ist nicht beobachtet.

## Verdrahtung

| Waveshare | Anschluss | Bemerkung |
|---|---|---|
| CH1 (GPIO1) COM + **NC** | Therme Klemme E1 | Relais stromlos = E1 geschlossen = Heizung frei. Freies Adernpaar im Cat-Kabel Therme–MM. Keine Fremdspannung an E1 (Wolf-Montageanleitung S. 29). |
| CH2 (GPIO2) COM | Heizkreispumpe L | Relais stromlos: NC → MM-Ausgang A1 (MM steuert wie bisher). Angezogen: NO → Dauer-L (Prüflauf). 230 V: Elektriker. |
| RS485 A/B | TUF-2000 (Adr. 1) und PTA8C04 (Adr. 2) | 9600 8N1, 120-Ω-Abschluss per Jumper H3 am Waveshare. Richtungsumschaltung automatisch. |
| GPIO4 (Stiftleiste H1 Pin 15) + GND | 230-V-Optokoppler-Modul am MM-Ausgang A1 | „Wolf will Heizkreispumpe“. Polarität am Modul prüfen (`inverted` in der YAML). |
| DC 7–36 V | 24-V-Netzteil | |

CH5/CH6 (GPIO45/46) sind Strapping-Pins und werden nicht benutzt.

## Ablauf in der Firmware

1. **Frei:** Läuft die Wolf-Pumpe und liegt der Durchfluss länger als *Sperren nach* unter der *Schwelle*, und ist es
   draußen wärmer als *Nicht sperren unter Außentemperatur*, wird gesperrt (CH1 zieht an).
2. **Gesperrt:** Alle *Prüfintervall* Minuten Prüflauf.
3. **Prüflauf:** CH2 zieht an, Pumpe läuft *Prüflauf Dauer* Sekunden. Höchster Durchfluss ≥ *Schwelle* → frei,
   sonst weiter gesperrt.
4. Nach jeder Freigabe bleibt die Heizung mindestens *Mindestdauer frei* frei.

Sicherungen (jeweils sofort frei):
- Höchstdauer Sperre erreicht
- Außentemperatur zu niedrig oder seit 3 h kein Wert aus Home Assistant
- Durchflussmesser liefert keinen Wert
- Taster „Heizung sofort freigeben“
- Modus „Aus“ oder „Beobachten“: Relais immer abgefallen
- ESP stromlos/abgestürzt: Relais fallen ab → Heizung wie ohne ESP

**Beobachten** (Werkseinstellung der Firmware): schaltet nichts, simuliert aber Sperren und Freigaben. Die
Entitäten „Heizung gesperrt“ und „Sperrzeit gesamt“ zeigen, wie oft und wie lange gesperrt worden wäre.

## Inbetriebnahme

1. TUF-2000 einstellen: Rohrdaten, Nullpunkt (M42) bei stehendem Wasser, M46 = 1, M62 = 9600/none/8/1,
   M63 = MODBUS-RTU. Koppelpaste, Signalqualität am Display prüfen.
2. PTA8C04 allein an RS485, Taster „PTA8C04 Adresse 1 auf 2 setzen“ drücken, danach TUF anschließen.
3. **TUF Registervariante:** Die Kandidaten A–D mit dem Display des TUF vergleichen und die passende Variante
   auswählen. Registeradresse (0- oder 1-basiert) und Wortreihenfolge sind nicht verifiziert.
4. Mit Modus „Beobachten“ messen: Durchfluss bei „alle Ventile zu“ und bei „ein Ventil auf“. Daraus *Schwelle*,
   *Sperren nach* und *Prüflauf Dauer* festlegen.
5. Erst dann E1 anschließen (Relais NC), **danach** HG13 = 1 an der Therme schreiben (vorher ist E1 offen und die
   Heizung wäre sofort gesperrt), Modus „Automatisch“.

## Nicht verifiziert

- TUF-2000: Registeradresse, Wortreihenfolge, Lage der Signalqualität (Register 92, Low-Byte laut Handbuch der
  TDS-100M-Familie), Werkseinstellungen des konkreten Geräts.
- Alle Startwerte der Einstellungen (in der YAML als BEISPIEL markiert).
- Polarität des 230-V-Optokoppler-Moduls.
- Verhalten der MKP bei E1 offen.
- Flash-Größe des Waveshare-Moduls (4 MB angenommen = kleinste Variante).
