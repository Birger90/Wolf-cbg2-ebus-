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
Schreiben (verifiziert 19./20.10.2026):
  BM-2 (35): 5 Byte an Slave 35, Schreib-ID '00' + TN, Prüfbyte wird vom BM-2 nicht geprüft -> statische Zeilen.
  Therme:    5 Byte an Master 03, Prüfbyte WIRD geprüft (mit '00' kein ACK, mit CRC 'done' und Wert geändert).
             Deshalb nur eine Roh-Schreibnachricht HgRaw (HEX:5); Prüfbyte berechnet Home Assistant
             (script.heizung_therme_schreiben, Jinja-Makro, gegen tools/wolf_crc.py verifiziert).
  MK (86):   statische Zeilen wie BM-2 plus MkRaw; ob 86 das Prüfbyte prüft, zeigt der Test.

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
V_AKTIV = vals("0;Deaktiviert;1;Aktiviert")
V_DST = vals("0;Aus;1;Auto")
V_LEGIONELLEN = vals("0;Aus;1;Montag;2;Dienstag;3;Mittwoch;4;Donnerstag;5;Freitag;6;Samstag;7;Sonntag;8;Täglich")

# --- Tabellen: (TN, Name, Kommentar, Typ, Teiler|Werte, Einheit, Poll-Prio oder None, schreibbar) --------------
# Typen: SIN/UIN = 16 Bit signed/unsigned little endian (Wolf-DB SS/US), Teiler 10 = SS10/US10, 100 = SS100/US100

