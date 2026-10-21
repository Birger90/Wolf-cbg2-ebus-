# Wolf CGB-2 · eBus · Home Assistant

Lokale Steuerung einer **Wolf-Gasbrennwerttherme CGB-2-24** mit Bedienmodul **BM-2**, Mischermodul **MM** und
Funk-Außenfühler über den **eBus** – lesen *und schreiben*, ohne Wolf-Cloud, mit [ebusd](https://github.com/john30/ebusd)
und Home Assistant.

Alles hier ist an einer realen Anlage erprobt: Werte gegen Wolf-Cloud und BM-2-Display verglichen, jeder Schreibweg
mit Rücklesen und Zurückstellen getestet. Belege, Mitschnitte und Fehlversuche stehen in [`docs/protokoll.md`](docs/protokoll.md).
Stand: 21.10.2026.

```
Therme CGB-2-24   ──┐
BM-2 (Regler)     ──┤
Mischermodul MM   ──┤ eBus ── eBUS Adapter Shield C5 ── WLAN ── ebusd (HA-App) ── MQTT ── Home Assistant
Funkempfänger     ──┤
ISM7 (optional)   ──┘
```

---

## Inhalt

1. [Was geht – was nicht](#was-geht--was-nicht)
2. [Hardware](#hardware)
3. [Busteilnehmer](#busteilnehmer)
4. [Installation](#installation)
5. [Protokoll](#protokoll)
6. [Parameterabdeckung](#parameterabdeckung)
7. [Home Assistant](#home-assistant)
8. [Sicherheitsregeln](#sicherheitsregeln)
9. [Repo-Struktur](#repo-struktur)
10. [Offene Punkte](#offene-punkte)
11. [Quellen und Dank](#quellen-und-dank)

---

## Was geht – was nicht

| Funktion | Stand |
|---|---|
| Temperaturen, Druck, Brennerstatus, Zähler, Modulation lesen | ✅ |
| HG-Parameter der Therme schreiben | ✅ (Prüfbyte nötig) |
| Mischermodul-Parameter (MI) schreiben | ✅ |
| BM-2: Heizkurven, Programmwahl, Party, Urlaub, A-Parameter, Wartungsdatum | ✅ |
| Aktueller Störungscode von Therme, BM-2, MM mit Klartext | ✅ |
| Außentemperatur, BM-2-Uhr, BM-2-Status aus Broadcasts | ✅ |
| Störung quittieren | ❌ läuft intern BM-2 ↔ Regelplatine, kein eBus-Telegramm |
| BM-2-Uhr stellen | ❌ Uhr liegt im BM-2, alle Schreibversuche wirkungslos |
| Störungshistorie des BM-2 (40 Einträge) | ❌ Telegrammnummer unbekannt |
| HG-Parameter durch Mitschneiden am Display finden | ❌ das BM-2 liest sie intern, nicht über den eBus |

## Hardware

| Gerät | Details |
|---|---|
| Wolf CGB-2-24 | Feuerungsautomat Kromschröder, eBus-Kennung SW 2002 |
| Wolf BM-2 | SW 02.04, sitzt in der Therme |
| Wolf Mischermodul MM | Kromschröder SW 0100, MI05 = 3 „Mischerkreis und direkter Heizkreis“ |
| Wolf Funk-Außenfühler + Funkempfänger | Empfänger mit DCF77-Funkuhr, sendet als Master `0f` |
| Wolf ISM7 / Link home | optional, für den Betrieb dieses Repos nicht nötig |

### Bus-Adapter

- **[eBUS Adapter Shield C5](https://adapter.ebusd.eu/v5-c5/)** (ESP32-C5), angeschlossen am eBus-Anschluss der Therme.
- Betrieb über **WLAN**, ebusd verbindet sich per TCP im Enhanced-Protokoll: `--device=ens:<IP>:9999`.
- Firmware laut ebusd: `1.1[6911]`. Beobachtet: Symbolrate 57/s (max. 215), Arbitrierung 3–141 µs,
  0 Neuverbindungen seit dem letzten Start.
- ebusd sendet über den Adapter als Master `31` (Slave `36`); alle Schreibtests liefen über diesen Weg.

### Software

- Home Assistant OS mit der App [eBUSd von LukasGrebe](https://github.com/LukasGrebe/ha-addons), ebusd 26.1
- Mosquitto als MQTT-Broker

## Busteilnehmer

Ausgabe von ebusd `info` und eigene Mitschnitte:

| Adresse | Gerät | Inhalt |
|---|---|---|
| `08` (Master `03`) | Therme | Temperaturen, Druck, Brennerstatus, Zähler, HG-Parameter |
| `35` (Master `30`) | BM-2 | A-Parameter, direkter Heizkreis, Warmwasser, Uhr, Party/Urlaub, Wartung |
| `86` | Mischerkreis (MK) | Programmwahl, Heizkurve, Tagtemperatur des Mischerkreises |
| `52` | Mischermodul MM | Mischer-Vorlauf und -Soll, Pumpe, MI-Parameter |
| `0f` | Funkempfänger | Außentemperatur jede Minute; Zeit/Datum sendet er als ungültig (DCF vermutlich nicht synchron) |
| `ff` / `04` | ISM7 | liest alles zyklisch (Slave `04` = Master + 5) |
| `31` / `36` | ebusd über den Adapter | |
| `f0` / `f5`, `f1` | unbekannt | `f5` meldet sich als Kromschröder SW 0100 wie das MM; Zuordnung nicht verifiziert |

## Installation

1. ebusd-App installieren, als Gerät `ens:<IP-des-Adapters>:9999` eintragen.
2. Dateien aus `ebusd-config/` nach `/app_configs/<slug>_ebusd/ebusd-config/` kopieren (File editor oder Samba), dazu
   `mqtt-hassio.cfg` nach `/app_configs/<slug>_ebusd/`.
3. App-Optionen, `commandline_options`:
   ```
   --configpath=/config/ebusd-config
   --pollinterval=2
   --httpport=8889
   --enabledefine
   ```
   Kein `--scanconfig` – alle Dateien im Ordner werden geladen.
4. App neu starten, im Log die Zahl der geladenen Nachrichten prüfen (`found messages: …`).
5. Home Assistant legt die Entitäten per MQTT-Discovery an (`sensor.heating_ebusd_<kreis>_<name>`, schreibbare
   BM-2/MK-Werte als `number`/`select`).
6. Skripte aus `homeassistant/` anlegen (`python3 homeassistant/gen_scripts.py` erzeugt die JSON-Dateien), dazu
   `configuration_shell_command.yaml` für Rohbefehle über den ebusd-Kommandoport (Feld `cmd`).

Die Therme wird vom BM-2 ohnehin alle ~65 s abgefragt. Weil die IDs in `hc.csv` dem Format des BM-2 entsprechen,
liest ebusd diese Antworten passiv mit; dasselbe gilt für die ISM7-Abfragen von BM-2, MK und MM.

## Protokoll

```
Lesen      ZZ 50 22 03 <Prüfbyte> <TN lo> <TN hi>                    → 02 <Wert lo> <Wert hi>   (0080 = ungültig)
Schreiben  ZZ 50 23 05 <Prüfbyte> <TN lo> <TN hi> <Wert lo> <Wert hi>
```

- **TN** = Telegrammnummer aus der Wolf-Parameterdatenbank (dieselben Nummern wie im ISM7-Protokoll, siehe
  [zivillian/ism7mqtt](https://github.com/zivillian/ism7mqtt)). Werte 16 Bit little endian, Temperaturen ×10.
- **Prüfbyte** = CRC8 über die folgenden Bytes, Polynom `0x5C`, Start `0x00`. Selbsttest gegen 30 Mitschnitte:
  `python3 tools/wolf_crc.py --verify`.
- Die Geräte antworten auch auf unbekannte TNs (meist mit 0) – eine Antwort beweist nicht, dass es den Parameter gibt.

### Schreibwege

| Ziel | Weg | Prüfbyte |
|---|---|---|
| Therme `08` | 5 Byte an **Master** `03`, MQTT `ebusd/hc/HgRaw/set` = `"crc tnlo tnhi vlo vhi"` | wird geprüft, sonst kein Effekt |
| Mischermodul `52` | 5 Byte an `52`, `ebusd/mm/MmRaw/set` | CRC, wird quittiert |
| BM-2 `35` | 5 Byte an **Slave** `35`, `ebusd/bm2/BmRaw/set` = `"00 tnlo tnhi vlo vhi"` | wird nicht geprüft |
| Mischerkreis `86` | `ebusd/mk/MkRaw/set`, Präfix `00` | wird nicht geprüft |

- ebusd meldet beim BM-2 immer `ERR: read timeout`, weil keine Antwortdaten kommen
  ([ebusd #1696](https://github.com/john30/ebusd/issues/1696)) – Erfolg nur per Rücklesen prüfen.
- Das 9-Byte-Format des ISM7 (an Master `30` bzw. `03`, mit Anhang) nehmen BM-2 und Therme von ebusd nicht an.
- Programmwahl: `0` Standby, `1` Auto, `2` Permanent, `3` Sparen.

## Parameterabdeckung

**Lesen und Schreiben getestet** (geändert, zurückgelesen, zurückgestellt):

- **Therme:** HG01–HG04, HG07–HG09, HG13–HG17, HG19–HG22, HG25, HG33, HG38, HG39, HG41, HG60.
  HG13 = Zirkomat setzt und sperrt HG14 – erst HG13, dann HG14 schreiben.
- **Mischermodul:** MI08 RL-Soll (TN 400), MI09 max. Speicherladezeit (TN 384), TV-min/-max, Heizkurvenabstand,
  Nachlaufzeit, P-Bereich.
- **BM-2 und Heizkreise:** Bedienparameter und Heizkurven, Programmwahl, Party, Urlaub, 1× Warmwasser,
  A04 (TN 388), A07 (TN 257), A08 (TN 618), A09 Frostschutzgrenze (TN 2560), A10 (TN 35), A15 Korrektur
  Außentemperatur (TN 1443), A23 (TN 10141), A26 (TN 10912), Kreisart (TN 9005), Raumeinfluss (TN 651),
  Wartungsdatum (TN 5250/5264).

**Nur gelesen:** HG23 WW-Maximum = TN 385 (Zuordnung am Display bestätigt), HG40 Anlagenkonfiguration (TN 10076),
Raumregler-Parameter A00, A05, A16–A18 (wirken nur mit Raumfühler am BM-2).

**Bewusst ausgelassen:** HG10 (eBus-Adresse), HG12 (Gasart), MI10/Busspeisung; HG43–HG45 – **HG43 am Display
startet eine 100-%-Kalibrierung**.

Fehlercodes mit Klartext und Abgleich gegen die Wolf-Anleitungen: [`docs/fehlercodes-cgb2.md`](docs/fehlercodes-cgb2.md).

## Home Assistant

Vollständige Liste mit Entitätsnamen: [`docs/ha-helfer.md`](docs/ha-helfer.md).

- **Bedienung:** Dashboard „Heizung“ mit Reglern für die HG- und MI-Parameter, Programmwahl der Kreise, Partymodus.
- **Schreib-Skripte:** `heizung_therme_schreiben` (Therme und MM, Prüfbyte in Jinja), `heizung_ebus_schreiben`
  (BM-2/MK, Rücklesen, bis 3 Versuche), `heizung_parametertest`, `heizung_partymodus`.
- **Überwachung:** Störungscodes mit Push, Anlagendruck, Datenausfall, fehlende Außentemperatur (ohne sie gehen beide
  Kreise in Frostschutz), Wartung, Abweichung der BM-2-Uhr.
- **Optimierung:** täglich 07:30 Auswertung des Vortags (Brennerstarts, Laufzeit, Schutzabschaltungen) nach den Regeln
  der Wolf-Montageanleitung; höchstens ein Vorschlag pro Tag, Modi „Nur überwachen“, „Vorschlagen“ (Push mit
  Übernehmen/Ablehnen), „Automatisch“. Reihenfolge bei > 40 Starts und > 30 % Schutzabschaltungen: HG37 → dT (Spreizung),
  HG16 +10 % (max 65), HG39 → 3 min, HG04 −8 % (min 70); bei > 40 Starts: HG09 +3 min (max 15).
  Nie angefasst: Heizkurven, Programmwahl, Warmwasser, Gas-/Abgasparameter.
- **Anwendungsbeispiel Gewerbeeinheit:** Vorheizen nach Buchungskalender, Anwesenheit über Handy-Ortung, Lüftung gegen
  Muff; die Wolf-Kreise gehen nur auf Permanent, solange der Raum Wärme braucht.

## Vollständigkeit der Parameter (Stand 21.10.2026)

`tools/wolf_db_export.py` zieht **alle** Parameter der Wolf-Gerätevorlagen CGB-2, BM-2, DHK_BM-2, WW_BM-2, MK_BM-2 und MM
aus der Parameterdatenbank (ism7mqtt) und schreibt, was nicht schon in den handgepflegten Dateien steht, lesend nach
`ebusd-config/ext_*.csv` (ohne Poll-Priorität; `script.heizung_parameter_einlesen` liest sie täglich 03:30 und nach
ebusd-Neustart ein). Die komplette Liste mit Status je Parameter steht in `docs/parameter_vollstaendig.md`.

Nicht übernommen, mit Grund:
- Zeitprogramme (TIMEPROG_03F1, 399 Einträge): kein Einzeltelegramm, in ism7mqtt „not yet implemented“.
- Einträge ohne Konverter in der Wolf-Datenbank (44), Unicode-Texte (3), Mischerzustand/Bitfelder des MM (3).
- Vorlage WWSystem_BM-2: nicht belegt, dass sie an dieser Anlage aktiv ist.
- Schreibsperre (nur lesen): Programmwahl beider Kreise, HG10, HG12, HG43–HG45 (Verbrennung, nicht einmal lesend).

## Sicherheitsregeln

- Jeder Schreibvorgang wird zurückgelesen und bei Bedarf wiederholt.
- Gesperrt: HG10, HG12, Busspeisung des MM. HG02/HG03 (Brennerleistung) sind schreibbar – mit Bedacht.
- Programmwahl und Heizkurven wirken auf den ganzen Kreis, also auf alle angeschlossenen Wohnungen.
- HG43 am BM-2-Display nicht aufrufen und bestätigen.

## Repo-Struktur

| Pfad | Inhalt |
|---|---|
| `ebusd-config/*.csv` | Nachrichtendefinitionen: Therme, BM-2, Mischerkreis, Mischermodul, Broadcasts, Störungscodes, passives Mitlesen |
| `ebusd-config/mqtt-hassio.cfg` | MQTT-Integration für Home Assistant |
| `tools/wolf_crc.py` | Prüfbyte-Berechnung mit Selbsttest |
| `tools/gen_ebusd_config.py` | erzeugt die CSV-Dateien aus Tabellen |
| `homeassistant/` | Skripte, Automationen, Jinja-Makros (`custom_templates/wolf_bm2.jinja`), Generatoren |
| `docs/protokoll.md` | Protokolldetails, Tests, Mitschnitte, Belege |
| `docs/fehlercodes-cgb2.md` | Störungs- und Warncodes |
| `docs/ha-helfer.md` | alle Home-Assistant-Bausteine |

## Offene Punkte

- A14 (WW-Maximum am BM-2): Telegrammnummer unbekannt.
- HG40: Rohwert 1, laut Wolf-Datenbank „02“ – am Display noch nicht abgelesen.
- MI17 ↔ TN 45 und HG61 ↔ TN 10017: Zuordnung nicht verifiziert.
- Störungshistorie: Suche über bekannten Eintrag (Code 15 vom 20.10.2026) geplant.
- Master `f0`/`f1`: Gerät nicht sicher zugeordnet.

## Quellen und Dank

- [ebusd](https://github.com/john30/ebusd) und [ebusd-configuration](https://github.com/john30/ebusd-configuration)
- [zivillian/ism7mqtt](https://github.com/zivillian/ism7mqtt) – Wolf-Parameterdatenbank (parameter.xml, converter.xml, device.xml)
- [dktzde/ebusd-configuration-wolf](https://github.com/dktzde/ebusd-configuration-wolf) – unabhängige Beschreibung der CRC8
- *audaciousengineer* in [ebusd Discussion #779](https://github.com/john30/ebusd/discussions/779) – 5-Byte-Schreibweg zum BM-2
- Wolf-Unterlagen: CGB-2 Montage-/Betriebsanleitung 3063421 (2015, 2021, 2024), BM-2 Fachkraft ab FW 2.80 (3063305),
  BM-2 Montageanleitung Experte, MM/MM-2 Montageanleitung, Funk-Außenfühler 3060938

## Lizenz

GNU General Public License v3.0, siehe [LICENSE](LICENSE). Grund: Die verwendeten Vorlagen
(ebusd-configuration, ism7mqtt) stehen ebenfalls unter GPL v3. Nutzung, Änderung und Weitergabe sind frei, abgeleitete
Werke müssen wieder unter GPL v3 stehen. Eine kommerzielle Nutzung schließt die GPL nicht aus.
