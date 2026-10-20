#!/usr/bin/env python3
"""Erzeugt die Home-Assistant-Skripte (JSON) fuer das Schreiben an die Therme und den Parametertest.

  script.heizung_therme_schreiben  - schreibt einen HG-Parameter an die Therme (5 Byte an 03, Pruefbyte in Jinja),
                                     liest zurueck, wiederholt bis zu 2x, meldet Fehler.
  script.heizung_parametertest     - aendert jeden schreibbaren Parameter um +1, liest zurueck, schreibt den
                                     Originalwert zurueck, liest erneut, protokolliert alles im Logbuch.

Aufruf: python3 homeassistant/gen_scripts.py  -> homeassistant/script_*.json
"""
import json
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from gen_ebusd_config import HC, BM2, MK  # noqa: E402

# Jinja-Makro: CRC8 Polynom 0x5C, Startwert 0, pro Byte c = shift8(c) XOR byte (identisch zu tools/wolf_crc.py,
# in HA gegen 5 Mitschnitte geprueft: 42010200->ac, 1300f4015d010000->b0, 74270200->d4, 42010100->48,
# 160048016f0172017301->71)
CRC_MACRO = """{%- macro wolfcrc(hexdata) -%}
{%- set ns = namespace(c=0) -%}
{%- for i in range(0, hexdata|length, 2) -%}
  {%- set b = hexdata[i:i+2] | int(base=16) -%}
  {%- for _ in range(8) -%}
    {%- if ns.c >= 128 -%}
      {%- set ns.c = ((ns.c * 2) % 256) | bitwise_xor(92) -%}
    {%- else -%}
      {%- set ns.c = (ns.c * 2) % 256 -%}
    {%- endif -%}
  {%- endfor -%}
  {%- set ns.c = ns.c | bitwise_xor(b) -%}
{%- endfor -%}
{{ '%02x' % ns.c }}
{%- endmacro -%}"""

PAYLOAD_TEMPLATE = CRC_MACRO + """
{%- set t = tn | int -%}
{%- set r = raw | int -%}
{%- set d = '%02x%02x%02x%02x' % (t % 256, t // 256, r % 256, r // 256) -%}
{{ wolfcrc(d) }} {{ d[0:2] }} {{ d[2:4] }} {{ d[4:6] }} {{ d[6:8] }}"""


