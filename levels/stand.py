#!/usr/bin/python3
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT, initial=1)
GPIO.setup(0, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


print("Start")

zaehler = 0
while True:
	print("#0: ", GPIO.input(0), "#1: ", GPIO.input(1), "#8: ", GPIO.input(8),"#9: ", GPIO.input(9))
	print("#10: ", GPIO.input(10), "#11: ", GPIO.input(11),"#13: ", GPIO.input(13))
	print("#18: ", GPIO.input(18), "#19: ", GPIO.input(19), "#22: ", GPIO.input(22), "#27: ", GPIO.input(27))
	print("----")
	sleep(1)