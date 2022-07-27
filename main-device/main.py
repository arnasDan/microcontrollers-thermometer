from machine import Pin, reset
from time import sleep
import local_dht
import screen
from micropython import const
from networking import init_wifi
import mqtt
import utils

oled_power = Pin(4, Pin.OUT)
sensor_power = Pin(6, Pin.OUT)
sensor_pin = Pin(5)
scl = Pin(3)
sda = Pin(2)

def run_main_loop():
    client = mqtt.init_client()
    mqtt_sensor = client.add_sensor('temp_sensor')
    custom_mqtt_sensor = client.add_sensor('custom_temp_sensor')
    
    oled_screen = screen.OledScreen(oled_power, scl, sda)
    oled_screen.init()
    
    sensor = local_dht.Sensor(sensor_power, sensor_pin)
    
    while True:
        sleep(1)
        
        local_data = sensor.get_data()
        
        client.refresh()
        mqtt_data = mqtt_sensor.get_data()
        custom_mqtt_data = custom_mqtt_sensor.get_data()
        
        print(local_data)
        print(mqtt_data)
        print(custom_mqtt_data)
        
        try:
            oled_screen.display_data(local_data, mqtt_data, custom_mqtt_data)
        except OSError as e:
            print(e)
        
        utils.collect_garbage()

if __name__ == "__main__":
    try:
        run_main_loop()
    except Exception as e:
        print(e)
        reset()