def therme_schreiben():
    return {
        "alias": "Heizung: Therme-Parameter schreiben (HG)",
        "description": "Schreibt einen HG-Parameter der Wolf CGB-2 ueber ebusd (5 Byte an Master 03, Pruefbyte berechnet). "
                       "Liest zurueck, wiederholt bis zu 2x. Gesperrt bleiben nur HG12 (Gasart) und HG10 (eBus-Adresse).",
        "mode": "queued",
        "fields": {
            "name": {"description": "ebusd-Name in hc, z.B. Hg07", "required": True, "selector": {"text": {}}},
            "tn": {"description": "Telegrammnummer (Wolf-DB), z.B. 322", "required": True,
                   "selector": {"number": {"min": 0, "max": 65535, "mode": "box"}}},
            "wert": {"description": "Zielwert in Anzeigeeinheit (z.B. 1 oder 75.0)", "required": True,
                     "selector": {"number": {"min": -100, "max": 10000, "step": 0.1, "mode": "box"}}},
            "teiler": {"description": "1 fuer ganze Zahlen, 10 fuer Werte mit einer Nachkommastelle", "default": 1,
                       "selector": {"number": {"min": 1, "max": 100, "mode": "box"}}},
            "minimum": {"description": "Erlaubtes Minimum (Bereichspruefung)", "default": -100,
                        "selector": {"number": {"min": -100, "max": 10000, "step": 0.1, "mode": "box"}}},
            "maximum": {"description": "Erlaubtes Maximum (Bereichspruefung)", "default": 10000,
                        "selector": {"number": {"min": -100, "max": 10000, "step": 0.1, "mode": "box"}}},
        },
        "sequence": [
            {"variables": {
                "teiler": "{{ teiler | default(1) | int }}",
                "minimum": "{{ minimum | default(-100) | float }}",
                "maximum": "{{ maximum | default(10000) | float }}",
                "sensor": "sensor.heating_ebusd_hc_{{ name | lower }}",
                "raw": "{{ (((wert | float) * (teiler | default(1) | int)) | round(0) | int) % 65536 }}",
            }},
            {"variables": {"payload": PAYLOAD_TEMPLATE}},
            {"if": [{"condition": "template",
                     "value_template": "{{ name | lower in ['hg12', 'hg10'] or (wert | float) < minimum or (wert | float) > maximum }}"}],
             "then": [
                 {"action": "persistent_notification.create",
                  "data": {"title": "Heizung: Schreiben abgelehnt",
                           "message": "{{ name }} = {{ wert }} liegt ausserhalb {{ minimum }}..{{ maximum }} oder ist gesperrt."}},
                 {"stop": "Bereichspruefung fehlgeschlagen", "error": True},
             ]},
            {"action": "logbook.log",
             "data": {"name": "Heizung eBus", "entity_id": "{{ sensor }}",
                      "message": "schreibe Therme {{ name }} (TN {{ tn }}) = {{ wert }}, Telegramm {{ payload }}"}},
            # Variablen sind in HA seit 2025.4 blockweise gueltig, deshalb wird der Rueckleswert direkt verglichen.
            {"repeat": {
                "until": [{"condition": "template",
                           "value_template": "{{ (states(sensor) | float(-9999) - (wert | float)) | abs < 0.05 or repeat.index >= 3 }}"}],
                "sequence": [
                    {"action": "mqtt.publish", "data": {"topic": "ebusd/hc/HgRaw/set", "payload": "{{ payload }}"}},
                    {"delay": {"seconds": 3}},
                    {"action": "mqtt.publish", "data": {"topic": "ebusd/hc/{{ name }}/get", "payload": ""}},
                    {"delay": {"seconds": 4}},
                ],
            }},
            {"if": [{"condition": "template",
                     "value_template": "{{ (states(sensor) | float(-9999) - (wert | float)) | abs >= 0.05 }}"}],
             "then": [
                 {"action": "persistent_notification.create",
                  "data": {"title": "Heizung: Schreiben fehlgeschlagen",
                           "message": "Therme {{ name }} = {{ wert }} nach 3 Versuchen nicht bestaetigt, gelesen: {{ states(sensor) }}"}},
                 {"action": "notify.mobile_app_birger_iphone",
                  "data": {"title": "Heizung: Schreiben fehlgeschlagen",
                           "message": "Therme {{ name }} = {{ wert }} nicht bestaetigt (gelesen {{ states(sensor) }})"}},
                 {"stop": "Schreiben nicht bestaetigt", "error": True},
             ],
             "else": [
                 {"action": "logbook.log",
                  "data": {"name": "Heizung eBus", "entity_id": "{{ sensor }}",
                           "message": "Therme {{ name }} = {{ wert }} bestaetigt"}},
             ]},
        ],
    }


def test_items():
    items = []
    for tn, name, comment, typ, div, unit, prio, writable in HC:
        if writable and name not in ("Hg21", "Hg62"):  # Hg21/Hg62 liefern 'unknown', nicht testbar
            items.append({"circuit": "hc", "name": name, "tn": tn, "teiler": 10 if div == "10" else 1,
                          "entity": f"sensor.heating_ebusd_hc_{name.lower()}"})
    for table, circ in ((BM2, "bm2"), (MK, "mk")):
        for tn, name, comment, typ, div, unit, prio, writable in table:
            if writable and name not in ("OneTimeHotwater",):  # loest eine Speicherladung aus, kein Test
                items.append({"circuit": circ, "name": name, "tn": tn, "teiler": 10 if div == "10" else 1,
                              "entity": f"number.heating_ebusd_{circ}_{name.lower()}"})
    return items


