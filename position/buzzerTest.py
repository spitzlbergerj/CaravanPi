#!/usr/bin/python3
# coding=utf-8
# buttontest.py
#
# Buzzer testen
#
#-------------------------------------------------------------------------------

import time
from time import sleep
import RPi.GPIO as io

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
	while i < 30:
		io.output(BUZZER_PIN, io.HIGH)
		sleep(.1)
		io.output(BUZZER_PIN, io.LOW)
		sleep(.9)
		i+=1
		
	# buzzer beeps rapidly to signal imminent measurement
	i=0
	while i < 10:
		io.output(BUZZER_PIN, io.HIGH)
		sleep(.1)
		io.output(BUZZER_PIN, io.LOW)
		sleep(.1)
		i+=1
		
	# long beep of the buzzer to signal completion
	io.output(BUZZER_PIN, io.HIGH)
	sleep(2)
	io.output(BUZZER_PIN, io.LOW)
	io.cleanup()
	

if __name__ == "__main__":
	main()
