#!/usr/bin/python3
# coding=utf-8
# levels2file.py
#
# Liest die GPIO Ports der MCP23017 zur Bestimmung der Fülllevel von Tanks
#
# Aufruf-Parameter
# positionLive.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
# 	-t <configfile>
#
#
# freie Ports an den MCP23017
# 0x20:
# 	B0 - B6 --> #8 - #14
# 0x21:
# 	B3 - B6 --> #11 - #14
#
#-------------------------------------------------------------------------------

import time, datetime
import statistics
import signal
import sys
from time import sleep
import os
import getopt

# import for GPIO Input tactile switches
import RPi.GPIO as GPIO

# -----------------------------------------------
# libraries from CaravanPi
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

# -----------------------------------------------
# library from Adafruit
# -----------------------------------------------
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

# files
filePosition = "/home/pi/CaravanPi/values/levels"

# -------------------------
# call options 
# -------------------------
shortOptions = 'hfsl'
longOptions = ['help', 'file', 'screen', 'live']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h -f -s -l")
	print ("  -h   show this guide")
	print ("  -f   write values to file ", filePosition)
	print ("  -s   display values on this screen\n")
	print ("  -t <configfile>   welcher Tank soll abgefragt werden\n")


	
def main():
	# -------------------------
	# main 
	# -------------------------

	global mymcp1, mymcp2
	global tank
	global LED_HR, LED_HL, LED_ZR, LED_ZL, LED_VR, LED_VL, LED_Vo

	# -----------------------------------------------
	# Initialize the I2C bus and the GPIO port expander
	# -----------------------------------------------
	i2c = busio.I2C(board.SCL, board.SDA)
	mymcp1=MCP23017(i2c, address=0x20)
	mymcp2=MCP23017(i2c, address=0x21)


	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeFile = 0
	displayScreen = 0
	tank=1
	pin1=(0,0)
	pin2=(0,0)
	pin3=(0,0)
	pin4=(0,0)
	pin5=(0,0)
	pin6=(0,0)
	pin7=(0,0)
	pin8=(0,0)
	pin9=(0,0)
	pin10=(0,0)

	
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
	except getopt.GetoptError:
		print(datetime.datetime.now().strftime("%Y%m%d%H%M%S "), "ERROR: options not correct")
		usage()
		sys.exit()
	
	for o, a in opts:
		if o == "--help" or o == "-h":
			print("HELP")
			usage()
			sys.exit()
		elif o == "--file" or o == "-f":
			print("output also to file ", filePosition)
			writeFile = 1
		elif o == "--screen" or o == "-s":
			print("output also to this screen")
			displayScreen = 1
		elif o == "--screen" or o == "-l":
			print("start in live mode")
			liveMode = 1
			GPIO.output(pinLEDLive, True)


	for a in args:
		print("further argument: ", a)
	
	
	# read defaults
	#(anzahl, pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10) = CaravanPiFiles.readFillLevel(tank)

	# test für Frischwassertank tank = 1
	anzahl=4
	pin1=(1,8)
	pin2=(1,9)
	pin3=(1,10)
	pin4=(1,11)
	pin5=(0,0)
	pin6=(0,0)
	pin7=(0,0)
	pin8=(0,0)
	pin9=(0,0)
	pin10=(0,0)

	# -------------------------
	# initialize GPIO Pins
	# -------------------------

	input1 = mymcp1.get_pin(8)
	input1.direction = digitalio.Direction.INPUT

	input2 = mymcp1.get_pin(9)
	input2.direction = digitalio.Direction.INPUT

	input3 = mymcp1.get_pin(10)
	input3.direction = digitalio.Direction.INPUT

	input4 = mymcp1.get_pin(11)
	input4.direction = digitalio.Direction.INPUT

	# read sensor and adjust LEDs
	while True:
		print(datetime.datetime.now().strftime("%Y%m%d%H%M%S "))
		try:
			print("Level Input 1: {0}".format(input1.value))
			print("Level Input 2: {0}".format(input2.value))
			print("Level Input 3: {0}".format(input3.value))
			print("Level Input 4: {0}".format(input4.value))
			time.sleep(1)
		except KeyboardInterrupt:
			GPIO.cleanup()
			break
		except:
			print("unprocessed Error:", sys.exc_info()[0])
			GPIO.cleanup()
			raise
			
	GPIO.cleanup()

if __name__ == "__main__":
	main()
