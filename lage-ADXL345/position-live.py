#!/usr/bin/python3
# coding=utf-8
# position2file.py
#
# nutzt die aus dem Beschleunigungssensor ADXL345 gelesenen Lagewerte
# um den Wohnwagen über LEDS auszurichten
#
# Schreibt die Werte zudem in eine Datei zum Debuggen
#
# Aufruf-Parameter
# position-live.py >file>
# <file> = 1: Werte werden in ein File geschrieben
#
#-------------------------------------------------------------------------------

import time, datetime
import board
import busio
import adafruit_adxl34x
import statistics
import signal
import sys
from mcp23017 import mcp23017,pin
from time import sleep
import RPi.GPIO as GPIO
import os

# ------------------------
# init
# ------------------------

# initiate 3-axis-sensor
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# initiate GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT, initial=0)
GPIO.setup(16, GPIO.OUT, initial=0)
GPIO.setup(18, GPIO.OUT, initial=0)
GPIO.setup(20, GPIO.OUT, initial=0)
GPIO.setup(23, GPIO.OUT, initial=0)
GPIO.setup(24, GPIO.OUT, initial=0)

# initiate GPIO port expander
mymcp=mcp23017()

# global variables
programmstatus = 1
# Correction of axis values
adjustX = 0
adjustY = 0
adjustZ = 0
# what is still considered horizontal
offsetX = 0
offsetY = 0
# When should the approach color be selected?
approximationX = 0
approximationY = 0

# -------------------------
# functions 
# -------------------------

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	positionExit()

def deleteFile():
	try:
		os.remove("/home/pi/CaravanPi/values/lage-live")
		return(0)
	except:
		# Schreibfehler
		print ("positionExit: The file could not be deleted.")
		return(-1)


def positionExit():
	# ProgramStatus stetzen
	programmStatus = 0
	
	# LEDs ausschalten
	setAlle(99)
	
	return

# -------------------------
# 3-axis-sensor 
# -------------------------

def readAdjustment():
	try:
		dateiName = "/home/pi/CaravanPi/defaults/adjustmentPosition"
		file = open(dateiName)
		strAdjustX = file.readline()
		strAdjustY = file.readline()
		strAdjustZ = file.readline()
		strOffsetX = file.readline()
		strOffsetY = file.readline()
		strApproximationX = file.readline()
		strApproximationY = file.readline()
		file.close()
		adjustX = float(strAdjustX)
		adjustY = float(strAdjustY)
		adjustZ = float(strAdjustZ)
		offsetX = float(strOffsetX)
		offsetY = float(strOffsetY)
		approximationX = float(strApproximationX)
		approximationY = float(strApproximationY)
		return(adjustX, adjustY, adjustZ, offsetX, offsetY, approximationX, approximationY)
	except:
		# Lesefehler
		print ("readAdjustment: The file could not be read.")
		return(0,0,0,0,0,0,0)

def write2file(x, y, z):
	try:
		dateiName = "/home/pi/CaravanPi/values/lage-live"
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strX = '{:.6f}'.format(x)
		strY = '{:.6f}'.format(y)
		strZ = '{:.6f}'.format(z)
		file.write("\n"+ str_from_time_now + " " + strX + " " + strY + " " + strZ)
		file.close()
		return 0
	except:
		print ("write2file: The file could not be written.")
		return -1


# -------------------------
# LED management
# -------------------------

def setPinMCP(pinRed, pinGreen, pinBlue, state):
	# state:
	#	2	zu hoch				blau
	#	1	knapp zu hoch		gelb
	#	0	waagrecht			weiß
	#	-1	knapp zu niedrig	gelb
	#	-2 	zu niedrig			grün
	#
	pinRed.disable();
	pinBlue.disable();
	pinGreen.disable();

	if state == 99:
		return
	elif state == 2:
		pinRed.disable();
		pinBlue.enable();
		pinGreen.disable()
	elif state == 1 or state == -1:
		pinRed.disable();
		pinBlue.enable();
		pinGreen.enable()
	elif state == 0:
		pinRed.enable()
		pinBlue.enable();
		pinGreen.enable();
	elif state == -2:
		pinRed.disable();
		pinBlue.disable()
		pinGreen.enable();
	return

def setPinGPIO(nrRed, nrGreen, nrBlue, state):
	GPIO.output(nrRed, 0)
	GPIO.output(nrGreen, 0)
	GPIO.output(nrBlue, 0)

	if state == 99:
		return
	elif state == 2:
		GPIO.output(nrRed, 0)
		GPIO.output(nrBlue, 1)
		GPIO.output(nrGreen, 0)
	elif state == 1 or state == -1:
		GPIO.output(nrRed, 0)
		GPIO.output(nrBlue, 1)
		GPIO.output(nrGreen, 1)
	elif state == 0:
		GPIO.output(nrRed, 1)
		GPIO.output(nrBlue, 1)
		GPIO.output(nrGreen, 1)
	elif state == -2:
		GPIO.output(nrRed, 0)
		GPIO.output(nrBlue, 0)
		GPIO.output(nrGreen, 1)
	return

def getHR():
	pinRed=pin(mymcp,"gpiob",3)
	pinGreen=pin(mymcp,"gpiob",4)
	pinBlue=pin(mymcp,"gpiob",5)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def getHL():
	pinRed=pin(mymcp,"gpioa",3)
	pinGreen=pin(mymcp,"gpioa",4)
	pinBlue=pin(mymcp,"gpioa",5)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def getVR():
	pinRed=pin(mymcp,"gpiob",0)
	pinGreen=pin(mymcp,"gpiob",1)
	pinBlue=pin(mymcp,"gpiob",2)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def getVL():
	pinRed=pin(mymcp,"gpioa",0)
	pinGreen=pin(mymcp,"gpioa",1)
	pinBlue=pin(mymcp,"gpioa",2)
	
	return ("mcp", pinRed, pinGreen, pinBlue)


