#!/usr/bin/env python

import sys
import os
import time
import RPi.GPIO as io

# GPIO konfigurieren
io.setmode(io.BCM)

#Variablen deklarieren
PIR_PIN = 27
LED_PIN = 21

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

    print('start - Warten auf erstes Event', flush=True)

    while True:
        if io.input(PIR_PIN):
            io.output(LED_PIN, io.HIGH)
            print(time.strftime('Bewegung erkannt %H:%M:%S '), flush=True)
            time.sleep(1)
            io.output(LED_PIN, io.LOW)
        time.sleep(.5)

# --------------------------------------------------------------------
# los gehts 
#---------------------------------------------------------------------

# Abfangen von SIGTERM
signal.signal(signal.SIGTERM, signal_term_handler)

# Abfangen von KeyboardInterrupt CRTL-C
atexit.register(goodbye)

# IO setzen für LED und PIR
io.setup(PIR_PIN, io.IN)
io.setup(LED_PIN, io.OUT)

# und los gehts
main()
