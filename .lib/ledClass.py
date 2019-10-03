import time
import sys
import threading

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from mcp23017 import mcp23017,pin

class Led(object):

    # initiate GPIO port expander
    MYMCP1=mcp23017(1,0x20)
    MYMCP2=mcp23017(1,0x21)

    LED_OFF = 0
    LED_ON = 1
    LED_FLASHING = 2

    # the short time sleep to use when the led is on or off to ensure the led responds quickly to changes to blinking
    FAST_CYCLE = 0.05

    def __init__(self, mcp, gpio, led_pin):
        # create the semaphore used to make thread exit
        self.pin_stop = threading.Event()
        # the pin for the LED
        self.__mcp = led_pin
        self.__gpio = led_pin
        self.__led_pin = led_pin
        # initialise the pin and turn the led off
        self.__led_address=pin(mcp,gpio,led_pin)
        ## GPIO.setmode(GPIO.BCM)
        ## GPIO.setup(self.__led_pin, GPIO.OUT)
        # the mode for the led - off/on/flashing
        self.__ledmode = Led.LED_OFF
        # make sure the LED is off (this also initialises the times for the thread)
        self.off()
        # create the thread, keep a reference to it for when we need to exit
        self.__thread = threading.Thread(name='ledblink',target=self.__blink_pin)
        # start the thread
        self.__thread.start()

    def blink(self, time_on=0.050, time_off=1):
        # blinking will start at the next first period
        # because turning the led on now might look funny because we don't know
        # when the next first period will start - the blink routine does all the
        # timing so that will 'just work'
        self.__ledmode = Led.LED_FLASHING
        self.__time_on = time_on
        self.__time_off = time_off

    def off(self):
        self.__ledmode = self.LED_OFF
        # set the cycle times short so changes to ledmode are picked up quickly
        self.__time_on = Led.FAST_CYCLE
        self.__time_off = Led.FAST_CYCLE
        # could turn the LED off immediately, might make for a short flicker on if was blinking

    def on(self):
        self.__ledmode = self.LED_ON
        # set the cycle times short so changes to ledmode are picked up quickly
        self.__time_on = Led.FAST_CYCLE
        self.__time_off = Led.FAST_CYCLE
        # could turn the LED on immediately, might make for a short flicker off if was blinking

    def reset(self):
        # set the semaphore so the thread will exit after sleep has completed
        self.pin_stop.set()
        # wait for the thread to exit
        self.__thread.join()
        # now clean up the GPIO
        GPIO.cleanup()

    ############################################################################
    # below here are private methods
    def __turnledon(self):
        self.__led_address.enable()
        ## GPIO.output(pin, GPIO.LOW)

    def __turnledoff(self):
        self.__led_address.disable()
        ## GPIO.output(pin, GPIO.HIGH)

    # this does all the work
    # If blinking, there are two sleeps in each loop
    # if on or off, there is only one sleep to ensure quick response to blink()
    def __blink_pin(self):
        while not self.pin_stop.is_set():
            # the first period is when the LED will be on if blinking
            if self.__ledmode == Led.LED_ON or self.__ledmode == Led.LED_FLASHING: 
                self.__turnledon()
            else:
                self.__turnledoff()
            # this is the first sleep - the 'on' time when blinking
            time.sleep(self.__time_on)
            # only if blinking, turn led off and do a second sleep for the off time
            if self.__ledmode == Led.LED_FLASHING:
                self.__turnledoff()
                # do an extra check that the stop semaphore hasn't been set before the off-time sleep
                if not self.pin_stop.is_set():
                    # this is the second sleep - off time when blinking
                    time.sleep(self.__time_off)