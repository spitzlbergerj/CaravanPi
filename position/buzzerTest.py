#!/usr/bin/python3
# coding=utf-8
# buttontest.py
#
# Buzzer testen
#
#-------------------------------------------------------------------------------

import time
import sys
from time import sleep
import RPi.GPIO as io

# -----------------------------------------------
# libraries from CaravanPi 
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles
from CaravanPiFunctionsClass import CaravanPiFunctions

cpfunclib = CaravanPiFunctions()

# buzzer
BUZZER_PIN = 26

def main():
	# -------------------------
	# main 
	# -------------------------

	# buzzer
	io.setmode(io.BCM)
	io.setup(BUZZER_PIN, io.OUT)
	io.output(BUZZER_PIN, io.LOW)

	# Wait 30 secondes so that any vibrations of the caravan can subside
	# during this waiting time slow beeping of the buzzer
	i=0
	while i < 3:
		io.output(BUZZER_PIN, io.HIGH)
		sleep(.1)
		io.output(BUZZER_PIN, io.LOW)
		sleep(.9)
		i+=1
		
	# buzzer beeps rapidly to signal imminent measurement
	i=0
	while i < 3:
		io.output(BUZZER_PIN, io.HIGH)
		sleep(.1)
		io.output(BUZZER_PIN, io.LOW)
		sleep(.1)
		i+=1
		
	# long beep of the buzzer to signal completion
	sleep(.5)
	io.output(BUZZER_PIN, io.HIGH)
	sleep(1)
	io.output(BUZZER_PIN, io.LOW)
	io.cleanup()
	sleep(.5)

	cpfunclib.play_melody(io, BUZZER_PIN, 'success')

	

if __name__ == "__main__":
	main()
