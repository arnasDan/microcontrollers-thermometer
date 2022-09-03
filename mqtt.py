from umqtt.simple import MQTTClient
import formatting
from time import sleep
import json

def format_topic(topic):
    return 'zigbee2mqtt/{}'.format(topic)

class MqttSensorClient:
    _sensors = {}
    
    def __init__(self, client, topic):
        self._client = client
        self._topic = str.encode(format_topic(topic))
        client.set_callback(self.__callback)
   
    def __callback(self, topic, message):
        topic = topic.decode()
        if topic in self._sensors:
            message = json.loads(message)
            
            self._sensors[topic].update_state(
                message['temperature'],
                message['humidity'])
            
    def add_sensor(self, topic):
        topic = format_topic(topic)
        self._client.subscribe(topic)
        sensor = MqttSensor()
        self._sensors[topic] = sensor
        return sensor
    
    def publish(self, temperature, humidity):
        json_msg = json.dumps({
            'temperature': temperature,
            'humidity': humidity
        })
        self._client.publish(
            self._topic,
            str.encode(json_msg))
    
    def refresh(self):
        self._client.check_msg()

class MqttSensor:
    _temperature = None
    _humidity = None
    
    def update_state(self, temperature, humidity):
        self._temperature = temperature
        self._humidity = humidity
        
    def get_data(self):
        return formatting.format_data(
            self._temperature, self._humidity)

def init_client(name, topic):
    client = MQTTClient(name, '192.168.0.123')
    client.connect()
     
    return MqttSensorClient(client, topic)