HC = [  # Therme, ZZ 08 (Lesen mit Präfix cc). "schreibbar" = Freigabe fuer HgRaw-Schreiben per HA-Skript (keine statischen w-Zeilen)
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
    (346,   "Hg02",  "HG02 Untere Brennerleistung (1-100 %)",                 "UIN", "",   "%",   9, True),
    (345,   "Hg03",  "HG03 Obere Brennerleistung Warmwasser (1-100 %)",       "UIN", "",   "%",   9, True),
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
    (10100, "HkProgram",         "Programmwahl direkter Heizkreis", "UIN", V_PROGRAMM_HK, "", 3, True),
    (10101, "WwProgram",         "Programmwahl Warmwasser",        "UIN", V_PROGRAMM_WW, "", 5, True),
    (10134, "WwStatus",          "Warmwasser Status",                          "UIN", V_WW_STATUS, "", 5, False),
    (10109, "HkDaytemp",         "Tagtemperatur direkter Heizkreis (5-30 C)",  "SIN", "10", "°C", 9, True),
    (10113, "HkSparfaktor",      "Sparfaktor direkter Heizkreis (0-10)",       "SIN", "10", "",   9, True),
    (10107, "HkCurveBasetemp",   "Sockeltemperatur Heizkurve (10-60 C)",       "SIN", "10", "°C", 9, True),
    (10110, "HkCurveStart",      "Startpunkt Heizkurve (0-40 C)",              "SIN", "10", "°C", 9, True),
    (10111, "HkCurveNormoutside", "Normaussentemperatur Heizkurve (-25-0 C)",  "SIN", "10", "°C", 9, True),
    (10108, "HkCurveFlowtemp",   "Vorlauftemperatur Heizkurve (25-90 C)",      "SIN", "10", "°C", 9, True),
    (10165, "HkSetpointcorr",    "Sollwertkorrektur direkter Heizkreis (-4-4 K)", "SIN", "10", "K", 9, True),
    (278,   "HkWintersummer",    "Winter/Sommer Umschaltung (0-40 C)",         "SIN", "10", "°C", 9, True),
    (279,   "HkEcoabs",          "ECO/ABS (-10-40 C)",                         "SIN", "10", "°C", 9, True),
    (702,   "Absenkstopp",       "Absenkstopp (-30-0 C)",                      "SIN", "10", "°C", 9, True),
    (10159, "HkTimeprogram",     "Zeitprogramm direkter Heizkreis aktiv (1-3)", "UIN", "",  "",   9, True),
    (10158, "WwTimeprogram",     "Zeitprogramm Warmwasser aktiv (1-3)",        "UIN", "",   "",   9, True),
    (10157, "CircTimeprogram",   "Zeitprogramm Zirkulation Heizgeraet aktiv (1-3)", "UIN", "", "", 9, True),
    (10130, "CommonSwitch",      "Programmwahlschalter gemeinsam",             "UIN", V_AUS_EIN, "", 9, True),
    (10102, "DstAuto",           "Winter-/Sommerzeitumstellung",               "UIN", V_DST, "",   9, True),
    # Uhr des BM-2: nur lesen. Schreibversuche 20.10.2026 (5 Byte Praefix 00, 5 Byte CRC, 9 Byte Time+Date mit CRC,
    # Datetime-Broadcast 0700) wurden alle ignoriert; Wolf-DB: Parameter 220032/220033 ReadOnly=True.
    # Die laufende Uhr kommt genauer aus dem Datetime-Broadcast des BM-2 (broadcast.csv, jede Minute).
    (10161, "Time",              "Uhrzeit BM-2 roh (BM2Time: Stunde=v div 256 Minute=v mod 256) - nicht schreibbar", "UIN", "", "", 9, False),
    (10160, "Date",              "Datum BM-2 roh (BM2Date: Tag=(v&31)+1 Monat=((v>>5)&15)+1 Jahr=2000+(v>>9)) - nicht schreibbar", "UIN", "", "", 9, False),
    (10150, "PartyMode",         "Partymodus",                                 "UIN", V_AKTIV, "", 9, True),
    (10153, "PartyStart",        "Partymodus Start Uhrzeit roh (BM2Time)",     "UIN", "",   "",   9, True),
    (10154, "PartyStartDate",    "Partymodus Start Datum roh (BM2Date)",       "UIN", "",   "",   9, True),
    (10151, "PartyEnd",          "Partymodus Ende Uhrzeit roh (BM2Time)",      "UIN", "",   "",   9, True),
    (10152, "PartyEndDate",      "Partymodus Ende Datum roh (BM2Date)",        "UIN", "",   "",   9, True),
    (10145, "HolidayMode",       "Urlaubsmodus",                               "UIN", V_AKTIV, "", 9, True),
    (10148, "HolidayStart",      "Urlaubsmodus Start Uhrzeit roh (BM2Time)",   "UIN", "",   "",   9, True),
    (10149, "HolidayStartDate",  "Urlaubsmodus Start Datum roh (BM2Date)",     "UIN", "",   "",   9, True),
    (10146, "HolidayEnd",        "Urlaubsmodus Ende Uhrzeit roh (BM2Time)",    "UIN", "",   "",   9, True),
    (10147, "HolidayEndDate",    "Urlaubsmodus Ende Datum roh (BM2Date)",      "UIN", "",   "",   9, True),
    (257,   "Antilegionella",    "Antilegionellenfunktion",                    "UIN", V_LEGIONELLEN, "", 9, False),
    (10141, "AntilegionellaStart", "Startzeit Antilegionellenfunktion roh (BM2Time)", "UIN", "", "", 9, False),
    (5266,  "HkControllertype",  "Reglertyp",                                  "UIN", V_REGLERTYP, "", None, False),
    (5249,  "Maintenance",       "Wartung betriebsabhaengig",                  "UIN", "",   "%",  9, False),
    (618,   "MaintenanceMode",   "Wartungsmeldung",                            "UIN", V_WARTUNG, "", None, False),
    (5250,  "MaintenanceDate",   "Wartung Faelligkeitsdatum roh (BM2Date: Tag=(v&31)+1 Monat=((v>>5)&15)+1 Jahr=2000+(v>>9))", "UIN", "", "", 9, False),
    (35,    "ParallelMode",      "Freigabe Parallelbetrieb",                   "UIN", V_AUS_EIN, "", 9, False),
    (10117, "OneTimeHotwater",   "1x Warmwasser",                              "UIN", V_AUS_EIN, "", 9, True),
    (10912, "SmarthomeEnable",   "Freigabe SmartHome",                         "UIN", V_AUS_EIN, "", None, False),
    (388,   "AvgPeriod",         "Aussenfuehler gemittelt Berechnungszeitraum (0-24 h)", "UIN", "", "", None, False),
]