def getZR():
	nrRed=16
	nrGreen=20
	nrBlue=12
	
	return("gpio", nrRed, nrGreen, nrBlue)


def getZL():
	nrRed=23
	nrGreen=24
	nrBlue=18
	
	return("gpio", nrRed, nrGreen, nrBlue)


def getVo():
	pinRed=pin(mymcp,"gpioa",6)
	pinGreen=pin(mymcp,"gpioa",7)
	pinBlue=pin(mymcp,"gpiob",7)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def setPins(position,state):
	if position == "HR":
		pins=getHR()
	elif position == "HL":
		pins=getHL()
	elif position == "VR":
		pins=getVR()
	elif position == "VL":
		pins=getVL()
	elif position == "ZR":
		pins=getZR()
	elif position == "ZL":
		pins=getZL()
	elif position == "Vo":
		pins=getVo()
	
	if pins[0] == "mcp":
		setPinMCP(pins[1], pins[2], pins[3], state)
	elif pins[0] == "gpio":
		setPinGPIO(pins[1], pins[2], pins[3], state)


def setAlle(state):
	positions = ['HR', 'HL', 'ZR','ZL', 'VR', 'VL', 'Vo']
	for pos in positions:
		setPins(pos,state)
	return
	
def stateCheck(x, y, value)
	return

def LED(x, y, z)
	#*************************************
	# Einstellen der LEDs
	#*************************************
	
	# x  < 0: hinten tiefer
	# y > 0: rechts tiefer
	
	if (x  < 0 and y > 0):
		# Wagen ist vorne und rechts tiefer
		positions = ['HR', 'VL']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZL', 'HL']
		for pos in positions:
			setPins(pos,2)
		positions = ['ZR','VR']
		for pos in positions:
			setPins(pos,-2)
		setPins('Vo',-2)
	elif (x  < 0 and y < 0):
		# Wagen ist vorne und links tief
		positions = ['VR', 'HL']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZR', 'HR']
		for pos in positions:
			setPins(pos,2)
		positions = ['ZL','VL']
		for pos in positions:
			setPins(pos,-2)
		setPins('Vo',-2)
	elif (x  < 0 and y == 0):
		# Wagen ist vorne tief und rechts und links in Waage
		positions = ['VR', 'VL']
		for pos in positions:
			setPins(pos,-2) 
		positions = ['ZR', 'ZL']
		for pos in positions:
			setPins(pos,0)
		positions = ['HR','HL']
		for pos in positions:
			setPins(pos,2)
		setPins('Vo',-2)
	elif (x  > 0 and y > 0):
		# Wagen ist hinten und rechts tief
		positions = ['VR', 'HL']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZR', 'HR']
		for pos in positions:
			setPins(pos,-2)
		positions = ['ZL','VL']
		for pos in positions:
			setPins(pos,2)
		setPins('Vo',2)
	elif (x  > 0 and y < 0):
		# Wagen ist hinten und links tief
		positions = ['VL', 'HR']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZR', 'VR']
		for pos in positions:
			setPins(pos,2)
		positions = ['ZL','HL']
		for pos in positions:
			setPins(pos,2)
		setPins('Vo',-2)
	elif (x  > 0 and y == 0):
		# Wagen ist hinten tief und rechts und links in Waage
		positions = ['VR', 'VL']
		for pos in positions:
			setPins(pos,2) 
		positions = ['ZR', 'ZL']
		for pos in positions:
			setPins(pos,0)
		positions = ['HR','HL']
		for pos in positions:
			setPins(pos,-2)
		setPins('Vo',2)
	elif (x == 0 and y > 0):
		# Wagen ist vorne und hinten in Waage und rechts tief
		positions = ['VR', 'ZR', 'HR']
		for pos in positions:
			setPins(pos,-2) 
		positions = ['VL', 'ZL', 'HL']
		for pos in positions:
			setPins(pos,2)
		setPins('Vo',0)
	elif (x == 0 and y < 0):
		# Wagen ist ist vorne und hinten in Waage und links tief
		positions = ['VR', 'ZR', 'HR']
		for pos in positions:
			setPins(pos,2) 
		positions = ['VL', 'ZL', 'HL']
		for pos in positions:
			setPins(pos,-2)
		setPins('Vo',0)
	elif (x == 0 and y == 0):
		# Wagen ist vollstaendig in der Waage
		setAlle(0)
		
	return
	
	
# -------------------------
# main 
# -------------------------

# initiate signal handler
signal.signal(signal.SIGINT, signal_handler)

# process call parameters
writeFile = 0
if len(sys.argv) >= 2:
    writeFile = int(sys.argv[1])

# delete file to start clean
deleteFile()

# read defaults
(adjustX, adjustY, adjustZ, offsetX, offsetY, approximationX, approximationY) = readAdjustment()

programmStatus = 1
# Lagewerte in Schleife
while programmStatus == 1:
	i=0
	arrayX = []
	arrayY = []
	arrayZ = []
	while i < 500:
		(x, y, z) = accelerometer.acceleration
		arrayX.append(x)
		arrayY.append(y)
		arrayZ.append(z)
		i += 1
		# no sleep here, because the accuracy of Python/Raspberry Sleep is not sufficient anyway
		# instead a high number of passes over the loop variable
		
	x = statistics.median(arrayX) - adjustX
	y = statistics.median(arrayY) - adjustY
	z = statistics.median(arrayZ) - adjustZ
	
	if writeFile == 1:
		write2file(x, y, z)
		

# Programmende durch Veränderung des programmStatus
print("Programm wurde beendet.")
