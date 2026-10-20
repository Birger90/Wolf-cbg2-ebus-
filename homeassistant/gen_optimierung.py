#!/usr/bin/env python3
"""Erzeugt die Home-Assistant-Bausteine der Stufe "Vorschlagen"/"Automatisch" (JSON).

Grundlage: Wolf CGB-2 Montageanleitung 3063421_201512 (Kap. 22/23 Regelungsparameter, Kap. 33 Pumpe,
Kap. 40 Warnung 43 "Viele Brennerstarts") und die Mitschnitte vom 19.10.2026 (Takten tagsueber fast nur
durch Schutzabschaltungen "Spreizung KF" -> "Gradientenueberwachung", d.h. zu wenig Durchfluss).

Regeln (ein Vorschlag pro Tag, erst 24 h nach der letzten Aenderung, Reihenfolge = Prioritaet):
  R1  Starts > 40 und Schutzabschaltungen > 30 % der Starts und HG16 < 65  -> HG16 +10 (Pumpe min, Anleitung S. 61)
  R2  dito und HG39 < 3                                                     -> HG39 = 3 (Softstart, Werkseinstellung)
  R3  dito und HG04 > 70                                                    -> HG04 -8 (max. Heizleistung, Tabelle S. 55)
  R4  Starts > 40 und HG09 < 15                                             -> HG09 +3 (Taktsperre, Warnung 43)
  sonst kein Vorschlag.
Nie: Heizkurve, Programmwahl, Warmwasser, Gas-/Abgasparameter.

Vorschlagsformat in input_text.heizung_vorschlag_offen:
  circuit|name|tn|teiler|von|nach|min|max|grund
"""
import json
import os

HERE = os.path.dirname(__file__)

MOBILE = "notify.mobile_app_birger_iphone"
MODE = "input_select.heizung_optimierung_modus"
OFFEN = "input_text.heizung_vorschlag_offen"
LETZTE = "input_text.heizung_letzte_optimierung"
LETZTE_ZEIT = "input_datetime.heizung_letzte_parameteranderung"
STARTS_TAG = "sensor.wolflink_c083_brennerstarts_pro_tag"       # utility_meter, Quelle eBus; Vortag = Attribut last_period
STUNDEN_TAG = "sensor.wolflink_c083_brennerstunden_pro_tag"      # utility_meter, Quelle eBus
SPREIZ_G = "sensor.heating_ebusd_hc_heizung_schutzabschaltungen_spreizung_gestern"
GRAD_G = "sensor.heating_ebusd_hc_heizung_schutzabschaltungen_gradient_gestern"


def uebernehmen_script():
    return {
        "alias": "Heizung: Vorschlag uebernehmen",
        "description": "Schreibt den offenen Optimierungsvorschlag (input_text.heizung_vorschlag_offen) ueber das passende "
                       "Schreib-Skript, protokolliert und setzt den Zeitstempel der letzten Aenderung.",
        "mode": "single",
        "sequence": [
            {"variables": {
                "v": "{{ states('" + OFFEN + "') }}",
                "p": "{{ states('" + OFFEN + "').split('|') }}",
            }},
            {"if": [{"condition": "template", "value_template": "{{ p | length < 9 }}"}],
             "then": [{"action": "persistent_notification.create",
                       "data": {"title": "Heizung: kein Vorschlag", "message": "Es liegt kein offener Vorschlag vor."}},
                      {"stop": "kein Vorschlag"}]},
            {"variables": {"circuit": "{{ p[0] }}", "name": "{{ p[1] }}", "tn": "{{ p[2] | int }}", "teiler": "{{ p[3] | int }}",
                           "von": "{{ p[4] | float }}", "nach": "{{ p[5] | float }}", "minimum": "{{ p[6] | float }}",
                           "maximum": "{{ p[7] | float }}", "grund": "{{ p[8] }}"}},
            {"action": "logbook.log",
             "data": {"name": "Heizung Optimierung", "message": "uebernehme {{ circuit }}/{{ name }} {{ von }} -> {{ nach }} ({{ grund }})"}},
            {"if": [{"condition": "template", "value_template": "{{ circuit == 'hc' }}"}],
             "then": [{"action": "script.heizung_therme_schreiben",
                       "data": {"name": "{{ name }}", "tn": "{{ tn }}", "wert": "{{ nach }}", "teiler": "{{ teiler }}",
                                "minimum": "{{ minimum }}", "maximum": "{{ maximum }}"}}],
             "else": [{"action": "script.heizung_ebus_schreiben",
                       "data": {"circuit": "{{ circuit }}", "name": "{{ name }}", "wert": "{{ nach }}",
                                "minimum": "{{ minimum }}", "maximum": "{{ maximum }}"}}]},
            # Die Schreib-Skripte enden bei Misserfolg mit Fehler, dann bricht dieses Skript hier ab (Vorschlag bleibt offen).
            {"action": "input_datetime.set_datetime", "target": {"entity_id": LETZTE_ZEIT},
             "data": {"datetime": "{{ now().strftime('%Y-%m-%d %H:%M:%S') }}"}},
            {"action": "input_text.set_value", "target": {"entity_id": LETZTE},
             "data": {"value": "{{ now().strftime('%d.%m. %H:%M') }} {{ name }} {{ von }} -> {{ nach }} ({{ grund }})"}},
            {"action": "input_text.set_value", "target": {"entity_id": OFFEN}, "data": {"value": ""}},
            {"action": "persistent_notification.dismiss", "data": {"notification_id": "heizung_vorschlag"}},
            {"action": MOBILE, "continue_on_error": True,
             "data": {"title": "Heizung: Parameter geaendert",
                      "message": "{{ name }} {{ von }} -> {{ nach }} geschrieben und bestaetigt."}},
        ],
    }