MK = [  # Mischerkreis-Einstellungen, ZZ 86 (Schreiben: gleiches Format wie BM-2, noch ungetestet)
    (10119, "Flowtemp",          "Vorlauftemperatur Mischerkreis",             "SIN", "10", "°C", 3, False),
    (10156, "MkStatus",          "Mischerkreis Status",                        "UIN", V_HK_STATUS, "", 2, False),
    (10155, "MkDemand",          "Anforderung Mischerkreis",                   "UIN", V_HK_ANFORDERUNG, "", 5, False),
    (10100, "MkProgram",         "Programmwahl Mischerkreis", "UIN", V_PROGRAMM_HK, "", 3, True),
    (10109, "MkDaytemp",         "Tagtemperatur Mischerkreis (5-30 C)",        "SIN", "10", "°C", 9, True),
    (10113, "MkSparfaktor",      "Sparfaktor Mischerkreis (0-10)",             "SIN", "10", "",   9, True),
    (10107, "MkCurveBasetemp",   "Sockeltemperatur Heizkurve MK (10-60 C)",    "SIN", "10", "°C", 9, True),
    (10110, "MkCurveStart",      "Startpunkt Heizkurve MK (0-40 C)",           "SIN", "10", "°C", 9, True),
    (10111, "MkCurveNormoutside", "Normaussentemperatur Heizkurve MK (-25-0 C)", "SIN", "10", "°C", 9, True),
    (10108, "MkCurveFlowtemp",   "Vorlauftemperatur Heizkurve MK (25-90 C)",   "SIN", "10", "°C", 9, True),
    (10165, "MkSetpointcorr",    "Sollwertkorrektur Mischerkreis (-4-4 K)",    "SIN", "10", "K",  9, True),
    (10164, "Roomtemp",          "Raumtemperatur Mischerkreis",                "SIN", "10", "°C", 9, False),
    (10179, "OutsidetempAvg",    "Gemittelte Aussentemperatur MK",             "SIN", "10", "°C", 9, False),
    (278,   "MkWintersummer",    "Winter/Sommer Umschaltung MK (0-40 C)",      "SIN", "10", "°C", 9, True),
    (279,   "MkEcoabs",          "ECO/ABS MK (-10-40 C)",                      "SIN", "10", "°C", 9, True),
    (10159, "MkTimeprogram",     "Zeitprogramm Mischerkreis aktiv (1-3)",      "UIN", "",   "",   9, True),
    (5266,  "MkControllertype",  "Reglertyp MK",                               "UIN", V_REGLERTYP, "", None, False),
]

MM = [  # Mischermodul MM, ZZ 52 (Kromschroeder). "schreibbar" = Freigabe fuer MmRaw-Schreiben per HA-Skript (Pruefbyte wie Therme, keine statischen w-Zeilen)
    (15,    "Flowtemp",          "Vorlauftemperatur Mischer",                  "SIN", "10", "°C", 2, False),
    (4,     "Flowtempdesired",   "Mischersolltemperatur",                      "SIN", "10", "°C", 2, False),
    (82,    "Pump",              "Ausgang Mischerkreispumpe MKP",              "UIN", V_AUS_EIN, "", 3, False),
    (2701,  "OutputA1",          "Ausgang A1",                                 "UIN", V_AUS_EIN, "", 9, False),
    (299,   "TvMin",             "Minimalbegrenzung Mischerkreis TV-min (0-80 C)", "SIN", "10", "°C", 9, True),
    (40,    "TvMax",             "Maximalbegrenzung Mischerkreis TV-max (20-80 C)", "SIN", "10", "°C", 9, True),
    (273,   "CurveDistance",     "Heizkurvenabstand (0-30 K)",                 "SIN", "10", "K",  9, True),
    (322,   "PumpOverrun",       "Nachlaufzeit Heizkreis (0-30 min)",          "UIN", "",   "min", 9, True),
    (399,   "MixerPband",        "P-Bereich Mischer (5-40 K)",                 "SIN", "10", "K",  9, True),
    (2593,  "Config",            "Konfiguration MM (1-11)",                    "UIN", "",   "",   None, False),
    (65019, "EbusPower",         "eBus Einspeisung",                           "UIN", V_EBUS_EINSP, "", None, False),
]


def rows(circuit, zz, table, prefix_mode, static_writes=True):
    out = []
    for tn, name, comment, typ, div, unit, prio, writable in table:
        prefix = "cc" if prefix_mode == "cc" else None
        rid = (prefix + tn_hex(tn)) if prefix else read_id(tn)
        rtype = f"r{prio}" if prio else "r"
        out.append(f"{rtype},{circuit},,{name},{comment},,{zz},5022,{rid},value,,{typ},{div},{unit},TN {tn}")
        if writable and static_writes:
            out.append(f"w,{circuit},,{name},{comment},,{zz},5023,00{tn_hex(tn)},value,,{typ},{div},{unit},TN {tn}")
    return out


