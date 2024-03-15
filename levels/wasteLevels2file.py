#!/usr/bin/python3
# coding=utf-8
# wasteLevels2filePeriodic.py
#
# Liest die GPIO Ports der MCP23017 zur Bestimmung der Fülllevel von Tanks
#
# Aufruf-Parameter
# wasteLevels2filePeriodic.py -f
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
# nutzt die Python library von Adafruit für MCP23017
# https://learn.adafruit.com/using-mcp23008-mcp23017-with-circuitpython/python-circuitpython
# github
# https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx
# Dokumentation
# https://readthedocs.org/projects/adafruit-circuitpython-mcp230xx/downloads/pdf/latest/
#-------------------------------------------------------------------------------

import time, datetime
import sys
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
shortOptions = 'hfst:'
longOptions = ['help', 'file', 'screen', 'tank=']

# -------------------------
# unterschiedliche Tanks
# 1 = Frischwasser
# 2 = Fäkalien
# -------------------------
tank = 2

# -------------------------
# Zeiten
# -------------------------
waitAfterReadingSeconds = 600


# -------------------------
# Funktionen
# -------------------------
def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h -f -s -t <nr>")
	print ("  -h        show this guide")
	print ("  -f        write values to file ", filePosition)
	print ("  -s        display values on this screen\n")
	print ("  -t <nr>   welcher Tank soll abgefragt werden\n")

	
def main():
	# -------------------------
	# main 
	# -------------------------

	global mymcp1, mymcp2
	global tank

	# -----------------------------------------------
	# Initialize the I2C bus and the GPIO port expander
	# -----------------------------------------------
	i2c = busio.I2C(board.SCL, board.SDA)
	mymcp1=MCP23017(i2c, address=0x20)
	mymcp2=MCP23017(i2c, address=0x21)

	# -----------------------------------------------
	# Initialize the GPIO ports
	# -----------------------------------------------
	GPIO.setmode(GPIO.BCM)

	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeFile = 0
	displayScreen = 0

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
		elif o == "--tank" or o == "-t":
			tank = int(a)
			print("Tanknummer ", '{:.0f}'.format(tank))
		elif o == "--file" or o == "-f":
			print("output also to file ", filePosition)
			writeFile = 1
		elif o == "--screen" or o == "-s":
			print("output also to this screen")
			displayScreen = 1

	for a in args:
		print("further argument: ", a)
	

	cplib = CaravanPiFiles()

	# -------------------------
	# read defaults
	# -------------------------
	(literLevel1, literLevel2, literLevel3, literLevel4) = cplib.readFillLevels(tank)

	# -------------------------
	# initialize IO Pins on MCP23017
	# pin number from 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4)
	# Füllstände: 1 an Pin GPIOB3 (11), ..., 4 an Pin GPIOB6 (14)
	# -------------------------

	fillingLevel1 = mymcp2.get_pin(11)
	fillingLevel1.direction = digitalio.Direction.INPUT

	fillingLevel2 = mymcp2.get_pin(12)
	fillingLevel2.direction = digitalio.Direction.INPUT

	fillingLevel3 = mymcp2.get_pin(13)
	fillingLevel3.direction = digitalio.Direction.INPUT

	fillingLevel4 = mymcp2.get_pin(14)
	fillingLevel4.direction = digitalio.Direction.INPUT

	# -------------------------
	# Main 
	# -------------------------

	try:
		while True:
			if displayScreen == 1:
				print("Level prüfen ...")

			level1contact = fillingLevel1.value
			level2contact = fillingLevel2.value
			level3contact = fillingLevel3.value
			level4contact = fillingLevel4.value

			if displayScreen == 1:
				print("Level 1 erreicht? {0}".format(level1contact), literLevel1, " Liter")
				print("Level 2 erreicht? {0}".format(level2contact), literLevel2, " Liter")
				print("Level 3 erreicht? {0}".format(level3contact), literLevel3, " Liter")
				print("Level 4 erreicht? {0}".format(level4contact), literLevel4, " Liter")

			if level4contact:
				actLiter = literLevel4
			elif level3contact:
				actLiter = literLevel3
			elif level2contact:
				actLiter = literLevel2
			elif level1contact:
				actLiter = literLevel1
			else:
				actLiter = 0

			if displayScreen == 1:
				if actLiter < literLevel1:
					print("Füllmenge gering")
				else:
					print("mind. "+str(actLiter)+" Liter im Tank")

			# Sensorwerte verarbeiten
			cplib.handle_sensor_values(
				displayScreen == 1,								# Anzeige am Bildschirm?
				"tankfuellgrad",								# sensor_name = Datenbankname
				f"waste-{tank}",								# sensor_id = Filename und Spalte in der Datenbank
				[
					"fuellgrad",
				],											# Liste Spaltennamen
				(
					actLiter,
				)											# Tupel Sensorwerte
			)    


			time.sleep(waitAfterReadingSeconds)

	except KeyboardInterrupt:
		GPIO.cleanup()
	except:
		print("unprocessed Error:", sys.exc_info()[0])
		GPIO.cleanup()

	# -------------------------
	# Cleaning at the end
	# -------------------------
	GPIO.cleanup()

if __name__ == "__main__":
	main()
