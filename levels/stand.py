#!/usr/bin/python3
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT, initial=1)
GPIO.setup(1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


print("Start")

zaehler = 0
while True:
	print("#1: ", GPIO.input(1), "#13: ", GPIO.input(13), "#22: ", GPIO.input(22), "#27: ", GPIO.input(27))
	sleep(1)