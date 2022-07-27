import dht
import formatting

class Sensor:   
    def __init__(self, power_pin, sensor_pin):
        self._power_pin = power_pin
        self._sensor = dht.SI7021(sensor_pin)
        
    def get_data(self):   
        try:
            temp, hum = dht.get_data(self._power_pin, self._sensor)
            return formatting.format_data(temp, hum)
        except Exception as e:
            print(e)
            return formatting.format_data(None, None)
        