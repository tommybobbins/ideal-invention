# This example shows you a simple, non-interrupt way of reading Pico Display's buttons with a loop that checks to see if buttons are pressed.
# If you have a Display Pack 2.0" or 2.8" use DISPLAY_PICO_DISPLAY_2 instead of DISPLAY_PICO_DISPLAY

import time
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
from pimoroni import RGBLED
from micropython import const
import qrcode
import sys
import asyncio
import aioble
import bluetooth
import binascii
import random
import struct
import array
import re

devlist= []
regex = "Polar 360"

async def scan_devices():
    
#     print ("Inside scan_devices")
    async with aioble.scan(3000, interval_us=30000, window_us=30000, active=True) as scanner:
        devlist = {}
        async for result in scanner:
            print(result)
            if result.name():
#                 print(result.name())
                if re.search(regex, result.name()):
#                     print(result, '::', binascii.hexlify(result.device.addr,':'), '::', result.name(), '::', result.rssi, '::')
#                     address = binascii.hexlify(result.device.addr.decode())
                    [address, name, rssi, services] = [ binascii.hexlify(result.device.addr,':') , result.name(), result.rssi, result.services() ]
                    devlist[name] = address
    return devlist


async def parse_devices():
#     print ("Inside parse_devices")
    devices = await scan_devices()
    polar_devices = []
    for dev in devices:
        replaced = dev.replace("Polar 360 ","")
#         print(f"Polar Device = {replaced}")
        polar_devices.append(replaced)
    return polar_devices

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

# Set up the RGB LED For Display Pack and Display Pack 2.0":
led = RGBLED(6, 7, 8)

# For Display Pack 2.8" uncomment the line below and comment out the line above:
# led = RGBLED(26, 27, 28)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
LIGHTEST = display.create_pen(208, 208, 208)
LIGHT = display.create_pen(160, 168, 64)
DARK = display.create_pen(112, 128, 40)
DARKEST = display.create_pen(64, 80, 16)

WIDTH, HEIGHT = display.get_bounds()

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    led.set_rgb(0, 0, 0)
    display.clear()
    display.update()

def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(WHITE)
    display.rectangle(ox, oy, size, size)
    display.set_pen(BLACK)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


def show_qr(qr_text):  
    display.set_pen(WHITE)
    display.clear()
    code = qrcode.QRCode()
    code.set_text(qr_text)
    size, module_size = measure_qr_code(HEIGHT, code)
#     left = int((WIDTH // 2) - (size // 2))
    left = 10
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)

# set up
clear()

while True:
    # button logic is reversed as we're using pull-ups
    if button_a.value() == 0:                             # if a button press is detected then...
        clear() 
        led.set_rgb(48, 24, 48)
        #display.text("Button A pressed", 10, 10, 240, 4)
        display.update()
#         print("About to scan")
        try:
#             print("About to async")
            try:
#                 print("Trying")
                polar_devices=asyncio.run(parse_devices())
#                 print("Back from Polar Devices")
                show_qr(polar_devices[0])
                display.update()
                led.set_rgb(0, 2, 0)# update the display
                time.sleep(60)                                     # pause for a sec
                clear()
            except:
                polar_devices=[]
#                 print("No Polar device found")
                led.set_rgb(22 , 0, 0)
                display.clear()
                show_qr("FAIL")
                #display.text("No Polar found", 10, 10, 240, 4)
                display.update()
                time.sleep(10)
                clear()
        except: #
            led.set_rgb(24, 0, 0)# update the display
            time.sleep(1)                                     # pause for a sec
            clear()
    elif button_b.value() == 0:
        clear()
        display.set_pen(CYAN)
        led.set_rgb(0, 128, 128)
        display.text("Button B pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_x.value() == 0:
        clear()
        display.set_pen(MAGENTA)
        led.set_rgb(255, 0, 255)
        display.text("Button X pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_y.value() == 0:
        clear()
        display.set_pen(YELLOW)
        led.set_rgb(255, 255, 0)
        display.text("Button Y pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    else:
        display.set_pen(GREEN)
        led.set_rgb(0, 255, 0)
        display.text("Press A to Scan", 10, 10, 240, 4)
        display.update()
        time.sleep(0.1)
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses