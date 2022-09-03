import dht
import formatting

class Sensor:
    __temperature: float
    __humidity: float
    
    def __init__(self, power_pin, sensor_pin):
        self._power_pin = power_pin
        self._sensor = dht.SI7021(sensor_pin)
        
    def get_raw(self):
        if self.__temperature is not None and self.__humidity is not None:
            return self.__temperature, self.__humidity
        
        return None
    
    def get_formatted(self):
        return formatting.format_data(self.__temperature, self.__humidity)
        
    def refresh(self):   
        try:
            temp, hum = dht.get_data(self._power_pin, self._sensor)
            self.__temperature = temp
            self.__humidity = hum
        except Exception as e:
            print(e)
            self.__humidity = None
            self.__temperature = None
        