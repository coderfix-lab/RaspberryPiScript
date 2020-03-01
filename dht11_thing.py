import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_DHT

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import sys
from linkkit import linkkit
import threading
import traceback
import inspect
import time
import logging

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


# config log
__log_format = '%(asctime)s-%(process)d-%(thread)d - %(name)s:%(module)s:%(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=__log_format)

class CustomerThing(object):
    def __init__(self):
        self.__linkkit = linkkit.LinkKit(
            host_name="cn-shanghai",
            product_key="****",
            device_name="***",
            device_secret="&*****")
        self.__linkkit.enable_logger(logging.ERROR)
        self.__linkkit.on_device_dynamic_register = self.on_device_dynamic_register
        self.__linkkit.on_connect = self.on_connect
        self.__linkkit.on_disconnect = self.on_disconnect
        self.__linkkit.on_topic_message = self.on_topic_message
        self.__linkkit.on_subscribe_topic = self.on_subscribe_topic
        self.__linkkit.on_unsubscribe_topic = self.on_unsubscribe_topic
        self.__linkkit.on_publish_topic = self.on_publish_topic
        self.__linkkit.on_thing_enable = self.on_thing_enable
        self.__linkkit.on_thing_disable = self.on_thing_disable
        self.__linkkit.on_thing_event_post = self.on_thing_event_post
        self.__linkkit.on_thing_prop_post = self.on_thing_prop_post
        self.__linkkit.on_thing_prop_changed = self.on_thing_prop_changed
        self.__linkkit.on_thing_call_service = self.on_thing_call_service
        self.__linkkit.on_thing_raw_data_post = self.on_thing_raw_data_post
        self.__linkkit.on_thing_raw_data_arrived = self.on_thing_raw_data_arrived
        self.__linkkit.thing_setup("model.json")
        self.__linkkit.config_device_info("Eth|03ACDEFF0032|Eth|03ACDEFF0031")
        self.__call_service_request_id = 0
        self.__linkkit.connect_async()
        
    def on_device_dynamic_register(self, rc, value, userdata):
        if rc == 0:
            print("dynamic register device success, value:" + value)
        else:
            print("dynamic register device fail, message:" + value)

    def on_connect(self, session_flag, rc, userdata):
        print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))

    def on_disconnect(self, rc, userdata):
        print("on_disconnect:rc:%d,userdata:" % rc)

    def on_topic_message(self, topic, payload, qos, userdata):
        print("on_topic_message:" + topic + " payload:" + str(payload) + " qos:" + str(qos))
        pass

    def on_subscribe_topic(self, mid, granted_qos, userdata):
        print("on_subscribe_topic mid:%d, granted_qos:%s" %
              (mid, str(','.join('%s' % it for it in granted_qos))))
        pass

    def on_unsubscribe_topic(self, mid, userdata):
        print("on_unsubscribe_topic mid:%d" % mid)
        pass

    def on_publish_topic(self, mid, userdata):
        print("on_publish_topic mid:%d" % mid)

    def on_thing_prop_changed(self, params, userdata):
        print("on_thing_prop_changed params:" + str(params))

    def on_thing_enable(self, userdata):
        print("on_thing_enable")

    def on_thing_disable(self, userdata):
        print("on_thing_disable")

    def on_thing_event_post(self, event, request_id, code, data, message, userdata):
        print("on_thing_event_post event:%s,request id:%s, code:%d, data:%s, message:%s" %
              (event, request_id, code, str(data), message))
        pass

    def on_thing_prop_post(self, request_id, code, data, message,userdata):
        print("on_thing_prop_post request id:%s, code:%d, data:%s message:%s" %
              (request_id, code, str(data), message))

    def on_thing_raw_data_arrived(self, payload, userdata):
        print("on_thing_raw_data_arrived:%s" % str(payload))

    def on_thing_raw_data_post(self, payload, userdata):
        print("on_thing_raw_data_post: %s" % str(payload))

    def on_thing_call_service(self, identifier, request_id, params, userdata):
        print("on_thing_call_service identifier:%s, request id:%s, params:%s" %
              (identifier, request_id, params))
        self.__call_service_request_id = request_id
        pass

    def update(self,CurrentTemperature,CurrentHumidity):
        prop_data = {
                        "CurrentTemperature": float(CurrentTemperature),
                        "CurrentHumidity": float(CurrentHumidity)
                    }
        self.__linkkit.thing_post_property(prop_data)

if __name__ == "__main__":
    custom_thing = CustomerThing()
    time.sleep(3)
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        sensor  = 11 # 传感器型号
        pin = 22 # 针脚
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            Temp = '{0:0.1f}'.format(temperature)
            H = '{0:0.1f}'.format(humidity)

        now = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        draw.text((x, top),       str(now),  font=font, fill=255)
        draw.text((x, top+8),     str("Temp="+Temp), font=font, fill=255)
        draw.text((x, top+16),     str("Humidity="+H+"%"), font=font, fill=255)

        custom_thing.update(Temp,H)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(2)

