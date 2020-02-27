#!/usr/bin/python
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_DHT

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    sensor  = 11 # 传感器型号
    pin = 22 # 针脚
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        Temp = 'Temp={0:0.1f}*'.format(temperature)
        H = 'Humidity={0:0.1f}%'.format(humidity)

    now = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    draw.text((x, top),       str(now),  font=font, fill=255)
    draw.text((x, top+8),     str(Temp), font=font, fill=255)
    draw.text((x, top+16),     str(H), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
