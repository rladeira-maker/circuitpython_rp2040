# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT
from time import sleep
import time
import board
import terminalio
from adafruit_display_text import label

from adafruit_bitmap_font import bitmap_font

import digitalio
import busio
import displayio
from adafruit_st7789 import ST7789

import rtc

r = rtc.RTC()
hora = (input ('Digite a hora atual ou c para continuar:  '))
if hora != 'c' and hora != 'C':
    hora = int (hora)
    min = int(input ('agora os minutos:  '))
    data = input ('dia de hoje no formato DD/MM/AA  ')
    input('Digite enter para iniciar o relógio')
    r.datetime = time.struct_time((int('20'+data[6:8]), int(data[3:5]), int(data[0:2]), hora, min, 00, 0, -1, -1))


#Initial configuration of Display
def tft_init():
    
    tft_pwron= board.GP22
    tft_mosi = board.GP3
    tft_clk  = board.GP2
    tft_cs   = board.GP5
    tft_dc   = board.GP1
    tft_rst  = board.GP0
    tft_bl   = board.GP4

    tft_pwr_on_pin = digitalio.DigitalInOut(tft_pwron)
    tft_pwr_on_pin.direction= digitalio.Direction.OUTPUT
    tft_pwr_on_pin.value = True
    displayio.release_displays()
    tft_spi  = busio.SPI( clock=tft_clk, MOSI=tft_mosi )
    display_bus = displayio.FourWire( tft_spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
    return (ST7789( display_bus, rotation=270, width=240, height=135, backlight_pin=tft_bl, rowstart=40, colstart=53))

# Inicializa o display
display = tft_init()

display.brightness = 0.5

#display = board.DISPLAY

# Set text, font, and color
text = "22:10"
font = terminalio.FONT
#font = bitmap_font.load_font("/fonts/IndieFlower-117.bdf")
color = 0x0000FF

# Create the text label
text_area = label.Label(font, text=text, color=color,scale=8)

# Set the location
text_area.x = 0
text_area.y = 60



# Show it
display.show(text_area)

seg = 0
# Loop forever so you can enjoy your image
text_area.scale = 5
while True:
    sleep(0.4)
    seg += 1
    if seg%2:
        point = ' '
    else:
        point = ':'
    text_area.text = '{:02d}{}{:02d}{}{:02d}'.format(r.datetime.tm_hour,point, r.datetime.tm_min,point,r.datetime.tm_sec)
    time = r.datetime
    



