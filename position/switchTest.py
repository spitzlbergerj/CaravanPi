#!/usr/bin/python3
# coding=utf-8
# switchTest.py
#
# Taster testen
#
#-------------------------------------------------------------------------------

import time
from time import sleep
import RPi.GPIO as GPIO

# buzzer
pinSwitch = 12

def switchInterrupt(channel):  
	print ("ACHTUNG: manuelles Waagrecht setzen in Querrichtung !!!")


def main():
	# -------------------------
	# main 
	# -------------------------

	# tactile switch
	GPIO.setmode(GPIO.BCM)
	# GPIO.setup(pinSwitch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	# GPIO.add_event_detect(pinSwitch, GPIO.RISING, callback = switchInterrupt, bouncetime = 200)
	GPIO.setup(pinSwitch, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(pinSwitch, GPIO.FALLING, callback = switchInterrupt, bouncetime = 500)

	try:
		while True:
			print("\nwarten")
			time.sleep(1)
	except KeyboardInterrupt:
		GPIO.cleanup()
		print ("\nBye")


	GPIO.cleanup()
	

if __name__ == "__main__":
	main()