def raw_write(circuit, name, zz, comment):
    """Roh-Schreibnachricht: Nutzdaten komplett als Hex-Bytes, normal 5 (Pruefbyte TNlo TNhi Wertlo Werthi), z.B. '48 42 01 01 00'.
    Variable Laenge (HEX:*), damit auch die 9-Byte-Form des ISM7 (Pruefbyte TN Wert TN2 Wert2) getestet werden kann."""
    return f"w,{circuit},,{name},{comment},,{zz},5023,,data,,HEX:*,,,Pruefbyte+TN+Wert"


def main():
    os.makedirs(OUT, exist_ok=True)

    hc = [HEADER,
          "# Wolf CGB-2-24 Therme (Kromschroeder-Feuerungsautomat), Slave 08 / Master 03.",
          "# Lesen mit Praefix cc (wie das BM-2), dadurch werden die zyklischen Abfragen des BM-2 passiv mitgelesen.",
          "# Schreiben: 5 Byte an Master 03, die Therme prueft das Pruefbyte (Test 20.10.2026: Praefix 00 -> kein ACK, CRC -> done).",
          "# Das offizielle ebusd-Format (9 Byte mit Anhang 9d010000) nimmt die CGB-2 nicht an (Test 19.10.2026).",
          "# Deshalb eine Roh-Schreibnachricht HgRaw; das Pruefbyte berechnet script.heizung_therme_schreiben in Home Assistant.",
          "# Passive Telegramme des Reglers (Operation, RcTarget) aus der offiziellen ebusd-Konfiguration:",
          "w,hc,,Operation,Betriebsdaten des Reglers an den Feuerungsautomaten,,03,0507,,status,,UCH,0=off;1=none;85=hwc;170=heat;204=emissioncheck;221=techcheck;238=stop;102=hwc_stop;187=hwc_heat;68=hwc_stepped,,status heat request,action,,UCH,0=none;1=pumpoff;2=pumpon;3=consumeoff;4=consumeon,,variable consumers,desiredtemp,,D2C,,°C,boiler target temperature,desiredpress,,D2B,,bar,boiler target pressure,settingdegree,,D1C,,%,setting degree,hwcdesiredtemp,,D1C,,°C,hot water target temperature,fuel,,UCH,0=dontcare;1=gas;2=oil;3=dontcare1,,fuel choice",
          "w,hc,,RcTarget,Sollwertuebertragung des Reglers an andere Regler,,03,0800,,desiredtemp,,D2B,,°C,boiler target temperature,outsidetemp,,D2B,,°C,Aussentemperatur,forced,,SCH,,%,forced performance,hwc,,BI0,,,hot water active,hc,,BI1,,,heat active,hwcdesiredtemp,,D2B,,°C,hot water target temperature",
          raw_write("hc", "HgRaw", "03", "Roh-Schreibtelegramm an die Therme (HG-Parameter) nur ueber script.heizung_therme_schreiben"),
          ] + rows("hc", "08", HC, "cc", static_writes=False)

    bm2 = [HEADER, "# Wolf BM-2 Bedienmodul, Slave 35: System, direkter Heizkreis, Warmwasser.",
           "# Lesen mit CRC-Praefix (wie das ISM7). Schreiben: 5 Byte an 35 mit Praefix 00 (verifiziert 19.10.2026, TN 19 und 279).",
           "# Programmwahl und Sparfaktor schreibbar (Mieterwohnung haengt an beiden Kreisen - mit Bedacht nutzen).",
           raw_write("bm2", "BmRaw", "35", "Roh-Schreibtelegramm an das BM-2 - nur fuer Tests und Skripte"),
           ] + rows("bm2", "35", BM2, "crc")

    mk = [HEADER, "# Mischerkreis-Einstellungen (MK_BM-2), Slave 86. Lesen verifiziert, statische Schreibzeilen wie BM-2.",
          raw_write("mk", "MkRaw", "86", "Roh-Schreibtelegramm an den Mischerkreis - nur fuer Tests und Skripte"),
          ] + rows("mk", "86", MK, "crc")

    mm = [HEADER, "# Wolf Mischermodul MM, Slave 52 (Kromschroeder).",
          "# Schreiben: Kromschroeder-Geraet wie die Therme, deshalb Roh-Schreibnachricht MmRaw mit Pruefbyte aus Home Assistant",
          "# (script.heizung_therme_schreiben, kreis=mm). Zieladresse 52 - ob 52 oder ein Master (f0/f1) Schreibtelegramme annimmt, zeigt der Test.",
          raw_write("mm", "MmRaw", "52", "Roh-Schreibtelegramm an das Mischermodul (Pruefbyte+TN+Wert) nur ueber script.heizung_therme_schreiben kreis=mm"),
          ] + rows("mm", "52", MM, "crc", static_writes=False)

    mc = [HEADER,
          "# Passive Telegramme Regler -> Mischermodul aus der offiziellen ebusd-Konfiguration (kromschroeder/50..mc.csv)",
          "uw,mc,,Yields,Ertrag,,,5018,,power,,D2B,,,Solarleistung,yieldday,,UIN,,,Ertrag Tag,yieldsum,,UIN,,,Summe Ertrag,yieldm,,UCH,,,Summe Ertrag M",
          "uw,mc,,Status,Status,,,5017,,pump,,UCH,188=off;189=on,,Solar Pumpe,ign,,IGN:1,,,,collectortemp,,D2C,,°C,Kollektortemperatur,hwcsolartemp,,D2C,,°C,Solartemperatur Warmwasser",
          "uw,mc,,Operation,Operation,,,5014,,status,,HEX,,,Status Solar,ign,,IGN:1,,,,hctempdesired,,D2B,,°C,Mischer Solltemperatur,roomtemp,,D1C,,°C,Raumtemperatur,hwctempdesired,,D1C,,°C,Warmwasser Solltemperatur",
          ]

    broadcast = [HEADER,
                 "# Standard-Broadcasts (ebusd broadcast.csv + kromschroeder/broadcast.csv)",
                 "u,Broadcast,,Datetime,Datum Uhrzeit,,fe,0700,,outsidetemp,,D2B,,°C,Temperatur,time,,BTI,,,Uhrzeit,date,,BDA,,,Datum",
                 "# Schreibform des Standard-Broadcasts wurde am 20.10.2026 einmal getestet (BM-2 uebernimmt die Uhrzeit nicht) und danach entfernt:",
                 "# kurz darauf fiel die Aussentemperatur des Funkempfaengers (Master 0f) aus - Zusammenhang nicht verifiziert, deshalb keine Broadcasts von ebusd.",
                 "# w,Broadcast,,Datetime,Datum Uhrzeit senden,,fe,0700,,outsidetemp,,D2B,,°C,Temperatur,time,,BTI,,,Uhrzeit,date,,BDA,,,Datum",
                 "# Aussentemperatur vom Funkempfaenger (Master 0f) getrennt mitlesen: derselbe 0700-Broadcast, aber nur mit Temperatur (Zeit/Datum = ff).",
                 "u,Broadcast,,OutsidetempRadio,Aussentemperatur vom Funkempfaenger Master 0f,0f,fe,0700,,outsidetemp,,D2B,,°C,Aussentemperatur,rest,,HEX:7,,,Zeit und Datum ungueltig",
                 "# Ersatz-Aussentemperatur von ebusd senden wurde am 20.10.2026 22:55/22:56 getestet (gleiche Form wie Master 0f, 2x 5.7 C):",
                 "# das BM-2 uebernimmt den Wert nicht (TN 10195 blieb bei 10.1 vom Funkempfaenger). Definition deshalb wieder entfernt:",
                 "# w,Broadcast,,OutsidetempSet,Ersatz-Aussentemperatur senden wie Master 0f,,fe,0700,,outsidetemp,,D2B,,°C,Aussentemperatur,rest,,HEX:7,,,Zeit und Datum ungueltig (ff)",
                 "r,Broadcast,,Id,Identifikation,,,0704,,mf,,UCH,6=Dungs;15=FH_Ostfalia;16=TEM;17=Lamberti;20=CEB;21=Landis-Staefa;22=FERRO;23=MONDIAL;24=Wikon;25=Wolf;32=RAWE;48=Satronic;64=ENCON;80=Kromschroeder;96=Eberle;101=EBV;117=Graesslin;133=ebm-papst;149=SIG;165=Theben;167=Thermowatt;181=Vaillant;192=Toby;197=Weishaupt;253=ebusd,,Geraete-Hersteller,id,,STR:5,,,Geraete-ID,sw,,PIN,,,Software Version,hw,,PIN,,,Hardware-Version",
                 "u,Broadcast,,IdAnswer,answer to identification query,,fe,0704,,mf,,UCH,6=Dungs;15=FH_Ostfalia;16=TEM;17=Lamberti;20=CEB;21=Landis-Staefa;22=FERRO;23=MONDIAL;24=Wikon;25=Wolf;32=RAWE;48=Satronic;64=ENCON;80=Kromschroeder;96=Eberle;101=EBV;117=Graesslin;133=ebm-papst;149=SIG;165=Theben;167=Thermowatt;181=Vaillant;192=Toby;197=Weishaupt;253=ebusd,,Geraete-Hersteller,id,,STR:5,,,Geraete-ID,sw,,PIN,,,Software Version,hw,,PIN,,,Hardware-Version",
                 "u,Broadcast,,Signoflife,Lebenszeichen,,fe,07ff,,",
                 "u,Broadcast,,Error,Fehlernachricht,,fe,fe01,,error,,STR:10,,,",
                 "u,Broadcast,,RcTarget,room controller target values,,fe,0800,,desiredtemp,,D2B,,°C,boiler target temperature,outsidetemp,,D2B,,°C,Aussentemperatur,forced,,SCH,,%,forced performance,hwc,,BI0,,,hot water active,hc,,BI1,,,heat active,hwcdesiredtemp,,D2B,,°C,hot water target temperature",
                 "u,Broadcast,,RcOperation,room controller operational data,,fe,0801,,temp,,D2B,,°C,boiler effective temperature,buffertemp,,D2B,,°C,hot water effective temperature,emissiontest,,UCH,0=none;1=br1;2=br1stb;3=br12;4=br12stb,,emission test,hwc,,BI0,,,hot water active,pump,,BI1,,,pump active,buffer1,,BI2,,,buffer 1 active,buffer2,,BI3,,,buffer 2 active,loading,,BI4,,,loading pump active,hwcloading,,BI5,,,hot water loading pump active,tbfconnect,,BI6,,,TBF connected,returntemp,,D2B,,°C,return flow temperature",
                 "u,Broadcast,,ControlCmd,control commands,,fe,0802,,desiredtemp,,D2B,,°C,boiler target temperature,hwcdesiredtemp,,D2B,,°C,hot water target temperature,expected,,SCH,,%,expected performance,device,,UCH,,,first device with error,error,,UCH,,,error code",
                 "# Roh-Mitschnitt der 8-Byte-Broadcasts PBSB 0503 (eBUS-Standard: Betriebsdaten des Feuerungsautomaten an den Regler; Layout nicht dokumentiert, Kandidat fuer Stoerungscode):",
                 "u,Broadcast,,FaStatusRaw,Betriebsdaten Feuerungsautomat roh (0503 von 03),03,fe,0503,,data,,HEX:8,,,8 Bytes",
                 "u,Broadcast,,F1StatusRaw,Betriebsdaten Master f1 roh (0503 von f1),f1,fe,0503,,data,,HEX:8,,,8 Bytes"
                 ]

    fault = [HEADER,
             "# Aktueller Stoerungscode je Geraet: TN 1 (nicht in der Wolf-Parameterdatenbank fuer CGB-2/BM-2/MM, aber das ISM7 liest",
             "# ihn alle 15 s auf 08/35/52 mit Pruefbyte 5c). Beobachtet 20.10.2026 22:38: BM-2 antwortet 15 = Aussenfuehler defekt,",
             "# waehrend das BM-2 'T aussen' meldet; vorher und auf Therme/MM 0. Praefix 5c = CRC von 01 00, dadurch werden die",
             "# ISM7-Abfragen passiv mitgelesen. Code -> Text: docs/fehlercodes-cgb2.md bzw. custom_templates/wolf_bm2.jinja.",
             "r5,hc,,FaultCode,Aktueller Stoerungscode Therme (TN 1),,08,5022,5c0100,value,,UIN,,,TN 1",
             "r5,bm2,,FaultCode,Aktueller Stoerungscode BM-2 (TN 1),,35,5022,5c0100,value,,UIN,,,TN 1",
             "r5,mm,,FaultCode,Aktueller Stoerungscode Mischermodul (TN 1),,52,5022,5c0100,value,,UIN,,,TN 1",
             ]

    for fname, lines in [("hc.csv", hc), ("bm2.csv", bm2), ("mk.csv", mk), ("mm.csv", mm), ("mc.csv", mc), ("broadcast.csv", broadcast), ("fault.csv", fault)]:
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"{fname}: {len(lines)} Zeilen")


if __name__ == "__main__":
    main()
