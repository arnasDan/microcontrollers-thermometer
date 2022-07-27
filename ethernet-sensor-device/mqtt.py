from umqtt.simple import MQTTClient
import json
import networking

class MqttSensorClient:
    def __init__(self, client, topic):
        self._client = client
        self._topic = str.encode(topic)
    
    def publish(self, temperature, humidity):
        json_msg = json.dumps({
            'temperature': temperature,
            'humidity': humidity
        })
        self._client.publish(
            self._topic,
            str.encode(json_msg))

def init_client():
    networking.init_ethernet()
    client = MQTTClient('pi-pico-sensor', '192.168.0.123')
    client.connect()
     
    return MqttSensorClient(client, 'zigbee2mqtt/custom_temp_sensor')
