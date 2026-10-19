# Wolf CGB-2 am eBus mit ebusd und Home Assistant

Lokaler Lese- **und Schreibzugriff** auf eine Wolf-Gasbrennwerttherme CGB-2-24 mit Bedienmodul BM-2 und
Mischermodul MM über den eBus, ohne Wolf-Cloud und ohne ISM7/Link home. Stand 19.10.2026, alles an einer
realen Anlage verifiziert (Werte gegen die Wolf-Cloud verglichen).

```
Therme CGB-2-24 ──┐
BM-2 (Regler)   ──┤ eBus ── eBUS Adapter Shield C5 (ESP32-C5, WLAN) ── ebusd (HA-App) ── MQTT ── Home Assistant
MM (Mischer)    ──┤
ISM7 (noch)     ──┘
```

## Was im Repo liegt

| Pfad | Inhalt |
|---|---|
| `ebusd-config/*.csv` | Nachrichtendefinitionen für ebusd (Therme, BM-2, Mischerkreis, Mischermodul, Broadcast) |
| `ebusd-config/mqtt-hassio.cfg` | ebusd-MQTT-Integration für Home Assistant (angepasste Filter, alle Werte, schreibbare Nachrichten) |
| `tools/wolf_crc.py` | Prüfbyte-Berechnung des Wolf-Protokolls, Selbsttest gegen 30 mitgeschnittene Telegramme |
| `tools/gen_ebusd_config.py` | Generator, der die CSV-Dateien aus Tabellen erzeugt (Telegrammnummern aus der Wolf-Parameterdatenbank) |
| `docs/protokoll.md` | Protokolldetails, Busadressen, was funktioniert und was nicht, mit Belegen |

## Hardware

