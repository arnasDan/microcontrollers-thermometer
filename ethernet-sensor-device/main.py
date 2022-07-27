from machine import Pin, reset
from time import sleep
import dht
from micropython import const
import gc
import utils
import mqtt

sensor_power = Pin(6, Pin.OUT)
sensor_pin = Pin(5)

def run_main_loop():
    sensor = dht.SI7021(sensor_pin)
    mqtt_client = mqtt.init_client()
    
    while True:        
        temp, humidity = dht.get_data(sensor_power, sensor)       
        print(temp)
        print(humidity)
        
        mqtt_client.publish(temp, humidity)
        
        utils.collect_garbage()
        sleep(10)

try:
    run_main_loop()
except Exception as e:
    print(e)
    #reset() 