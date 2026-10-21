#!/usr/bin/env python3
"""Vollständige Parameterlisten aus der Wolf-Parameterdatenbank (ism7mqtt) als ebusd-CSV.

Quelle: zivillian/ism7mqtt, Verzeichnis src/ism7mqtt/Resources (device.xml, parameter.xml, converter.xml).
Aufruf:  python3 tools/wolf_db_export.py /pfad/zu/ism7mqtt/src/ism7mqtt/Resources
Ausgabe: ebusd-config/ext_hc.csv, ext_bm2.csv, ext_mk.csv, ext_mm.csv  (nur lesend, ohne Poll-Priorität)
         docs/parameter_vollstaendig.md (Liste inkl. der nicht übernommenen Einträge mit Grund)

Gerätevorlagen -> ebusd-Circuit / Slave-Adresse dieser Anlage (Adressen verifiziert 19.10.2026):
  CGB-2 -> hc 08 (Lese-Präfix cc)   BM-2, DHK_BM-2, WW_BM-2 -> bm2 35 (CRC-Präfix)   MK_BM-2 -> mk 86   MM -> mm 52
WWSystem_BM-2 wird nicht übernommen: nicht belegt, dass diese Vorlage an der Anlage aktiv ist.

Datentypen (ism7mqtt-Konverter -> ebusd):
  US/SS            -> UIN/SIN            US10/SS10 -> UIN/SIN Teiler 10     SS100 -> SIN Teiler 100
  BinaryReadOnly   -> UIN roh (Bitnummer im Kommentar)
  BM2Date          -> UIN roh (Tag=(v&31)+1, Monat=((v>>5)&15)+1, Jahr=2000+(v>>9), ism7mqtt BM2DateConverterTemplate)
  BM2Time          -> zwei Felder UCH: minute (Low-Byte), hour (High-Byte) (ism7mqtt BM2TimeConverterTemplate)
  NumericConverter32 (UINT32) -> zwei Nachrichten _lo/_hi (zwei Telegrammnummern)
  Timeprog03F1, TIMEPROG, Unicode-Text, Mischerzustand, ohne Konverter -> NICHT übernommen (siehe Doku-Datei)
Alle Nachrichten sind ohne Poll-Priorität: ebusd liest sie nur auf Anforderung (MQTT .../get bzw. HTTP maxage=0).
Das HA-Skript 'heizung_parameter_einlesen' liest sie einmal täglich komplett ein.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))
from wolf_crc import read_id  # noqa: E402

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "ebusd-config")
DOC = os.path.join(HERE, "..", "docs", "parameter_vollstaendig.md")
HEADER = "type,circuit,level,name,comment,qq,zz,pbsb,id,*name,part,type,divisor/values,unit,comment"

TEMPLATES = [  # (Vorlage, circuit, zz, prefix_mode)
    ("CGB-2", "hc", "08", "cc"),
    ("BM-2", "bm2", "35", "crc"),
    ("DHK_BM-2", "bm2", "35", "crc"),
    ("WW_BM-2", "bm2", "35", "crc"),
    ("MK_BM-2", "mk", "86", "crc"),
    ("MM", "mm", "52", "crc"),
]


def tn_hex(tn):
    return f"{tn & 0xff:02x}{(tn >> 8) & 0xff:02x}"


def slug(name, maxlen=40):
    s = (name.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("Ä", "Ae").replace("Ö", "Oe")
         .replace("Ü", "Ue").replace("ß", "ss").replace("°", "").replace("%", "Proz"))
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s[:maxlen].rstrip("_") or "Param"


def vals(kv):
    parts = kv.split(";")
    out, seen = [], set()
    for k, v in zip(parts[0::2], parts[1::2]):
        n = slug(v, 30)
        while n in seen:
            n += "_"
        seen.add(n)
        out.append(f"{k}={n}")
    return ";".join(out)


def load(res):
    dev = ET.parse(os.path.join(res, "device.xml")).getroot()
    par = ET.parse(os.path.join(res, "parameter.xml")).getroot()
    conv = ET.parse(os.path.join(res, "converter.xml")).getroot()
    templates = {t.get("Name"): [r.get("PTID") for r in t.iter("ParameterReference")] for t in dev.iter("DeviceTemplate")}
    pdesc, cdesc = {}, {}
    for el in par.iter():
        if el.get("PTID"):
            d = {c.tag: (c.text or "").strip() for c in el}
            d["_tag"] = el.tag
            pdesc[el.get("PTID")] = d
    for el in conv.iter():
        if el.get("CTID"):
            d = {c.tag: (c.text or "").strip() for c in el}
            d["_tag"] = el.tag
            cdesc[el.get("CTID")] = d
    return templates, pdesc, cdesc


def core_tns():
    """(circuit, TN) der handgepflegten Dateien, damit nichts doppelt definiert wird."""
    have = {}
    for fn in ("hc", "bm2", "mk", "mm"):
        p = os.path.join(OUT, f"{fn}.csv")
        if not os.path.exists(p):
            continue
        for line in open(p, encoding="utf-8"):
            if line.startswith("#") or line.startswith("type,"):
                continue
            cols = line.rstrip("\n").split(",")
            if len(cols) > 8 and cols[7] == "5022" and len(cols[8]) == 6:
                tn = int(cols[8][4:6] + cols[8][2:4], 16)
                have[(cols[1], tn)] = cols[3]
    return have


def main(res):
    templates, pdesc, cdesc = load(res)
    have = core_tns()
    rows = {"hc": [], "bm2": [], "mk": [], "mm": []}
    names = {k: set() for k in rows}
    ext_tns = {}
    doc = ["# Vollständige Parameterliste (Wolf-Datenbank, ism7mqtt)", "",
           "Erzeugt von `tools/wolf_db_export.py`. Spalte Status: core = in den handgepflegten CSV, ext = in ext_*.csv, "
           "sonst Grund für Nichtübernahme.", ""]
    stats = {"core": 0, "ext": 0, "skip": 0}
    for tname, circuit, zz, pm in TEMPLATES:
        doc += [f"## {tname} → {circuit} (Adresse {zz})", "", "| PTID | Name | Konverter | TN | Status |", "|---|---|---|---|---|"]
        for pt in templates.get(tname, []):
            p = pdesc.get(pt, {})
            c = cdesc.get(pt)
            name = p.get("Name", f"PTID{pt}")
            ro = p.get("ReadOnlyConditionId", "") == "True"
            comment = p.get("Comment", "")
            label = f"{comment} {name}".strip() if comment and comment.startswith("HG") else name
            if not c:
                doc.append(f"| {pt} | {name} | – | – | kein Konverter |"); stats["skip"] += 1; continue
            typ = c.get("Type", "")
            tag = c["_tag"]
            if tag in ("Timeprog03F1ConverterTemplate", "TimeprogConverterTemplate", "UnicodeTextConverter",
                       "MixerStateConverterTemplate") or tag.startswith("READONLY_Bit"):
                doc.append(f"| {pt} | {name} | {tag} | – | nicht übernommen ({typ}: in ism7mqtt nicht implementiert bzw. kein einzelnes Telegramm) |")
                stats["skip"] += 1
                continue
            tns = []
            if tag == "NumericConverter32Template":
                tns = [(int(c["TelegramNrLow"]), "_lo"), (int(c["TelegramNrHigh"]), "_hi")]
            elif c.get("TelegramNr"):
                tns = [(int(c["TelegramNr"]), "")]
            else:
                doc.append(f"| {pt} | {name} | {tag} | – | keine Telegrammnummer |"); stats["skip"] += 1; continue
            for tn, suffix in tns:
                if (circuit, tn) in have:
                    doc.append(f"| {pt} | {name} | {typ} | {tn} | core (`{have[(circuit, tn)]}`) |"); stats["core"] += 1
                    continue
                if (circuit, tn) in ext_tns:
                    doc.append(f"| {pt} | {name} | {typ} | {tn} | doppelt (gleiche TN wie `{ext_tns[(circuit, tn)]}`) |")
                    stats["skip"] += 1
                    continue
                base = "x_" + slug(name) + suffix
                n, k = base, 1
                while n in names[circuit]:
                    n = f"{base}_{tn}" if k == 1 else f"{base}_{tn}_{k}"
                    k += 1
                names[circuit].add(n)
                ext_tns[(circuit, tn)] = n
                rid = ("cc" + tn_hex(tn)) if pm == "cc" else read_id(tn)
                unit = p.get("UnitName", "").replace(",", " ")
                extra = " RO" if ro else ""
                kv = p.get("KeyValueList", "")
                if tag == "NumericConverter16Template":
                    base_t = "SIN" if typ.startswith("SS") else "UIN"
                    div = {"US": "", "SS": "", "US10": "10", "SS10": "10", "SS100": "100", "US100": "100"}.get(typ)
                    if div is None:
                        doc.append(f"| {pt} | {name} | {typ} | {tn} | unbekannter Zahlentyp |"); stats["skip"] += 1; continue
                    if kv and not div:
                        div = vals(kv)
                    fields = f"value,,{base_t},{div},{unit},"
                elif tag == "NumericConverter32Template":
                    fields = "value,,UIN,,,"
                elif tag == "BinaryReadOnlyConverterTemplate":
                    fields = "value,,UIN,,,"
                    extra += f" Bit{c.get('Bitnumber', '?')} OnValue={c.get('OnValue', '?')}"
                elif tag == "BM2DateConverterTemplate":
                    fields = "value,,UIN,,,"
                    extra += " BM2Date"
                elif tag == "BM2TimeConverterTemplate":
                    fields = "minute,,UCH,,,Minute,hour,,UCH,,,"
                else:
                    doc.append(f"| {pt} | {name} | {tag} | {tn} | Konverter nicht abgebildet |"); stats["skip"] += 1; continue
                cmt = (label.replace(",", " ") + extra).strip()
                rows[circuit].append(f"r,{circuit},,{n},{cmt},,{zz},5022,{rid},{fields}TN {tn} PTID {pt}")
                doc.append(f"| {pt} | {name} | {typ} | {tn} | ext (`{n}`) |"); stats["ext"] += 1
        doc.append("")
    for circuit, lines in rows.items():
        p = os.path.join(OUT, f"ext_{circuit}.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n")
            f.write(f"# Automatisch erzeugt aus der Wolf-Parameterdatenbank (ism7mqtt), nur lesend, ohne Poll-Prioritaet.\n")
            f.write("# Einlesen per MQTT ebusd/<circuit>/<name>/get (HA-Skript heizung_parameter_einlesen).\n")
            f.write("\n".join(lines) + ("\n" if lines else ""))
        print(f"ext_{circuit}.csv: {len(lines)} Nachrichten")
    doc.insert(3, f"Stand: core {stats['core']}, ext {stats['ext']}, nicht übernommen {stats['skip']}.")
    with open(DOC, "w", encoding="utf-8") as f:
        f.write("\n".join(doc) + "\n")
    print(stats)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ism7mqtt/src/ism7mqtt/Resources")
