import network
import rp2
from secrets import secrets
import time
import machine

def init_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['password'])
    
    # Wait for connection with 10 second timeout
    timeout = 10
    while timeout > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        timeout -= 1
        print('Waiting for connection...')
        time.sleep(1)

    # Define blinking function for onboard LED to indicate error codes    
    def blink_onboard_led(num_blinks):
        led = machine.Pin('LED', machine.Pin.OUT)
        for i in range(num_blinks):
            led.on()
            time.sleep(.2)
            led.off()
            time.sleep(.2)
        
    # Handle connection error
    # Error meanings
    # 0  Link Down
    # 1  Link Join
    # 2  Link NoIp
    # 3  Link Up
    # -1 Link Fail
    # -2 Link NoNet
    # -3 Link BadAuth

    wlan_status = wlan.status()
    blink_onboard_led(wlan_status)

    if wlan_status != 3:
        raise RuntimeError('Wi-Fi connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

if __name__ == "__main__":
    init_wifi()
