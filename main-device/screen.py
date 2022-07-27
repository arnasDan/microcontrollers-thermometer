from machine import I2C
from oled import Write, GFX, SSD1306_I2C #micropython-oled
from oled.fonts import ubuntu_mono_20
from time import sleep

line_height = const(20)
base_height = const(1)
max_height = const(63)
max_width = const(127)
horizontal_middle = const(64)
right_column_start = const(horizontal_middle + 5)
vertical_middle = const(32)

class OledScreen:
    _oled: SSD1306_I2C
    _gfx: GFX
    _writer: Write
    
    def __init__(self, power, scl, sda):
        self._power = power
        self._scl = scl
        self._sda = sda
        
    def init(self):
        self._power.on()
        i2c = I2C(1, scl=self._scl, sda=self._sda)
        sleep(1)
        
        self._oled = SSD1306_I2C(128, 64, i2c)
        self._gfx = GFX(128, 64, self._oled.pixel)
        self._writer = Write(self._oled, ubuntu_mono_20)
        
    def display_data(self, *args):
        self._oled.fill(0)
        current_height = base_height
        for data in args:
            temperature, humidity = data
            
            self._writer.text(temperature, 10, current_height)
            self._writer.text(humidity, right_column_start, current_height)
            
            current_height += line_height
    
        self._oled.show()
    
