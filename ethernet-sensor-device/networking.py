import network
from machine import Pin, SPI
from time import sleep

led = Pin(25, Pin.OUT)

def init_ethernet():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    while not nic.isconnected():
        sleep(1)
        print(nic.regs())
    sleep(5)

if __name__ == "__main__":
    init_ethernet()