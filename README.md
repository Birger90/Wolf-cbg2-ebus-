# Wolf CGB-2 am eBus mit ebusd und Home Assistant

Lokaler Lese- **und Schreibzugriff** auf eine Wolf-Gasbrennwerttherme CGB-2-24 mit Bedienmodul BM-2, Mischermodul MM
und Funk-Außenfühler über den eBus, ohne Wolf-Cloud. Stand 21.10.2026, alles an einer realen Anlage verifiziert (Werte
gegen die Wolf-Cloud und das BM-2-Display verglichen, jeder Schreibweg mit Rücklesen und Zurückstellen getestet).

```
Therme CGB-2-24   ──┐
BM-2 (Regler)     ──┤
MM (Mischer)      ──┤ eBus ── eBUS Adapter Shield C5 (ESP32-C5, WLAN) ── ebusd (HA-App) ── MQTT ── Home Assistant
Funkempfänger 0f  ──┤
ISM7 (noch)       ──┘
```

## Stand in einem Satz

Alle für Betrieb und Optimierung relevanten Parameter von Therme, BM-2, Heizkreisen und Mischermodul sind lesbar und
schreibbar; Störungscodes werden gelesen und im Klartext ausgegeben. Nicht über den eBus möglich: Störung quittieren,
BM-2-Uhr stellen, Störungshistorie lesen (Details unten und in `docs/protokoll.md`).

## Was im Repo liegt

| Pfad | Inhalt |
|---|---|
| `ebusd-config/*.csv` | Nachrichtendefinitionen für ebusd (Therme, BM-2, Mischerkreis, Mischermodul, Broadcast) |
| `ebusd-config/mqtt-hassio.cfg` | ebusd-MQTT-Integration für Home Assistant (angepasste Filter, alle Werte, schreibbare Nachrichten) |
| `tools/wolf_crc.py` | Prüfbyte-Berechnung des Wolf-Protokolls, Selbsttest gegen 30 mitgeschnittene Telegramme |
| `tools/gen_ebusd_config.py` | Generator, der die CSV-Dateien aus Tabellen erzeugt (Telegrammnummern aus der Wolf-Parameterdatenbank) |
| `docs/protokoll.md` | Protokolldetails, Busadressen, Tests und Mitschnitte mit Belegen, was geht und was nicht |
| `docs/fehlercodes-cgb2.md` | Störungs- und Warncodes CGB-2/BM-2/MM mit Abgleich gegen die Wolf-Anleitungen |
| `docs/ha-helfer.md` | Alle Home-Assistant-Helfer, Skripte und Automationen (Heizung und Kabine) mit Entitätsnamen |
| `homeassistant/gen_scripts.py` | Erzeugt die HA-Skripte `heizung_therme_schreiben` (Prüfbyte in Jinja) und `heizung_parametertest` als JSON |
| `homeassistant/script_*.json` | Die erzeugten Skripte, per API/UI in Home Assistant anlegbar |

## Hardware

