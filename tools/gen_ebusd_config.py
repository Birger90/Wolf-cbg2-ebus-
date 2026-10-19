#!/usr/bin/env python3
"""Erzeugt die ebusd-Konfiguration (CSV) für Wolf CGB-2-24 + BM-2 + MM aus den Tabellen unten.

Quellen der Telegrammnummern (TN): Wolf-Parameterdatenbank aus ism7mqtt (zivillian/ism7mqtt, Resources/*.xml),
Gerätevorlagen CGB-2, BM-2, DHK_BM-2, WW_BM-2, MK_BM-2, MM. Offizielle ebusd-Datei kromschroeder/08..hc.csv
(ebus.github.io) als Basis für Therme/hc.

Busadressen dieser Anlage (verifiziert 19.10.2026 über Vergleich mit der Wolf-Cloud):
  08  Therme CGB-2 (Feuerungsautomat, Kromschröder), Schreiben an Master-Adresse 03
  35  BM-2: Systemparameter, direkter Heizkreis (DHK), Warmwasser
  52  Mischermodul MM (Hardware: Vorlauf, Mischersoll, Pumpe)
  86  Mischerkreis-Einstellungen (MK, Programmwahl, Heizkurve ...)

Lese-ID = Prüfbyte + TN (little endian). Prüfbyte:
  Therme: 'cc' (so liest das BM-2 selbst -> ebusd sieht diese Telegramme passiv mit)
  BM-2/MK/MM: CRC nach tools/wolf_crc.py (so liest das ISM7 -> ebenfalls passiv mitgelesen)
Schreib-ID = '00' + TN (Prüfbyte wird vom BM-2 ignoriert, Test 19.10.2026).

Aufruf: python3 tools/gen_ebusd_config.py  -> schreibt ebusd-config/*.csv
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from wolf_crc import read_id  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "ebusd-config")
HEADER = "type,circuit,level,name,comment,qq,zz,pbsb,id,*name,part,type,divisor/values,unit,comment"


def tn_hex(tn):
    return f"{tn & 0xff:02x}{(tn >> 8) & 0xff:02x}"


def vals(s):
    """'0;Aus;1;Ein' (Wolf-DB) -> '0=Aus;1=Ein' (ebusd), Namen ASCII ohne Leer-/Sonderzeichen, Duplikate nummeriert."""
    parts = s.split(";")
    out, seen = [], {}
    for k, v in zip(parts[0::2], parts[1::2]):
        v = (v.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("Ä", "Ae").replace("Ö", "Oe")
             .replace("Ü", "Ue").replace("ß", "ss").replace(",", "").replace(".", "").replace("/", "_")
             .replace("-", "_").strip().replace(" ", "_"))
        if v in seen:
            seen[v] += 1
            v = f"{v}_{seen[v]}"
        else:
            seen[v] = 1
        out.append(f"{k}={v}")
    return ";".join(out)


# --- Wertelisten (Wolf-DB, wörtlich) -----------------------------------------------------------------
V_BRENNERSTATUS = vals("0;Aus;1;Ruhekontakt;2;Vorspülen;3;Zünden;4;Stabilisierung;5;Ein;6;Ventilprüfung;7;Nachspülen;"
                       "8;Softstart;9;Taktsperre;10;Betrieb ohne Brenner;11;Abgasklappe;12;Störung;13;Gradienten Überwachung;"
                       "14;Gasdruck;15;Spreizung hoch;16;Spreizung KF")
V_BETRIEBSART = vals("0;Test;1;Start;2;Frost Heizkreis;3;Frost Warmwasser;4;Schornsteinfeger;5;Kombibetrieb;6;Parallelbetrieb;"
                     "7;Warmwasser;8;Warmwassernachlauf;9;Mindest-Kombizeit;10;Heizbetrieb;11;Nachlauf Heizkreispumpe;"
                     "12;Frostschutz;13;Standby;14;Kaskadenbetrieb;15;GLT-Betrieb;16;Kalibration;17;Kalibration Heizbetrieb;"
                     "18;Kalibration Warmwasserbetrieb;19;Kalibration Kombibetrieb;20;Warmwasser Schnellstart;"
                     "21;Externe Deaktivierung;22;Durchfluss gering")
V_STB = vals("0;i. O.;1;Ausgelöst")
V_GASART = vals("0;Nat. gas;1;LPG")
V_PROGRAMM_HK = vals("0;Standby;1;Auto;2;Permanent;3;Sparen")
V_PROGRAMM_WW = vals("0;Standby;1;Auto;2;Permanent")
V_HK_STATUS = vals("0;Aus;1;Heizbetrieb;2;Absenkbetrieb;3;Eco;4;Absenkstop;5;AT Abschaltung;6;RT Abschaltung;7;AT Frostschutz;"
                   "8;RT Frostschutz;9;SmartHome;10;Warmwasservorrang;11;Kühlbetrieb;12;TPW ausgelöst;13;Heizvorrang vor Kühlen")
V_HK_ANFORDERUNG = vals("0;Initialisierung;1;Deaktiviert;2;Estrichtrocknung;3;Schornsteinfeger;4;Telefonfernschalter;5;Partymodus;"
                        "6;Urlaubsmodus;7;Automatik ein;8;Automatik aus;9;Permanentbetrieb;10;Sparbetrieb;11;Standby;"
                        "12;Externe Deaktivierung;13;SmartHome;14;Automatik Kühlen Ein;15;Automatik Kühlen Aus;16;Permanent Kühlen")
V_WW_STATUS = vals("0;Deaktiviert;1;Initialisierung;2;Antilegionellenfunktion;3;Fernschalter ein;4;1x Warmwasser;5;Ein;"
                   "6;Bereit, keine Ladung;7;Solarbetrieb;8;Reduzierter Betrieb;9;Aus;10;Ein;11;Bereit, keine Ladung;12;Standby;"
                   "13;SmartHome;14;SmartGrid")
V_AUS_EIN = vals("0;Aus;1;Ein")
V_WARTUNG = vals("0;Aus;1;Betriebsabhängig;2;Datumsabhängig")
V_REGLERTYP = vals("0;Notbetrieb;1;Witterungsgeführt;2;Reiner Raumregler;3;Witterungsgeführt mit Raumeinfluss;4;Erweiterter Raumeinfuss")
V_EBUS_EINSP = vals("0;Aus;1;Ein;2;Auto")

# --- Tabellen: (TN, Name, Kommentar, Typ, Teiler|Werte, Einheit, Poll-Prio oder None, schreibbar) --------------
# Typen: SIN/UIN = 16 Bit signed/unsigned little endian (Wolf-DB SS/US), Teiler 10 = SS10/US10, 100 = SS100/US100

HC = [  # Therme, ZZ 08 (Lesen mit Präfix cc), Schreiben an 03 mit Anhang 9d010000 (offizielles ebusd-Format, auf CGB-2 noch ungetestet)
    (13,    "Flowtemp",          "Kesseltemperatur Vorlauf Istwert",          "SIN", "10",  "°C", 1, False),
    (22,    "Returntemp",        "Ruecklauftemperatur",                        "SIN", "10",  "°C", 2, False),
    (2,     "Flowtempdesired",   "Kesselsolltemperatur",                       "SIN", "10",  "°C", 2, False),
    (14,    "Hwctemp",           "Warmwassertemperatur",                       "SIN", "10",  "°C", 3, False),
    (3,     "Hwctempdesired",    "Warmwassersolltemperatur an der Therme",     "SIN", "10",  "°C", 5, False),
    (12,    "Outsidetemp",       "Aussentemperatur an der Therme",             "SIN", "10",  "°C", 9, False),
    (10013, "Exhausttemp",       "Abgastemperatur",                            "SIN", "10",  "°C", 3, False),
    (10010, "Pressure",          "Anlagendruck",                               "UIN", "100", "bar", 3, False),
    (367,   "Modulation",        "Modulationsgrad",                            "UIN", "",    "%",  1, False),
    (10068, "Brennerstatus",     "Brennerstatus",                              "UIN", V_BRENNERSTATUS, "", 1, False),
    (10067, "Betriebsart",       "Betriebsart der Therme",                     "UIN", V_BETRIEBSART, "", 2, False),
    (10071, "Pumpspeed",         "Drehzahl Heizkreispumpe",                    "UIN", "",    "%",  3, False),
    (364,   "Hwcflow",           "Durchfluss Warmwasser",                      "SIN", "10",  "l/min", 5, False),
    (550,   "BurnerStartsLow",   "Anzahl Brennerstarts Low-Wort (gesamt = High*65536+Low)", "UIN", "", "", 3, False),
    (551,   "BurnerStartsHigh",  "Anzahl Brennerstarts High-Wort",             "UIN", "",    "",   5, False),
    (554,   "BurnerHours",       "Brennerbetriebsstunden",                     "UIN", "",    "h",  5, False),
    (552,   "NetHoursLow",       "Netzbetriebsstunden Low-Wort",               "UIN", "",    "h",  9, False),
    (553,   "NetHoursHigh",      "Netzbetriebsstunden High-Wort",              "UIN", "",    "",   9, False),
    (10078, "NetStarts",         "Anzahl Netz-Starts",                         "UIN", "",    "",   9, False),
    (633,   "Stb",               "Sicherheitstemperaturbegrenzer",             "UIN", V_STB, "",   5, False),
    (10881, "EnergyToday",       "Verbrauch aktueller Tag",                    "UIN", "",    "kWh", 9, False),
    (10882, "HeatToday",         "Erzeugte Waermemenge aktueller Tag",         "UIN", "",    "kWh", 9, False),
    (13048, "EnergyYesterday",   "Verbrauch Vortag",                           "UIN", "",    "kWh", 9, False),
    (13049, "HeatYesterday",     "Erzeugte Waermemenge Vortag",                "UIN", "",    "kWh", 9, False),
    # HG-Parameter (Fachmann-Ebene). Schreiben nur nach Freigabe, siehe README.
    (34,    "Hg01",  "HG01 Schaltdifferenz Brenner (7-30 K)",                 "SIN", "10", "K",   9, True),
    (346,   "Hg02",  "HG02 Untere Brennerleistung (%) - nicht schreiben",     "UIN", "",   "%",   9, False),
    (345,   "Hg03",  "HG03 Obere Brennerleistung Warmwasser (%)",             "UIN", "",   "%",   9, False),
    (319,   "Hg04",  "HG04 Obere Brennerleistung Heizung (1-100 %)",          "UIN", "",   "%",   9, True),
    (322,   "Hg07",  "HG07 Nachlaufzeit Kesselkreispumpe (0-30 min)",         "UIN", "",   "min", 9, True),
    (644,   "Hg08",  "HG08 Kesselmaximaltemperatur Heizung TV-max (40-90 C)", "SIN", "10", "°C",  9, True),
    (323,   "Hg09",  "HG09 Brennertaktsperre Heizbetrieb (1-30 min)",         "UIN", "",   "min", 9, True),
    (320,   "Hg15",  "HG15 Speicherhysterese (1-30 K)",                       "SIN", "10", "K",   9, True),
    (341,   "Hg16",  "HG16 Pumpenleistung HK minimal (15-100 %)",             "UIN", "",   "%",   9, True),
    (342,   "Hg17",  "HG17 Pumpenleistung HK maximal (15-100 %)",             "UIN", "",   "%",   9, True),
    (31,    "Hg21",  "HG21 Kesselminimaltemperatur TK-min (20-90 C)",         "SIN", "10", "°C",  9, True),
    (39,    "Hg22",  "HG22 Kesselmaximaltemperatur TK-max (50-90 C)",         "SIN", "10", "°C",  9, True),
    (45,    "Hg25",  "HG25 Kesseluebertemperatur bei Speicherladung (1-30 K)", "SIN", "10", "K",  9, True),
    (33,    "Hg33",  "HG33 Laufzeit Brennerhysterese (1-30 min)",             "UIN", "",   "min", 9, True),
    (1486,  "Hg38",  "HG38 Soll-Spreizung dT Pumpenregelung (0-40 K)",        "SIN", "10", "K",   9, True),
    (339,   "Hg39",  "HG39 Zeit Softstart (0-10 min)",                        "UIN", "",   "min", 9, True),
    (10808, "Hg60",  "HG60 Minimale Schalthysterese Brenner (2-30 K)",        "SIN", "10", "K",   9, True),
    (10887, "Hg62",  "HG62 Anlagenkorrekturfaktor (0.1-2)",                   "SIN", "100", "",   9, False),
    (363,   "Hg12",  "HG12 Gasart - nur lesen",                               "UIN", V_GASART, "", None, False),
    (376,   "Hg10",  "HG10 eBus-Adresse",                                     "UIN", "",   "",   None, False),
    (410,   "Firmware", "Firmware Feuerungsautomat",                          "SIN", "100", "",  None, False),
]

BM2 = [  # BM-2, ZZ 35 (System, direkter Heizkreis, Warmwasser). Schreiben: 5 Byte an 35, Praefix 00 (verifiziert fuer TN 19)
    (19,    "WwSoll",            "Warmwassersolltemperatur eingestellt (25-65 C)", "SIN", "10", "°C", 5, True),
    (408,   "WwMin",             "Warmwasserminimaltemperatur (25-65 C)",      "SIN", "10", "°C", 9, True),
    (10195, "Outsidetemp",       "Aussentemperatur BM-2",                      "SIN", "10", "°C", 3, False),
    (10179, "OutsidetempAvg",    "Gemittelte Aussentemperatur",                "SIN", "10", "°C", 5, False),
    (10164, "Roomtemp",          "Raumtemperatur am BM-2",                     "SIN", "10", "°C", 5, False),
    (10119, "Flowtemp",          "Vorlauftemperatur direkter Heizkreis",       "SIN", "10", "°C", 3, False),
    (10156, "HkStatus",          "Heizkreis Status",                           "UIN", V_HK_STATUS, "", 2, False),
    (10155, "HkDemand",          "Anforderung Heizkreis",                      "UIN", V_HK_ANFORDERUNG, "", 5, False),
    (10100, "HkProgram",         "Programmwahl direkter Heizkreis - NUR LESEN (Mieter)", "UIN", V_PROGRAMM_HK, "", 3, False),
    (10101, "WwProgram",         "Programmwahl Warmwasser - NUR LESEN",        "UIN", V_PROGRAMM_WW, "", 5, False),
    (10134, "WwStatus",          "Warmwasser Status",                          "UIN", V_WW_STATUS, "", 5, False),
    (10109, "HkDaytemp",         "Tagtemperatur direkter Heizkreis (5-30 C)",  "SIN", "10", "°C", 9, True),
    (10113, "HkSparfaktor",      "Sparfaktor direkter Heizkreis (0-10)",       "SIN", "10", "",   9, False),
    (10107, "HkCurveBasetemp",   "Sockeltemperatur Heizkurve (10-60 C)",       "SIN", "10", "°C", 9, True),
    (10110, "HkCurveStart",      "Startpunkt Heizkurve (0-40 C)",              "SIN", "10", "°C", 9, True),
    (10111, "HkCurveNormoutside", "Normaussentemperatur Heizkurve (-25-0 C)",  "SIN", "10", "°C", 9, True),
    (10108, "HkCurveFlowtemp",   "Vorlauftemperatur Heizkurve (25-90 C)",      "SIN", "10", "°C", 9, True),
    (10165, "HkSetpointcorr",    "Sollwertkorrektur direkter Heizkreis (-4-4 K)", "SIN", "10", "K", 9, True),
    (278,   "HkWintersummer",    "Winter/Sommer Umschaltung (0-40 C)",         "SIN", "10", "°C", 9, True),
    (279,   "HkEcoabs",          "ECO/ABS (-10-40 C)",                         "SIN", "10", "°C", 9, True),
    (5266,  "HkControllertype",  "Reglertyp",                                  "UIN", V_REGLERTYP, "", None, False),
    (5249,  "Maintenance",       "Wartung betriebsabhaengig",                  "UIN", "",   "%",  9, False),
    (618,   "MaintenanceMode",   "Wartungsmeldung",                            "UIN", V_WARTUNG, "", None, False),
    (35,    "ParallelMode",      "Freigabe Parallelbetrieb",                   "UIN", V_AUS_EIN, "", 9, False),
    (10117, "OneTimeHotwater",   "1x Warmwasser",                              "UIN", V_AUS_EIN, "", 9, True),
    (10912, "SmarthomeEnable",   "Freigabe SmartHome",                         "UIN", V_AUS_EIN, "", None, False),
    (388,   "AvgPeriod",         "Aussenfuehler gemittelt Berechnungszeitraum (0-24 h)", "UIN", "", "", None, False),
]

MK = [  # Mischerkreis-Einstellungen, ZZ 86 (Schreiben: gleiches Format wie BM-2, noch ungetestet)
    (10119, "Flowtemp",          "Vorlauftemperatur Mischerkreis",             "SIN", "10", "°C", 3, False),
    (10156, "MkStatus",          "Mischerkreis Status",                        "UIN", V_HK_STATUS, "", 2, False),
    (10155, "MkDemand",          "Anforderung Mischerkreis",                   "UIN", V_HK_ANFORDERUNG, "", 5, False),
    (10100, "MkProgram",         "Programmwahl Mischerkreis - NUR LESEN (Mieter)", "UIN", V_PROGRAMM_HK, "", 3, False),
    (10109, "MkDaytemp",         "Tagtemperatur Mischerkreis (5-30 C)",        "SIN", "10", "°C", 9, True),
    (10113, "MkSparfaktor",      "Sparfaktor Mischerkreis (0-10)",             "SIN", "10", "",   9, False),
    (10107, "MkCurveBasetemp",   "Sockeltemperatur Heizkurve MK (10-60 C)",    "SIN", "10", "°C", 9, True),
    (10110, "MkCurveStart",      "Startpunkt Heizkurve MK (0-40 C)",           "SIN", "10", "°C", 9, True),
    (10111, "MkCurveNormoutside", "Normaussentemperatur Heizkurve MK (-25-0 C)", "SIN", "10", "°C", 9, True),
    (10108, "MkCurveFlowtemp",   "Vorlauftemperatur Heizkurve MK (25-90 C)",   "SIN", "10", "°C", 9, True),
    (10165, "MkSetpointcorr",    "Sollwertkorrektur Mischerkreis (-4-4 K)",    "SIN", "10", "K",  9, True),
    (10164, "Roomtemp",          "Raumtemperatur Mischerkreis",                "SIN", "10", "°C", 9, False),
    (10179, "OutsidetempAvg",    "Gemittelte Aussentemperatur MK",             "SIN", "10", "°C", 9, False),
    (278,   "MkWintersummer",    "Winter/Sommer Umschaltung MK (0-40 C)",      "SIN", "10", "°C", 9, True),
    (279,   "MkEcoabs",          "ECO/ABS MK (-10-40 C)",                      "SIN", "10", "°C", 9, True),
    (5266,  "MkControllertype",  "Reglertyp MK",                               "UIN", V_REGLERTYP, "", None, False),
]

MM = [  # Mischermodul MM, ZZ 52 (nur lesen)
    (15,    "Flowtemp",          "Vorlauftemperatur Mischer",                  "SIN", "10", "°C", 2, False),
    (4,     "Flowtempdesired",   "Mischersolltemperatur",                      "SIN", "10", "°C", 2, False),
    (82,    "Pump",              "Ausgang Mischerkreispumpe MKP",              "UIN", V_AUS_EIN, "", 3, False),
    (2701,  "OutputA1",          "Ausgang A1",                                 "UIN", V_AUS_EIN, "", 9, False),
    (299,   "TvMin",             "Minimalbegrenzung Mischerkreis TV-min (0-80 C)", "SIN", "10", "°C", 9, False),
    (40,    "TvMax",             "Maximalbegrenzung Mischerkreis TV-max (20-80 C)", "SIN", "10", "°C", 9, False),
    (273,   "CurveDistance",     "Heizkurvenabstand (0-30 K)",                 "SIN", "10", "K",  9, False),
    (322,   "PumpOverrun",       "Nachlaufzeit Heizkreis (0-30 min)",          "UIN", "",   "min", 9, False),
    (399,   "MixerPband",        "P-Bereich Mischer (5-40 K)",                 "SIN", "10", "K",  None, False),
    (2593,  "Config",            "Konfiguration MM (1-11)",                    "UIN", "",   "",   None, False),
    (65019, "EbusPower",         "eBus Einspeisung",                           "UIN", V_EBUS_EINSP, "", None, False),
]


def rows(circuit, zz, table, prefix_mode, write_zz=None, write_suffix=""):
    out = []
    for tn, name, comment, typ, div, unit, prio, writable in table:
        prefix = "cc" if prefix_mode == "cc" else None
        rid = (prefix + tn_hex(tn)) if prefix else read_id(tn)
        rtype = f"r{prio}" if prio else "r"
        out.append(f"{rtype},{circuit},,{name},{comment},,{zz},5022,{rid},value,,{typ},{div},{unit},TN {tn}")
        if writable:
            wzz = write_zz or zz
            w = f"w,{circuit},,{name},{comment},,{wzz},5023,00{tn_hex(tn)},value,,{typ},{div},{unit},TN {tn}"
            if write_suffix:
                w += f",suffix,,HEX:4,={write_suffix},,"
            out.append(w)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)

    hc = [HEADER,
          "# Wolf CGB-2-24 Therme (Kromschroeder-Feuerungsautomat), Slave 08 / Master 03.",
          "# Lesen mit Praefix cc (wie das BM-2), dadurch werden die zyklischen Abfragen des BM-2 passiv mitgelesen.",
          "# Schreiben an 03 mit Anhang 9d010000 = offizielles ebusd-Format (kromschroeder/08..hc.csv), auf CGB-2 ungetestet.",
          "# Passive Telegramme des Reglers (Operation, RcTarget) aus der offiziellen ebusd-Konfiguration:",
          "w,hc,,Operation,Betriebsdaten des Reglers an den Feuerungsautomaten,,03,0507,,status,,UCH,0=off;1=none;85=hwc;170=heat;204=emissioncheck;221=techcheck;238=stop;102=hwc_stop;187=hwc_heat;68=hwc_stepped,,status heat request,action,,UCH,0=none;1=pumpoff;2=pumpon;3=consumeoff;4=consumeon,,variable consumers,desiredtemp,,D2C,,°C,boiler target temperature,desiredpress,,D2B,,bar,boiler target pressure,settingdegree,,D1C,,%,setting degree,hwcdesiredtemp,,D1C,,°C,hot water target temperature,fuel,,UCH,0=dontcare;1=gas;2=oil;3=dontcare1,,fuel choice",
          "w,hc,,RcTarget,Sollwertuebertragung des Reglers an andere Regler,,03,0800,,desiredtemp,,D2B,,°C,boiler target temperature,outsidetemp,,D2B,,°C,Aussentemperatur,forced,,SCH,,%,forced performance,hwc,,BI0,,,hot water active,hc,,BI1,,,heat active,hwcdesiredtemp,,D2B,,°C,hot water target temperature",
          ] + rows("hc", "08", HC, "cc", write_zz="03", write_suffix="9d010000")

    bm2 = [HEADER, "# Wolf BM-2 Bedienmodul, Slave 35: System, direkter Heizkreis, Warmwasser.",
           "# Lesen mit CRC-Praefix (wie das ISM7). Schreiben: 5 Byte an 35 mit Praefix 00 (verifiziert 19.10.2026, TN 19).",
           "# Programmwahl bewusst nur lesbar (Mieterwohnung haengt an beiden Kreisen)."] + rows("bm2", "35", BM2, "crc")

    mk = [HEADER, "# Mischerkreis-Einstellungen (MK_BM-2), Slave 86. Lesen verifiziert, Schreiben ungetestet."] + rows("mk", "86", MK, "crc")

    mm = [HEADER, "# Wolf Mischermodul MM, Slave 52 (Kromschroeder). Nur lesen."] + rows("mm", "52", MM, "crc")

    mc = [HEADER,
          "# Passive Telegramme Regler -> Mischermodul aus der offiziellen ebusd-Konfiguration (kromschroeder/50..mc.csv)",
          "uw,mc,,Yields,Ertrag,,,5018,,power,,D2B,,,Solarleistung,yieldday,,UIN,,,Ertrag Tag,yieldsum,,UIN,,,Summe Ertrag,yieldm,,UCH,,,Summe Ertrag M",
          "uw,mc,,Status,Status,,,5017,,pump,,UCH,188=off;189=on,,Solar Pumpe,ign,,IGN:1,,,,collectortemp,,D2C,,°C,Kollektortemperatur,hwcsolartemp,,D2C,,°C,Solartemperatur Warmwasser",
          "uw,mc,,Operation,Operation,,,5014,,status,,HEX,,,Status Solar,ign,,IGN:1,,,,hctempdesired,,D2B,,°C,Mischer Solltemperatur,roomtemp,,D1C,,°C,Raumtemperatur,hwctempdesired,,D1C,,°C,Warmwasser Solltemperatur",
          ]

    broadcast = [HEADER,
                 "# Standard-Broadcasts (ebusd broadcast.csv + kromschroeder/broadcast.csv)",
                 "u,Broadcast,,Datetime,Datum Uhrzeit,,fe,0700,,outsidetemp,,D2B,,°C,Temperatur,time,,BTI,,,Uhrzeit,date,,BDA,,,Datum",
                 "r,Broadcast,,Id,Identifikation,,,0704,,mf,,UCH,6=Dungs;15=FH_Ostfalia;16=TEM;17=Lamberti;20=CEB;21=Landis-Staefa;22=FERRO;23=MONDIAL;24=Wikon;25=Wolf;32=RAWE;48=Satronic;64=ENCON;80=Kromschroeder;96=Eberle;101=EBV;117=Graesslin;133=ebm-papst;149=SIG;165=Theben;167=Thermowatt;181=Vaillant;192=Toby;197=Weishaupt;253=ebusd,,Geraete-Hersteller,id,,STR:5,,,Geraete-ID,sw,,PIN,,,Software Version,hw,,PIN,,,Hardware-Version",
                 "u,Broadcast,,IdAnswer,answer to identification query,,fe,0704,,mf,,UCH,6=Dungs;15=FH_Ostfalia;16=TEM;17=Lamberti;20=CEB;21=Landis-Staefa;22=FERRO;23=MONDIAL;24=Wikon;25=Wolf;32=RAWE;48=Satronic;64=ENCON;80=Kromschroeder;96=Eberle;101=EBV;117=Graesslin;133=ebm-papst;149=SIG;165=Theben;167=Thermowatt;181=Vaillant;192=Toby;197=Weishaupt;253=ebusd,,Geraete-Hersteller,id,,STR:5,,,Geraete-ID,sw,,PIN,,,Software Version,hw,,PIN,,,Hardware-Version",
                 "u,Broadcast,,Signoflife,Lebenszeichen,,fe,07ff,,",
                 "u,Broadcast,,Error,Fehlernachricht,,fe,fe01,,error,,STR:10,,,",
                 "u,Broadcast,,RcTarget,room controller target values,,fe,0800,,desiredtemp,,D2B,,°C,boiler target temperature,outsidetemp,,D2B,,°C,Aussentemperatur,forced,,SCH,,%,forced performance,hwc,,BI0,,,hot water active,hc,,BI1,,,heat active,hwcdesiredtemp,,D2B,,°C,hot water target temperature",
                 "u,Broadcast,,RcOperation,room controller operational data,,fe,0801,,temp,,D2B,,°C,boiler effective temperature,buffertemp,,D2B,,°C,hot water effective temperature,emissiontest,,UCH,0=none;1=br1;2=br1stb;3=br12;4=br12stb,,emission test,hwc,,BI0,,,hot water active,pump,,BI1,,,pump active,buffer1,,BI2,,,buffer 1 active,buffer2,,BI3,,,buffer 2 active,loading,,BI4,,,loading pump active,hwcloading,,BI5,,,hot water loading pump active,tbfconnect,,BI6,,,TBF connected,returntemp,,D2B,,°C,return flow temperature",
                 "u,Broadcast,,ControlCmd,control commands,,fe,0802,,desiredtemp,,D2B,,°C,boiler target temperature,hwcdesiredtemp,,D2B,,°C,hot water target temperature,expected,,SCH,,%,expected performance,device,,UCH,,,first device with error,error,,UCH,,,error code",
                 ]

    for fname, lines in [("hc.csv", hc), ("bm2.csv", bm2), ("mk.csv", mk), ("mm.csv", mm), ("mc.csv", mc), ("broadcast.csv", broadcast)]:
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"{fname}: {len(lines)} Zeilen")


if __name__ == "__main__":
    main()
