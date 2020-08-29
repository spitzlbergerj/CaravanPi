#!/usr/bin/env python

import sys
import os
import time
import RPi.GPIO as io
import subprocess

# Exception Handling
import atexit
import signal

# GPIO konfigurieren
io.setmode(io.BCM)

#Variablen deklarieren
PIR_PIN = 4
LED_PIN = 27
SHUTOFF_DELAY = 120 # Default 2 Minutzen = 120 Sekundennds
turned_off = False
LED_signal = True
motion_count = 0
dateiname = '/home/pi/pir.log'
dateiname_alt = '/home/pi/pir-alt.log'
loglevel = 0

# Funktionen
def signal_term_handler(signal, frame):
    print('got SIGTERM')
    io.cleanup()
    sys.exit(0)

def goodbye():
    print('Goodbye')
    io.cleanup()

def main():
    global turned_off
    global motion_count

    last_motion_time = time.time()

    print('start - Warten auf erstes Event', flush=True)

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            motion_count += 1
            if LED_signal:
                io.output(LED_PIN, io.HIGH)
            if loglevel > 1: 
                print(motion_count, ' ', end='', flush=True)
            if turned_off:
                turn_on()
                if loglevel > 0: 
                   print(time.strftime(' on %H:%M:%S '), end='', flush=True)
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turn_off()
                motion_count = 0
                if loglevel > 0: 
                   print(time.strftime(" off %H:%M:%S "), flush=True)
            if not turned_off and time.time() > (last_motion_time + 1):
                if LED_signal:
                    io.output(LED_PIN, io.LOW)
        time.sleep(.1)

def turn_on():
    global turned_off

    turned_off = False
    # time.sleep(.1)

    # bei 7 Zoll Raspian Display
    # subprocess.call("echo 0 > /sys/class/backlight/rpi_backlight/bl_power", shell=True)
    # bei HDMI Monitor 
    subprocess.call("vcgencmd display_power 1", shell=True)

def turn_off():
    global turned_off

    turned_off = True

    # bei 7 Zoll Raspian Display
    # subprocess.call("echo 1 > /sys/class/backlight/rpi_backlight/bl_power", shell=True)
    # bei HDMI Monitor 
    subprocess.call("vcgencmd display_power 0", shell=True)


def LED_blink():
	io.output(LED_PIN, io.LOW)
	time.sleep(.05)
	io.output(LED_PIN, io.HIGH)
	time.sleep(.05)
	io.output(LED_PIN, io.LOW)
	time.sleep(.05)
	io.output(LED_PIN, io.HIGH)
	time.sleep(.05)
	io.output(LED_PIN, io.LOW)
	time.sleep(.05)
	io.output(LED_PIN, io.HIGH)
	time.sleep(.05)
	io.output(LED_PIN, io.LOW)
	time.sleep(.05)
	io.output(LED_PIN, io.HIGH)
	time.sleep(.05)
	io.output(LED_PIN, io.LOW)
	time.sleep(.05)
	io.output(LED_PIN, io.HIGH)
	time.sleep(.05)
	io.output(LED_PIN, io.LOW)

# --------------------------------------------------------------------
# los gehts 
#---------------------------------------------------------------------

# Abfangen von SIGTERM
signal.signal(signal.SIGTERM, signal_term_handler)

# Abfangen von KeyboardInterrupt CRTL-C
atexit.register(goodbye)

# altes Log retten und dann Ausgabe umlenken
os.rename(dateiname, dateiname_alt)
sys.stdout = open(dateiname, 'w')

# Parameter verarbeiten
SHUTOFF_DELAY = 2 # seconds
if len(sys.argv) >= 2:
    SHUTOFF_DELAY = int(sys.argv[1])
    print("delay auf Parameter gesetzt")
print("Delay: ", SHUTOFF_DELAY)

if len(sys.argv) >= 3:
    if int(sys.argv[2]) == 0:
       LED_signal = False
       print("Signalisierung durch LED auf Parameter gesetzt")
print("LED Signalisierung: ", LED_signal)

if len(sys.argv) == 4:
    loglevel = int(sys.argv[3])
    print("LogLevel auf Parameter gesetzt")
print("Loglevel: ", loglevel)

# IO setzen für LED und PIR
io.setup(PIR_PIN, io.IN)
io.setup(LED_PIN, io.OUT)

# Bootvorgang abwarten
time.sleep(60)

# erst mal ausschalten
if loglevel > 0: 
    print(time.strftime("turn initially off %H:%M:%S "), flush=True)
LED_blink()
time.sleep(.05)
turn_off()

# und los gehts
if loglevel > 0: 
    print(time.strftime("start main routine %H:%M:%S "), flush=True)
main()

