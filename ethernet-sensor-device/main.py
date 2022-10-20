from machine import Pin, reset
from time import sleep
import dht
from micropython import const
import gc
import utils
import mqtt
import networking

sensor_power = Pin(6, Pin.OUT)
sensor_pin = Pin(5)

def run_main_loop():
    sensor = dht.SI7021(sensor_pin)
    networking.init_ethernet()
    mqtt_client = mqtt.init_client('pi-pico-sensor', 'custom_temp_sensor')
    
    while True:
        sleep(10)
        
        try:
            temp, humidity = dht.get_data(sensor_power, sensor)
        except Exception as e:
            print(e)
            print('sensor error')
            continue
        print(temp)
        print(humidity)
        
        mqtt_client.publish(temp, humidity)
        
        utils.collect_garbage()

try:
    run_main_loop()
except Exception as e:
    print(e)
    print('will reset in 30 seconds')
    sleep(30)
    reset() 