# Home-Assistant-Helfer (Template-Helfer, angelegt 20.10.2026)

Alle Helfer sind in Home Assistant Hannover über die UI angelegt (Einstellungen → Geräte & Dienste → Helfer, Typ „Template").
Sie brauchen keine CSV-Änderung in ebusd: Sie lesen die vorhandenen `sensor.heating_ebusd_*`-Entitäten und schreiben
über `script.heizung_therme_schreiben` bzw. die Roh-Nachrichten `BmRaw`/`MkRaw`.

## Schieberegler Therme (Template-Number)

`state` = `{{ states('sensor.heating_ebusd_hc_<name>') }}`,
`set_value` = `script.heizung_therme_schreiben` mit `name`, `tn`, `wert={{ value }}`, `teiler`, `minimum`, `maximum`.

| Entität | HG | TN | Bereich | Teiler |
|---|---|---|---|---|
| `number.therme_hg01_schaltdifferenz_brenner` | HG01 | 34 | 7–30 K | 10 |
| `number.therme_hg02_untere_brennerleistung` | HG02 | 346 | 1–100 % | 1 |
| `number.therme_hg03_obere_brennerleistung_warmwasser` | HG03 | 345 | 1–100 % | 1 |
| `number.therme_hg04_obere_brennerleistung_heizung` | HG04 | 319 | 1–100 % | 1 |
| `number.therme_hg07_nachlaufzeit_kesselkreispumpe` | HG07 | 322 | 0–30 min | 1 |
| `number.therme_hg08_kesselmaximaltemperatur_heizung` | HG08 | 644 | 40–90 °C | 10 |
| `number.therme_hg09_brennertaktsperre` | HG09 | 323 | 1–30 min | 1 |
| `number.therme_hg15_speicherhysterese` | HG15 | 320 | 1–30 K | 10 |
| `number.therme_hg16_pumpenleistung_hk_minimal` | HG16 | 341 | 15–100 % | 1 |
| `number.therme_hg17_pumpenleistung_hk_maximal` | HG17 | 342 | 15–100 % | 1 |
| `number.therme_hg22_kesselmaximaltemperatur` | HG22 | 39 | 50–90 °C | 10 |
| `number.therme_hg25_kesseluebertemperatur_speicherladung` | HG25 | 45 | 1–30 K | 10 |
| `number.therme_hg33_laufzeit_brennerhysterese` | HG33 | 33 | 1–30 min | 1 |
| `number.therme_hg38_soll_spreizung_pumpenregelung` | HG38 | 1486 | 0–40 K | 10 |
| `number.therme_hg39_zeit_softstart` | HG39 | 339 | 0–10 min | 1 |
| `number.therme_hg60_minimale_schalthysterese_brenner` | HG60 | 10808 | 2–30 K | 10 |

Bereiche aus der Wolf-Parameterdatenbank (MinValueCondition/MaxValueCondition der Gerätevorlage CGB-2).
Nicht als Regler angelegt: HG12 Gasart, HG10 eBus-Adresse (im Skript gesperrt), HG21/HG62 (liefern `unknown`).

## Auswahlfelder Programmwahl (Template-Select)

| Entität | Quelle | Schreibt | Optionen |
|---|---|---|---|
| `select.heizung_programm_direkter_heizkreis` | `sensor.heating_ebusd_bm2_hkprogram` | `ebusd/bm2/BmRaw/set` = `00 74 27 <code> 00` (TN 10100) | Standby 00, Auto 01, Permanent 02, Sparen 03 |
| `select.heizung_programm_mischerkreis` | `sensor.heating_ebusd_mk_mkprogram` | `ebusd/mk/MkRaw/set` = `00 74 27 <code> 00` (TN 10100 an 86) | wie oben |
| `select.heizung_programm_warmwasser` | `sensor.heating_ebusd_bm2_wwprogram` | `ebusd/bm2/BmRaw/set` = `00 75 27 <code> 00` (TN 10101) | Standby 00, Auto 01, Permanent 02 |

Ablauf: Telegramm senden, 3 s warten, `…/get`, 4 s warten, bis der Sensor die gewählte Option zeigt oder 3 Versuche
erreicht sind; danach Push, falls der Wert nicht übernommen wurde. Prüfbyte `00` reicht, weil das BM-2 und der Mischerkreis
das Prüfbyte beim Schreiben nicht prüfen (Tests 19./20.10.2026). Die Wiederholung ist nötig: BM-2 und MK quittieren nicht,
im Parametertest am 20.10. abends ging jedes dritte Telegramm ohne Wiederholung verloren.

## Schieberegler Mischermodul (Template-Number)

Schreibweg verifiziert 20.10.2026 20:42: `MmRaw` 5 Byte mit Prüfbyte an Slave `52` wird quittiert (ebusd `sent write`, kein
Timeout), Rücklesen sofort korrekt (PumpOverrun 5 → 6 → 5). `set_value` = `script.heizung_therme_schreiben` mit `kreis=mm`.

| Entität | ebusd-Name | TN | Bereich | Teiler |
|---|---|---|---|---|
| `number.mischer_tv_min_minimalbegrenzung` | TvMin | 299 | 0–80 °C | 10 |
| `number.mischer_tv_max_maximalbegrenzung` | TvMax | 40 | 20–80 °C | 10 |
| `number.mischer_heizkurvenabstand` | CurveDistance | 273 | 0–30 K | 10 |
| `number.mischer_nachlaufzeit_heizkreis` | PumpOverrun | 322 | 0–30 min | 1 |
| `number.mischer_p_bereich` | MixerPband | 399 | 5–40 K | 10 |

Nicht als Regler: `Config` (Modulfunktion 1–11) und `EbusPower` – im Skript gesperrt.

## CSV-Dateien ohne Samba in den Add-on-Ordner schreiben

Der File editor (core_configurator) kann per Ingress-API schreiben: `enforce_basepath` kurz auf `false`, App neu starten,
dann `POST /api/save` mit `filename=/app_configs/b4d7ad18_ebusd/ebusd-config/<name>.csv&text=<Inhalt>` (form-urlencoded),
anschließend `enforce_basepath` wieder auf `true`. Lesen geht mit `GET /api/file?filename=…`. Der Ordner heißt im File-editor-Container
`/app_configs/…`, in der ebusd-App `/config/ebusd-config`. Der HA-Konfigurationsordner ist im File editor `/homeassistant/…`
(dort geht `/api/save` auch mit `enforce_basepath=true`); neue Ordner mit `POST /api/newfolder` (`path=…&name=…`).

Stolperstein (20.10.2026): Ein Komma im Kommentarfeld einer CSV-Zeile verschiebt alle folgenden Spalten; ebusd meldet dann
`ERR: invalid numeric argument` für die Zeile und lädt die Datei nur bis dorthin (bm2.csv: statt 141 nur 97 Nachrichten).
Der Generator schreibt deshalb keine Kommas in Kommentare.

## Uhrzeit, Datum, Party-/Urlaubsmodus des BM-2 (angelegt 20.10.2026)

Rohwerte aus ebusd (`bm2.csv`): `Time` TN 10161, `Date` TN 10160, `PartyStart/-End(Date)` TN 10153/10151/10154/10152,
`HolidayStart/-End(Date)` TN 10148/10146/10149/10147, `AntilegionellaStart` TN 10141, `MaintenanceDate` TN 5250.
Kodierung (ism7mqtt `BM2TimeConverterTemplate.cs` / `BM2DateConverterTemplate.cs`, an der Anlage verifiziert):
Zeit = Stunde·256 + Minute; Datum = (Tag−1) + (Monat−1)·32 + (Jahr−2000)·512.

Die Dekodierung steckt einmal in `config/custom_templates/wolf_bm2.jinja` (Kopie in `homeassistant/custom_templates/`),
Makros `bm2_time`, `bm2_date`, `bm2_date_de`, `bm2_datetime_de`, `macro_bm2_time_raw`, `macro_bm2_date_raw`.
Nach Änderungen an der Datei: Aktion `homeassistant.reload_custom_templates`.

| Entität | Inhalt |
|---|---|
| `sensor.heizung_bm_2_uhrzeit` | Uhr des BM-2 als `HH:MM` (Pollpriorität 9, also einige Minuten alt) |
| `sensor.heizung_bm_2_datum` | Datum des BM-2 (device_class date) |
| `sensor.heizung_wartung_fallig_am_ebus` | Wartungsdatum, jetzt über dasselbe Makro |
| `sensor.heizung_partymodus_zeitraum` | `TT.MM.JJJJ HH:MM bis TT.MM.JJJJ HH:MM`; solange der Partymodus aus ist, führt das BM-2 Start = jetzt und Ende = jetzt + 3 h mit |
| `sensor.heizung_urlaubsmodus_zeitraum` | analog für den Urlaubsmodus |
| `sensor.heizung_antilegionellen_startzeit` | Startzeit der Antilegionellenfunktion (gelesen 12:30, Wochentag in `sensor.heating_ebusd_bm2_antilegionella`) |
| `input_number.heizung_bm_2_uhrabweichung` | zuletzt gemessene Abweichung BM-2-Uhr minus HA-Zeit in Minuten (wird vom Skript gesetzt) |
| `script.heizung_bm2_uhr_stellen` | liest Zeit/Datum frisch, misst die Abweichung; ab 2 min, bei falschem Datum oder mit `erzwingen: true` werden `Date` und `Time` über `script.heizung_ebus_schreiben` gestellt (Uhrzeit nur in den ersten 35 s einer Minute) |
| `automation.heizung_bm_2_uhr_taeglich_pruefen` | ruft das Skript täglich 03:17 auf (nach der Sommer-/Winterzeitumstellung) |

Entity-Duplikat behoben: `sensor.heating_ebusd_bm2_maintenancedate` (unique_id `…_0`, veraltet, `unavailable`) gelöscht und
`…_maintenancedate_2` (unique_id `…_value`) auf die alte ID umbenannt; der Wartungs-Helfer liefert wieder `2025-10-09`.

