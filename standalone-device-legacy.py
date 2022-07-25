#initial code, everything in a single pi pico
from machine import Pin, I2C, reset
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_20, ubuntu_condensed_20
from time import sleep
import dht
from micropython import const
import gc

oled_power = Pin(4, Pin.OUT)
oled_power.on()
sensor_power = Pin(6, Pin.OUT)
sensor_power.on()

def init_oled():
    i2c = I2C(1, scl=Pin(3), sda=Pin(2))
    sleep(1)
    oled = SSD1306_I2C(128, 64, i2c)
    gfx = GFX(128, 64, oled.pixel)

    return oled, gfx

def init_sensor():
    sensor = dht.SI7021(Pin(5))
    sleep(4)
    return sensor

line_height = const(20)
base_height = const(12)
max_height = const(63)
max_width = const(127)
horizontal_middle = const(64)
right_column_start = const(horizontal_middle + 5)
vertical_middle = const(32)

def collect_garbage():
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

def get_data(sensor):
    try:
        temp = '{}C'.format(sensor.temperature)
        humidity = '{}%'.format(sensor.humidity)
        
        return (temp, humidity)
    except dht.InvalidPulseCount as e:
        print(e)
        return ('Error', 'Error')

def display_data(oled, text_writer, data_writer, temp, humidity):
    oled.fill(0)
    
    text_writer.text("Temp", 15, base_height)
    data_writer.text(temp, 10, base_height + line_height)
    
    text_writer.text("Hum", right_column_start + 7, base_height)
    data_writer.text(humidity, right_column_start, base_height + line_height)
    
    #draw_vertical_line(gfx, horizontal_middle - 2, 0, max_height)

def draw_vertical_line(gfx, x, y, length, thickness=3, invert=False):
    for column in range(x - thickness, x + 1) if invert else range(x, x + thickness + 1):
        gfx.line(column, y, column, y + length, 1)
    
def draw_horizontal_line(gfx, x, y, length, thickness=3, invert=False):
    for row in range(y - thickness, y + 1) if invert else range(y, y + thickness + 1):
        gfx.line(x, row, x + length, row, 1)

def display_lines(gfx, iteration):    
    if iteration == 0:
        draw_horizontal_line(gfx, 0, 0, horizontal_middle)
        draw_vertical_line(gfx, 0, 0, vertical_middle)
    elif iteration == 1:
        draw_horizontal_line(gfx, horizontal_middle, 0, horizontal_middle)
        draw_vertical_line(gfx, max_width, 0, vertical_middle, invert=True)
    elif iteration == 2:
        draw_horizontal_line(gfx, horizontal_middle, max_height, horizontal_middle, invert=True)
        draw_vertical_line(gfx, max_width, vertical_middle, vertical_middle, invert=True)
    elif iteration == 3:
        draw_vertical_line(gfx, 0, vertical_middle, vertical_middle)
        draw_horizontal_line(gfx, 0, max_height, horizontal_middle, invert=True)

def run_main_loop():
    oled, gfx = init_oled()
    
    write_mono = Write(oled, ubuntu_mono_20)
    write_text = Write(oled, ubuntu_condensed_20)
    
    sensor = init_sensor()
    
    i = 0
    while True:
        display_lines(gfx, i)
        
        sleep(1)

        if i == 4:
            temp, humidity = get_data(sensor)
            display_data(oled, write_text, write_mono, temp, humidity)
            collect_garbage()
            i = 0
        else:
            i += 1
        try:
            oled.show()
        except OSError as e:
            print(e)

try:
    run_main_loop()
except Exception as e:
    print(e)
    reset()