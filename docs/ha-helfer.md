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

Nach dem Schreiben folgt nach 3 s ein `…/get`, damit der Sensor den neuen Wert liest. Prüfbyte `00` reicht, weil das BM-2
und der Mischerkreis das Prüfbyte beim Schreiben nicht prüfen (Tests 19./20.10.2026).

## Mischermodul (geplant)

Regler für TvMin, TvMax, CurveDistance, PumpOverrun, MixerPband folgen, sobald der Parametertest mit `kreis=mm` gelaufen ist.