def auswertung_automation():
    rule_tpl = (
        "{% set starts = state_attr('" + STARTS_TAG + "', 'last_period') | float(0) %}"
        "{% set schutz = states('" + SPREIZ_G + "') | float(0) + states('" + GRAD_G + "') | float(0) %}"
        "{% set anteil = (schutz / starts) if starts > 0 else 0 %}"
        "{% set hg16 = states('sensor.heating_ebusd_hc_hg16') | float(-1) %}"
        "{% set hg39 = states('sensor.heating_ebusd_hc_hg39') | float(-1) %}"
        "{% set hg04 = states('sensor.heating_ebusd_hc_hg04') | float(-1) %}"
        "{% set hg09 = states('sensor.heating_ebusd_hc_hg09') | float(-1) %}"
        "{% if starts > 40 and anteil > 0.3 and 0 <= hg16 < 65 %}"
        "hc|Hg16|341|1|{{ hg16 | int }}|{{ [hg16 | int + 10, 65] | min }}|15|100|"
        "Schutzabschaltungen {{ schutz | int }} von {{ starts | int }} Starts: Pumpendrehzahl minimal erhoehen (Anleitung Kap. 33)"
        "{% elif starts > 40 and anteil > 0.3 and 0 <= hg39 < 3 %}"
        "hc|Hg39|339|1|{{ hg39 | int }}|3|0|10|"
        "Schutzabschaltungen {{ schutz | int }} von {{ starts | int }} Starts: Softstart auf Werkseinstellung 3 min"
        "{% elif starts > 40 and anteil > 0.3 and hg04 > 70 %}"
        "hc|Hg04|319|1|{{ hg04 | int }}|{{ [hg04 | int - 8, 70] | max }}|60|100|"
        "Schutzabschaltungen {{ schutz | int }} von {{ starts | int }} Starts: max. Heizleistung senken (Tabelle S. 55)"
        "{% elif starts > 40 and 0 <= hg09 < 15 %}"
        "hc|Hg09|323|1|{{ hg09 | int }}|{{ [hg09 | int + 3, 15] | min }}|1|30|"
        "{{ starts | int }} Starts gestern: Brennertaktsperre erhoehen (Anleitung Warnung 43)"
        "{% endif %}"
    )
    bericht = (
        "Gestern: {{ state_attr('" + STARTS_TAG + "', 'last_period') | int(0) }} Brennerstarts, "
        "{{ state_attr('" + STUNDEN_TAG + "', 'last_period') | float(0) | round(1) }} h Laufzeit, "
        "Schutzabschaltungen Spreizung {{ states('" + SPREIZ_G + "') | int(0) }} / Gradient {{ states('" + GRAD_G + "') | int(0) }}. "
        "Letzte Aenderung: {{ states('" + LETZTE + "') or 'keine' }}."
    )
    return {
        "alias": "Heizung: Optimierung auswerten",
        "description": "Taeglich 07:30: wertet den Vortag aus (Brennerstarts, Laufzeit, Schutzabschaltungen) und erzeugt nach den "
                       "Regeln aus der Wolf-Montageanleitung hoechstens einen Parametervorschlag. Modus 'Vorschlagen': Push mit "
                       "Uebernehmen-Taste; 'Automatisch': direkt schreiben; 'Nur ueberwachen': nur Bericht ins Logbuch.",
        "mode": "single",
        "triggers": [{"trigger": "time", "at": "07:30:00"}],
        "actions": [
            {"variables": {"bericht": bericht, "vorschlag": rule_tpl,
                           "sperre": "{{ states('" + LETZTE_ZEIT + "') not in ['unknown', 'unavailable', ''] and "
                                     "(now() - as_datetime(states('" + LETZTE_ZEIT + "')) | as_local).total_seconds() < 86400 }}"}},
            {"action": "logbook.log", "data": {"name": "Heizung Optimierung", "message": "{{ bericht }} Vorschlag: {{ vorschlag or 'keiner' }}"}},
            {"choose": [
                {"conditions": [{"condition": "state", "entity_id": MODE, "state": "Nur überwachen"}],
                 "sequence": [{"action": "persistent_notification.create",
                               "data": {"notification_id": "heizung_bericht", "title": "Heizung: Tagesbericht", "message": "{{ bericht }}"}}]},
                {"conditions": [{"condition": "template", "value_template": "{{ vorschlag == '' }}"}],
                 "sequence": [{"action": "persistent_notification.create",
                               "data": {"notification_id": "heizung_bericht", "title": "Heizung: Tagesbericht",
                                        "message": "{{ bericht }} Kein Vorschlag (Regeln greifen nicht)."}}]},
                {"conditions": [{"condition": "template", "value_template": "{{ sperre }}"}],
                 "sequence": [{"action": "persistent_notification.create",
                               "data": {"notification_id": "heizung_bericht", "title": "Heizung: Tagesbericht",
                                        "message": "{{ bericht }} Vorschlag zurueckgestellt: letzte Aenderung ist juenger als 24 h."}}]},
                {"conditions": [{"condition": "template", "value_template": "{{ states('" + OFFEN + "') | length > 8 }}"}],
                 "sequence": [{"action": "persistent_notification.create",
                               "data": {"notification_id": "heizung_bericht", "title": "Heizung: Tagesbericht",
                                        "message": "{{ bericht }} Ein Vorschlag ist noch offen und bleibt bestehen: {{ states('" + OFFEN + "') }}"}}]},
                {"conditions": [{"condition": "state", "entity_id": MODE, "state": "Automatisch"}],
                 "sequence": [
                     {"action": "input_text.set_value", "target": {"entity_id": OFFEN}, "data": {"value": "{{ vorschlag }}"}},
                     {"action": "script.heizung_vorschlag_uebernehmen"},
                 ]},
            ],
             "default": [  # Vorschlagen
                 {"action": "input_text.set_value", "target": {"entity_id": OFFEN}, "data": {"value": "{{ vorschlag }}"}},
                 {"action": "persistent_notification.create",
                  "data": {"notification_id": "heizung_vorschlag", "title": "Heizung: Vorschlag",
                           "message": "{{ bericht }}\n\nVorschlag: {{ vorschlag.split('|')[1] }} {{ vorschlag.split('|')[4] }} -> {{ vorschlag.split('|')[5] }}. "
                                      "{{ vorschlag.split('|')[8] }}\n\nUebernehmen: Dashboard Heizung, Taste 'Vorschlag uebernehmen'."}},
                 {"action": MOBILE, "continue_on_error": True,
                  "data": {"title": "Heizung: Vorschlag {{ vorschlag.split('|')[1] }} {{ vorschlag.split('|')[4] }} -> {{ vorschlag.split('|')[5] }}",
                           "message": "{{ vorschlag.split('|')[8] }}. {{ bericht }}",
                           "data": {"actions": [{"action": "HEIZUNG_UEBERNEHMEN", "title": "Uebernehmen"},
                                                {"action": "HEIZUNG_ABLEHNEN", "title": "Ablehnen"}]}}},
             ]},
        ],
    }