- Wolf CGB-2-24 (Feuerungsautomat von Kromschröder), Software laut eBus-Scan 2002
- Wolf BM-2, Software 02.04
- Wolf MM (Mischermodul, Kromschröder)
- [eBUS Adapter Shield C5](https://adapter.ebusd.eu/v5-c5/) am eBus-Anschluss der Therme, Betrieb über WLAN (`ens:IP:9999`)
- Home Assistant OS auf Raspberry Pi mit der App [eBUSd von LukasGrebe](https://github.com/LukasGrebe/ha-addons) (ebusd 26.1) und Mosquitto

## Busadressen dieser Anlage

| Slave | Gerät | Inhalt |
|---|---|---|
| `08` (Master `03`) | Therme | Temperaturen, Druck, Brennerstatus, Zähler, HG-Parameter |
| `35` (Master `30`) | BM-2 | Systemparameter, direkter Heizkreis, Warmwasser |
| `52` | Mischermodul MM | Mischer-Vorlauf, Mischersoll, Pumpe, MM-Parameter |
| `86` | Mischerkreis (MK) | Programmwahl, Heizkurve, Tagtemperatur des Mischerkreises |
| `ff` | ISM7 | Master, liest alles zyklisch |

Verifiziert über Vorlauftemperaturen: `35`/TN 10119 = Vorlauf direkter Heizkreis, `86`/TN 10119 = `52`/TN 15 = Mischer-Vorlauf,
jeweils identisch mit der Wolf-Cloud.

## Protokoll in Kürze

Lesen (PBSB `5022`): `ZZ 50 22 03 <Prüfbyte> <TN lo> <TN hi>` → Antwort `02 <Wert lo> <Wert hi>`
Schreiben (PBSB `5023`): `ZZ 50 23 05 <Prüfbyte> <TN lo> <TN hi> <Wert lo> <Wert hi>`

TN = Telegrammnummer aus der Wolf-Parameterdatenbank (identisch mit den Nummern im ISM7-Protokoll, siehe
[zivillian/ism7mqtt](https://github.com/zivillian/ism7mqtt)). Werte sind 16 Bit little endian, bei Temperaturen ×10.

**Prüfbyte** = CRC8 über alle folgenden Bytes, Polynom `0x5C`, Startwert `0x00`, pro Byte `c = shift8(c) XOR byte`.
Entschlüsselt aus neun ISM7-Schreibtelegrammen mit unterschiedlichen Werten und an allen 30 Mitschnitten
(Einzel- und Blocklesen, Schreiben von BM-2 und ISM7) bestätigt, siehe `tools/wolf_crc.py --verify`.
Unabhängig davon beschreibt [dktzde/ebusd-configuration-wolf](https://github.com/dktzde/ebusd-configuration-wolf)
dieselbe Formel.

Beobachtet: Die Therme antwortet auf Lesetelegramme mit beliebigem Prüfbyte (`00`, `cc`, CRC). Das BM-2 nimmt
Schreibtelegramme auch mit falschem Prüfbyte an. Deshalb reichen statische IDs in den CSV-Dateien.

### Was beim Schreiben wichtig war

- Das ISM7 schreibt 9 Byte an die **Master**-Adresse `30` (mit Anhang `5d01 0000`). Diese Form wird von ebusd aus
  nicht angenommen (kein ACK, Wert unverändert), auch nicht mit Absenderadresse `ff`.
- Es funktioniert die 5-Byte-Form an die **Slave**-Adresse `35` ohne Anhang (`31 35 5023 05 b1 1300 f401` = WW-Soll 50,0 °C).
  Hinweis von *audaciousengineer* in [ebusd Discussion #779](https://github.com/john30/ebusd/discussions/779).
- ebusd meldet dabei immer `ERR: read timeout`, weil das BM-2 keine Antwortdaten liefert
  ([ebusd Issue #1696](https://github.com/john30/ebusd/issues/1696)). Erfolg nur durch Zurücklesen prüfen.
  Von fünf Schreibvorgängen kam einer nicht an und musste wiederholt werden.
- Schreiben an die Therme (HG-Parameter): offizielles ebusd-Format an Master `03` mit Anhang `9d010000`
  (kromschroeder/08..hc.csv). **Auf der CGB-2 noch nicht getestet.**

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
4. App neu starten. Im Log muss stehen `found messages: 146 (… 88 poll, 10 update)`.
5. Home Assistant legt per MQTT-Discovery die Entitäten an: `sensor.heating_ebusd_<circuit>_<name>`,
   schreibbare Werte als `number.…` bzw. `select.…`.

Die Therme wird vom BM-2 ohnehin alle ~65 s abgefragt; da die IDs in `hc.csv` dem Format des BM-2 entsprechen
(Präfix `cc`), liest ebusd diese Antworten passiv mit. BM-2/MK/MM nutzen das CRC-Präfix wie das ISM7, solange
das ISM7 am Bus hängt, kommen auch diese Werte passiv.

## Sicherheitsregeln (für die HA-Automatisierung)

- Programmwahl (Standby/Sparen) beider Heizkreise ist in ebusd **nur lesbar** definiert, die Mieterwohnung hängt an beiden Kreisen.
- Keine Gas-/Abgasparameter (Gasart, Kalibrierung, untere Brennerleistung HG02).
- Jeder Schreibvorgang wird zurückgelesen und bei Bedarf einmal wiederholt.

## Quellen

- [ebusd](https://github.com/john30/ebusd), [ebusd-configuration](https://github.com/john30/ebusd-configuration) (kromschroeder/08..hc.csv, 50..mc.csv, broadcast.csv)
- [zivillian/ism7mqtt](https://github.com/zivillian/ism7mqtt) (Wolf-Parameterdatenbank: parameter.xml, converter.xml, device.xml)
- [dktzde/ebusd-configuration-wolf](https://github.com/dktzde/ebusd-configuration-wolf) (CRC8-Beschreibung)
- [ebusd Issue #1696](https://github.com/john30/ebusd/issues/1696), [Discussion #779](https://github.com/john30/ebusd/discussions/779)