- Wolf CGB-2-24 (Feuerungsautomat von Kromschröder), Software laut eBus-Scan 2002
- Wolf BM-2, Software 02.04, sitzt in der Therme
- Wolf MM (Mischermodul, Kromschröder), Konfiguration MI05 = 3 „Mischerkreis und direkter Heizkreis“
- Wolf Funk-Außenfühler mit Funkempfänger (DCF77-Funkuhr), Master `0f`
- [eBUS Adapter Shield C5](https://adapter.ebusd.eu/v5-c5/) am eBus-Anschluss der Therme, Betrieb über WLAN (`ens:IP:9999`)
- Home Assistant OS auf Raspberry Pi mit der App [eBUSd von LukasGrebe](https://github.com/LukasGrebe/ha-addons) (ebusd 26.1) und Mosquitto

## Busadressen dieser Anlage

| Adresse | Gerät | Inhalt |
|---|---|---|
| `08` (Master `03`) | Therme | Temperaturen, Druck, Brennerstatus, Zähler, HG-Parameter |
| `35` (Master `30`) | BM-2 | Systemparameter (A-Parameter), direkter Heizkreis, Warmwasser, Uhr, Party/Urlaub, Wartung |
| `52` | Mischermodul MM | Mischer-Vorlauf, Mischersoll, Pumpe, MI-Parameter; Schreiben über `MmRaw` mit Prüfbyte an `52` |
| `86` | Mischerkreis (MK) | Programmwahl, Heizkurve, Tagtemperatur des Mischerkreises |
| `0f` | Funkempfänger Außenfühler | sendet jede Minute die Außentemperatur; Zeit/Datum sendet er als ungültig (DCF vermutlich nicht synchron) |
| `ff` / `04` | ISM7 (Master / Slave) | liest alles zyklisch; Slave = Master + 5 |
| `f0`, `f1` | unbekannte Master | senden `RcTarget`- bzw. `0503`-Broadcasts und lesen das MM; Gerät offen |

Verifiziert über Vorlauftemperaturen: `35`/TN 10119 = Vorlauf direkter Heizkreis, `86`/TN 10119 = `52`/TN 15 = Mischer-Vorlauf,
jeweils identisch mit der Wolf-Cloud.

## Protokoll in Kürze

Lesen (PBSB `5022`): `ZZ 50 22 03 <Prüfbyte> <TN lo> <TN hi>` → Antwort `02 <Wert lo> <Wert hi>` (`0080` = ungültig)
Schreiben (PBSB `5023`): `ZZ 50 23 05 <Prüfbyte> <TN lo> <TN hi> <Wert lo> <Wert hi>`

TN = Telegrammnummer aus der Wolf-Parameterdatenbank (identisch mit den Nummern im ISM7-Protokoll, siehe
[zivillian/ism7mqtt](https://github.com/zivillian/ism7mqtt)). Werte sind 16 Bit little endian, bei Temperaturen ×10.

**Prüfbyte** = CRC8 über alle folgenden Bytes, Polynom `0x5C`, Startwert `0x00`, pro Byte `c = shift8(c) XOR byte`.
Entschlüsselt aus neun ISM7-Schreibtelegrammen und an allen 30 Mitschnitten bestätigt, siehe `tools/wolf_crc.py --verify`.
Unabhängig davon beschreibt [dktzde/ebusd-configuration-wolf](https://github.com/dktzde/ebusd-configuration-wolf)
dieselbe Formel.

### Schreibwege (alle getestet)

| Ziel | Weg | Prüfbyte |
|---|---|---|
| Therme `08` | 5 Byte an **Master** `03`, MQTT `ebusd/hc/HgRaw/set` = `"crc tnlo tnhi vlo vhi"` | wird geprüft (mit `00` kein Effekt) |
| Mischermodul `52` | 5 Byte an `52`, `ebusd/mm/MmRaw/set` | CRC, quittiert |
| BM-2 `35` | 5 Byte an **Slave** `35`, `ebusd/bm2/BmRaw/set` = `"00 tnlo tnhi vlo vhi"` | wird nicht geprüft |
| Mischerkreis `86` | `ebusd/mk/MkRaw/set`, Präfix `00` | wird nicht geprüft |

- Das ISM7 schreibt 9 Byte an die Master-Adresse `30` mit Anhang; diese Form nimmt das BM-2 von ebusd nicht an. Hinweis
  auf die 5-Byte-Form von *audaciousengineer* in [ebusd Discussion #779](https://github.com/john30/ebusd/discussions/779).
- ebusd meldet beim BM-2 immer `ERR: read timeout`, weil keine Antwortdaten kommen
  ([ebusd Issue #1696](https://github.com/john30/ebusd/issues/1696)). Erfolg nur durch Zurücklesen prüfen.
- Das offizielle ebusd-Format für die Therme (9 Byte an `03` mit Anhang `9d010000`) nimmt die CGB-2 nicht an.

## Parameterabdeckung (21.10.2026)

Lesen und Schreiben getestet (geändert, zurückgelesen, zurückgestellt):
- **Therme:** HG01–HG04, HG07–HG09, HG13–HG17, HG19–HG22, HG25, HG33, HG38, HG39, HG41, HG60.
  HG13 = Zirkomat setzt und sperrt HG14 (A1) – erst HG13, dann HG14 schreiben.
  HG23 WW-Maximum = TN 385: Zuordnung am Display bestätigt (64 ↔ 65), Schreiben über den Bus noch nicht getestet.
- **Mischermodul:** MI08 RL-Soll (TN 400), MI09 max. Speicherladezeit (TN 384), TV-min/-max, Heizkurvenabstand,
  Nachlaufzeit, P-Bereich.
- **BM-2 / Heizkreise:** Bedienparameter und Heizkurven (Parametertest 20.10.2026), Programmwahl (0 Standby, 1 Auto, 2 Permanent, 3 Sparen),
  Party, Urlaub, 1× Warmwasser, A04 (TN 388), A07 (TN 257), A08 (TN 618), A09 Frostschutzgrenze (TN 2560), A10 (TN 35),
  A15 Korrektur Außentemperatur (TN 1443), A23 (TN 10141), A26 (TN 10912), Kreisart (TN 9005), Raumeinfluss (TN 651),
  Wartungsdatum (TN 5250/5264).

Bewusst gesperrt bzw. ohne Regler: HG10 (eBus-Adresse), HG12 (Gasart), MI10/Busspeisung (`EbusPower`); keine Regler für
HG34 und HG40. HG43–HG45 nicht angefasst – **HG43 am Display startet eine 100-%-Kalibrierung**.

Offen / nicht verifiziert:
- A14 (WW-Maximum am BM-2): Telegrammnummer unbekannt, wird nicht verteilt.
- HG40: Rohwert 1, laut Wolf-DB „02“ (passt zu MI05 = 3), am Display nicht abgelesen.
- MI17 ↔ TN 45 (liest 15,0, Werk 10 K) und HG61 ↔ TN 10017: Zuordnung nicht verifiziert.
- Raumregler-Parameter A00, A05, A16–A18 lesbar, wirken ohne Raumfühler am BM-2 nicht.

Nicht über den eBus möglich (getestet, `docs/protokoll.md`):
- **Störung quittieren:** läuft intern BM-2 ↔ Regelplatine, kein eBus-Telegramm.
- **BM-2-Uhr stellen:** Schreiben auf TN 10161/10160 und Zeit-Broadcasts von `0f`/`30` wirkungslos; die Uhr liegt im BM-2.
- **Störungshistorie** (bis 40 Einträge im Fachmann-Menü): keine Telegrammnummer bekannt.
- HG-Parameter liest das BM-2 intern, nicht über den eBus – Mitschneiden am Display hilft für Therme-Parameter nicht.

## Installation in Home Assistant

1. ebusd-App installieren, Adapter als `network_device` = `ens:<IP>:9999` eintragen.
2. Dateien aus `ebusd-config/` nach `/app_configs/<slug>_ebusd/ebusd-config/` kopieren (z. B. mit dem File editor
   oder Samba; in der App heißt der Ordner `/config/ebusd-config`), `mqtt-hassio.cfg` nach `/app_configs/<slug>_ebusd/`.
3. App-Optionen, `commandline_options`:
   ```
   --configpath=/config/ebusd-config
   --pollinterval=2
   --httpport=8889
   --enabledefine
   ```
   (kein `--scanconfig`, die Dateien im Ordner werden alle geladen; `seed_mqtt_cfg` bleibt an, die vorhandene cfg wird genutzt)
4. App neu starten und im Log die Zahl der geladenen Nachrichten prüfen (`found messages: …`).
5. Home Assistant legt per MQTT-Discovery die Entitäten an: `sensor.heating_ebusd_<circuit>_<name>`, schreibbare
   BM-2/MK-Werte als `number.…`/`select.…`. HG-Parameter der Therme werden über `script.heizung_therme_schreiben`
   geschrieben (Felder: name, tn, wert, teiler, minimum, maximum).
6. Skripte aus `homeassistant/` anlegen (`python3 homeassistant/gen_scripts.py`, JSON per HA-API oder von Hand im Editor).

Die Therme wird vom BM-2 ohnehin alle ~65 s abgefragt; da die IDs in `hc.csv` dem Format des BM-2 entsprechen
(Präfix `cc`), liest ebusd diese Antworten passiv mit.

## Home-Assistant-Bausteine

Vollständige Liste mit Entitätsnamen in `docs/ha-helfer.md`. Überblick:
- **Bedienung Heizung** (Dashboard „Heizung“, `heizung-wolf`, nur eBus-Entitäten): Schieberegler für die HG-Parameter
  (`number.therme_*`), Programmwahl der drei Kreise (`select.heizung_programm_*`), Mischermodul-Regler, Partymodus-Skript.
- **Überwachung:** Störungscode von Therme/BM-2/MM mit Klartext und Push, Anlagendruck, Datenausfall, Außentemperatur fehlt
  (ohne Außentemperatur gehen beide Kreise in AT-Frostschutz, Vorfall 20.10.2026), Wartung fällig, BM-2-Uhrabweichung.
- **Schreib-Skripte:** `heizung_therme_schreiben` (Therme und MM, Prüfbyte), `heizung_ebus_schreiben` (BM-2/MK, Rücklesen,
  bis 3 Versuche), `heizung_parametertest`, `heizung_partymodus`.
- **Kabine (Gewerbeeinheit, 21.10.2026):** Vorheizen nach Buchungskalender, Geräte vor/nach Buchungen, Anwesenheitsmodus
  über iPhone-Ortung, Oberlicht-Lüftung gegen Muff (Taupunktvergleich, Regenschutz, Handbetrieb), Dashboard
  „Kabine“ (`kabine-steuerung`). Die Wolf-Kreise werden dabei nur auf Permanent gestellt, wenn die Kabine kälter als die
  Komforttemperatur ist; Permanent wirkt auf den ganzen Kreis (auch die Mieterwohnung).

## Optimierung („Vorschlagen“ / „Automatisch“)

Grundlage: Wolf CGB-2 Montageanleitung 3063421 (Kap. 22/23 HG-Parameter, Kap. 33 Pumpe, Warnung 43) und die Auswertung
vom 19.10.2026: tagsüber endete fast jeder Brennerlauf mit „Spreizung KF“ → „Gradientenüberwachung“ (laut Anleitung zu
wenig Durchfluss), Neustart nach der Taktsperre.

- `automation.heizung_optimierung_auswerten`, täglich 07:30: wertet den Vortag aus (Brennerstarts, Laufzeit,
  Schutzabschaltungen Spreizung/Gradient), höchstens ein Vorschlag, frühestens 24 h nach der letzten Änderung.
  Regeln in Reihenfolge: Starts > 40 und Schutzabschaltungen > 30 %: HG16 +10 (max 65) → HG39 = 3 → HG04 −8 (min 70);
  Starts > 40: HG09 +3 (max 15).
- Modus `input_select.heizung_optimierung_modus`: Nur überwachen, Vorschlagen (Push mit Übernehmen/Ablehnen), Automatisch.
- Bisher übernommen: 20.10.2026 HG16 45 → 55.
- Nie angefasst: Heizkurven, Programmwahl, Warmwasser, Gas-/Abgasparameter (HG02, HG03, HG12, HG43–HG45).

## Sicherheitsregeln

- Programmwahl beider Heizkreise ist schreibbar; die Mieterwohnung hängt an beiden Kreisen, also mit Bedacht.
- Gesperrt bleiben HG10, HG12 und die Busspeisung des MM. HG02/HG03 (Brennerleistung) sind schreibbar.
- Jeder Schreibvorgang wird zurückgelesen und bei Bedarf wiederholt.
- HG43 am BM-2-Display nicht aufrufen und bestätigen (startet Kalibrierung).

## Quellen

- [ebusd](https://github.com/john30/ebusd), [ebusd-configuration](https://github.com/john30/ebusd-configuration) (kromschroeder/08..hc.csv, 50..mc.csv, broadcast.csv)
- [zivillian/ism7mqtt](https://github.com/zivillian/ism7mqtt) (Wolf-Parameterdatenbank: parameter.xml, converter.xml, device.xml)
- [dktzde/ebusd-configuration-wolf](https://github.com/dktzde/ebusd-configuration-wolf) (CRC8-Beschreibung)
- Wolf CGB-2(K) Montageanleitung für den Fachhandwerker, Art.-Nr. 3063421 (Ausgaben 2015 und 2021/2024)
- Wolf BM-2 Betriebsanleitung für die Fachkraft ab FW 2.80 (3063305_201910), BM-2 Montageanleitung Experte, MM/MM-2 Montageanleitung
- Wolf Funk-Außenfühler/Funkempfänger, Anleitung 3060938_1007
- [ebusd Issue #1696](https://github.com/john30/ebusd/issues/1696), [Discussion #779](https://github.com/john30/ebusd/discussions/779)
