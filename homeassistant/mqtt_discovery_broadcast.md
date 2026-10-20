# MQTT-Discovery von Hand: BM-2 Datetime-Broadcast

ebusd legt für die passiven Broadcast-Nachrichten keine Home-Assistant-Entitäten an. Für die minütliche Uhrzeit des BM-2
(`Broadcast/Datetime`, Topic `ebusd/Broadcast/Datetime`, Payload z. B.
`{"outsidetemp": {"value": null}, "time": {"value": "22:16:10"}, "date": {"value": "20.10.2026"}}`) wurden am
20.10.2026 zwei Discovery-Nachrichten retained veröffentlicht (Aktion `mqtt.publish`, `retain: true`):

Topic `homeassistant/sensor/ebusd_broadcast_Datetime_time/config`:

```json
{"unique_id":"ebusd_broadcast_Datetime_time","name":"Datetime time","state_topic":"ebusd/Broadcast/Datetime",
 "value_template":"{{ value_json.time.value }}","icon":"mdi:clock-outline",
 "availability_topic":"ebusd/global/signal","payload_available":"true","payload_not_available":"false",
 "device":{"identifiers":["ebusd_broadcast"],"name":"ebusd broadcast","manufacturer":"ebusd.eu","via_device":"ebusd"}}
```

Topic `homeassistant/sensor/ebusd_broadcast_Datetime_date/config`: wie oben mit `_date`, `value_json.date.value`,
Icon `mdi:calendar`.

Ergebnis: `sensor.ebusd_broadcast_datetime_time` (`hh:mm:ss`) und `sensor.ebusd_broadcast_datetime_date` (`tt.mm.jjjj`).
Entfernen: leeres retained Payload auf dasselbe Config-Topic.

Hinweis zur Schreibweise: ebusd behält die Groß-/Kleinschreibung des Circuits aus der CSV im Topic bei (`Broadcast`),
beim Schreiben per `…/set` ist die Schreibweise egal. Die Discovery-Topics von ebusd selbst folgen dem Muster
`homeassistant/<typ>/ebusd_<circuit>_<Name>_<Feld>/config` (mqtt-hassio.cfg: `%haprefix/%type_topic/%{TOPIC}_%FIELD/config`);
damit lassen sich verwaiste Entitäten gezielt löschen (z. B. `homeassistant/number/ebusd_bm2_Time_value/config`).