def push_antwort_automation():
    return {
        "alias": "Heizung: Vorschlag per Push beantwortet",
        "description": "Reagiert auf die Tasten 'Uebernehmen'/'Ablehnen' der Vorschlags-Push-Nachricht.",
        "mode": "single",
        "triggers": [
            {"trigger": "event", "event_type": "mobile_app_notification_action", "event_data": {"action": "HEIZUNG_UEBERNEHMEN"}, "id": "ja"},
            {"trigger": "event", "event_type": "mobile_app_notification_action", "event_data": {"action": "HEIZUNG_ABLEHNEN"}, "id": "nein"},
        ],
        "actions": [{"choose": [
            {"conditions": [{"condition": "trigger", "id": "ja"}], "sequence": [{"action": "script.heizung_vorschlag_uebernehmen"}]},
            {"conditions": [{"condition": "trigger", "id": "nein"}], "sequence": [
                {"action": "logbook.log", "data": {"name": "Heizung Optimierung", "message": "Vorschlag abgelehnt: {{ states('" + OFFEN + "') }}"}},
                {"action": "input_text.set_value", "target": {"entity_id": OFFEN}, "data": {"value": ""}},
                {"action": "persistent_notification.dismiss", "data": {"notification_id": "heizung_vorschlag"}},
            ]},
        ]}],
    }


if __name__ == "__main__":
    for fn, cfg in (("script_heizung_vorschlag_uebernehmen.json", uebernehmen_script()),
                    ("automation_heizung_optimierung_auswerten.json", auswertung_automation()),
                    ("automation_heizung_vorschlag_push.json", push_antwort_automation())):
        with open(os.path.join(HERE, fn), "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=1)
        print(fn)
