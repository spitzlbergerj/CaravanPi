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

	cpfunclib.play_alarm_single(io, BUZZER_PIN, 1)
	time.sleep(1)
	cpfunclib.play_alarm_single(io, BUZZER_PIN, 2)
	time.sleep(1)
	cpfunclib.play_alarm_single(io, BUZZER_PIN, 3)
	time.sleep(1)

	cpfunclib.play_alarm_single(io, BUZZER_PIN, 99)
	time.sleep(1)


	cpfunclib.play_melody(io, BUZZER_PIN, 'success')

	

if __name__ == "__main__":
	main()