def parametertest():
    write_bm = [  # BM-2 / MK: statische ebusd-Nachricht, Wert als Anzeigewert
        {"action": "mqtt.publish", "data": {"topic": "ebusd/{{ repeat.item.circuit }}/{{ repeat.item.name }}/set",
                                            "payload": "{{ ziel }}"}},
        {"delay": {"seconds": 3}},
        {"action": "mqtt.publish", "data": {"topic": "ebusd/{{ repeat.item.circuit }}/{{ repeat.item.name }}/get", "payload": ""}},
        {"delay": {"seconds": 4}},
    ]

    def write_step(ziel_var):
        return {
            "variables": {"ziel": "{{ %s }}" % ziel_var},
        }

    def write_block():
        return [
            {"if": [{"condition": "template", "value_template": "{{ repeat.item.circuit == 'hc' }}"}],
             "then": [{"action": "script.heizung_therme_schreiben", "continue_on_error": True,
                       "data": {"name": "{{ repeat.item.name }}", "tn": "{{ repeat.item.tn }}", "wert": "{{ ziel }}",
                                "teiler": "{{ repeat.item.teiler }}"}}],
             "else": write_bm},
        ]

    return {
        "alias": "Heizung: Parametertest (alle schreibbaren Werte +1 und zurueck)",
        "description": "Testlauf: liest jeden schreibbaren Parameter, schreibt Wert+1, liest zurueck, schreibt den Originalwert, "
                       "liest erneut. Ergebnis je Parameter im Logbuch (Name 'Heizung Parametertest').",
        "mode": "single",
        "sequence": [
            {"action": "logbook.log", "data": {"name": "Heizung Parametertest", "message": "Start"}},
            {"repeat": {
                "for_each": test_items(),
                "sequence": [
                    {"action": "mqtt.publish",
                     "data": {"topic": "ebusd/{{ repeat.item.circuit }}/{{ repeat.item.name }}/get", "payload": ""}},
                    {"delay": {"seconds": 4}},
                    {"variables": {"orig": "{{ states(repeat.item.entity) | float(none) }}"}},
                    {"if": [{"condition": "template", "value_template": "{{ orig is none }}"}],
                     "then": [{"action": "logbook.log",
                               "data": {"name": "Heizung Parametertest",
                                        "message": "{{ repeat.item.circuit }}/{{ repeat.item.name }}: UEBERSPRUNGEN, kein Lesewert"}}],
                     "else": [
                         write_step("orig + 1"),
                         *write_block(),
                         {"variables": {"nach_test": "{{ states(repeat.item.entity) | float(none) }}"}},
                         write_step("orig"),
                         *write_block(),
                         # Variablen sind blockweise gueltig (HA >= 2025.4): Ruecklesewert immer direkt aus dem State.
                         {"if": [{"condition": "template",
                                  "value_template": "{{ (states(repeat.item.entity) | float(-9999) - orig) | abs > 0.05 }}"}],
                          "then": [  # Originalwert nochmals schreiben
                              write_step("orig"),
                              *write_block(),
                          ]},
                         {"action": "logbook.log",
                          "data": {"name": "Heizung Parametertest",
                                   "message": "{{ repeat.item.circuit }}/{{ repeat.item.name }}: orig {{ orig }} -> +1 gelesen {{ nach_test }} "
                                              "-> zurueck gelesen {{ states(repeat.item.entity) }} | "
                                              "{{ 'SCHREIBEN OK' if nach_test is not none and (nach_test - orig - 1) | abs < 0.05 else 'SCHREIBEN FEHLGESCHLAGEN' }}, "
                                              "{{ 'RUECKSETZEN OK' if (states(repeat.item.entity) | float(-9999) - orig) | abs < 0.05 else 'RUECKSETZEN FEHLGESCHLAGEN' }}"}},
                         {"if": [{"condition": "template",
                                  "value_template": "{{ (states(repeat.item.entity) | float(-9999) - orig) | abs > 0.05 }}"}],
                          "then": [{"action": "notify.mobile_app_birger_iphone",
                                    "data": {"title": "Heizung Parametertest: Ruecksetzen fehlgeschlagen",
                                             "message": "{{ repeat.item.circuit }}/{{ repeat.item.name }} sollte {{ orig }} sein, gelesen {{ states(repeat.item.entity) }}"}}]},
                     ]},
                ],
            }},
            {"action": "logbook.log", "data": {"name": "Heizung Parametertest", "message": "Ende"}},
            {"action": "notify.mobile_app_birger_iphone",
             "data": {"title": "Heizung Parametertest beendet", "message": "Ergebnis im Logbuch unter 'Heizung Parametertest'."}},
        ],
    }


if __name__ == "__main__":
    for fn, cfg in (("script_heizung_therme_schreiben.json", therme_schreiben()),
                    ("script_heizung_parametertest.json", parametertest())):
        with open(os.path.join(HERE, fn), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=1)
        print(fn, "geschrieben")
    print(len(test_items()), "Testparameter")
