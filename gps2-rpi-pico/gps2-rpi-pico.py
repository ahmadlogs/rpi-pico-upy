from machine import Pin, UART, I2C
#Import utime library to implement delay
import utime, time

#________________________________________________________
from ssd1306 import SSD1306_I2C
#https://github.com/stlehmann/micropython-ssd1306
#________________________________________________________
from micropyGPS import MicropyGPS
#https://github.com/inmcm/micropyGPS
#________________________________________________________

##########################################################
#Oled I2C connection
i2c=I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
##########################################################

##########################################################
#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
##########################################################


##########################################################
TIMEZONE = 5
my_gps = MicropyGPS(TIMEZONE)
##########################################################

##########################################################
def convert(parts):
    if (parts[0] == 0):
        return None
        
    data = parts[0]+(parts[1]/60.0)
    # parts[2] contain 'E' or 'W' or 'N' or 'S'
    if (parts[2] == 'S'):