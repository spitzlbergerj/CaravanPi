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
import statistics
import signal
import sys
from time import sleep
import os

import board
import busio
import adafruit_adxl34x

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from mcp23017 import mcp23017,pin
from ledClass import Led

# -----------------------------------------------
# global variables
# -----------------------------------------------
# initiate 3-axis-sensor
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# initiate GPIO port expander
mymcp1=mcp23017(1,0x20)
mymcp2=mcp23017(1,0x21)

# Correction of axis values
adjustX = 0
adjustY = 0
adjustZ = 0
# what is still considered horizontal
toleranceX = 0
toleranceY = 0
# When should the approach color be selected?
approximationX = 0
approximationY = 0

# files
filePositionLive = "/home/pi/CaravanPi/values/positionLive"
fileAdjustments = "/home/pi/CaravanPi/defaults/adjustmentPosition"

# LED threads
LED_HR = [None, None, None]
LED_HL = [None, None, None]
LED_ZR = [None, None, None]
LED_ZL = [None, None, None]
LED_VR = [None, None, None]
LED_VL = [None, None, None]
LED_Vo = [None, None, None]

# -------------------------
# 3-axis-sensor 
# -------------------------

def deleteFile():
	global filePositionLive
	
	try:
		os.remove(filePositionLive)
		return(0)
	except:
		# Schreibfehler
		# print ("positionExit: The file could not be deleted.")
		return(-1)

def readAdjustment():
	global fileAdjustments
	
	try:
		dateiName = fileAdjustments
		file = open(dateiName)
		strAdjustX = file.readline()
		strAdjustY = file.readline()
		strAdjustZ = file.readline()
		strtoleranceX = file.readline()
		strtoleranceY = file.readline()
		strApproximationX = file.readline()
		strApproximationY = file.readline()
		file.close()
		adjustX = float(strAdjustX)
		adjustY = float(strAdjustY)
		adjustZ = float(strAdjustZ)
		toleranceX = float(strtoleranceX)
		toleranceY = float(strtoleranceY)
		approximationX = float(strApproximationX)
		approximationY = float(strApproximationY)
		return(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY)
	except:
		# Lesefehler
		print ("readAdjustment: The file could not be read.")
		return(0,0,0,0,0,0,0)

def write2file(x, y, z, adjustX, adjustY, adjustZ, lastX, secondLastX):
	global filePositionLive
	
	try:
		dateiName = filePositionLive
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strX = '{:.6f}'.format(x)
		strY = '{:.6f}'.format(y)
		strZ = '{:.6f}'.format(z)
		strAdjustX = '{:.6f}'.format(adjustX)
		strAdjustY = '{:.6f}'.format(adjustY)
		if (lastX == None):
			strLastX = ""
		else:
			strLastX = '{:.6f}'.format(lastX)
		if (secondLastX == None):
			strSecondLastX = ""
		else:
			strSecondLastX = '{:.6f}'.format(secondLastX)

		valueStr = "\n"+ str_from_time_now + " adjusted & tolerant: " + strAdjustX + " " + strAdjustY + " original: " + strX + " " + strY + " " + strZ + " last and second last X: " + strLastX + " " + strSecondLastX

		file.write(valueStr)
		file.close()

		print(valueStr)
		
		return 0
	except:
		print("write2file: The file could not be written - unprocessed Error:", sys.exc_info()[0])
		raise
		return -1

# -------------------------
# adjust Threats for LEDs
# -------------------------

def setupHR():
	pinRed=Led(mymcp1,"gpiob",3)
	pinGreen=Led(mymcp1,"gpiob",4)
	pinBlue=Led(mymcp1,"gpiob",5)
	
	return([pinRed, pinGreen, pinBlue])


def setupHL():
	pinRed=Led(mymcp1,"gpioa",3)
	pinGreen=Led(mymcp1,"gpioa",4)
	pinBlue=Led(mymcp1,"gpioa",5)
	
	return([pinRed, pinGreen, pinBlue])


def setupVR():
	pinRed=Led(mymcp1,"gpiob",0)
	pinGreen=Led(mymcp1,"gpiob",1)
	pinBlue=Led(mymcp1,"gpiob",2)
	
	return([pinRed, pinGreen, pinBlue])


def setupVL():
	pinRed=Led(mymcp1,"gpioa",0)
	pinGreen=Led(mymcp1,"gpioa",1)
	pinBlue=Led(mymcp1,"gpioa",2)
	
	return ([pinRed, pinGreen, pinBlue])


def setupZR():
	pinRed=Led(mymcp2,"gpioa",5)
	pinGreen=Led(mymcp2,"gpioa",4)
	pinBlue=Led(mymcp2,"gpioa",3)
	
	return ([pinRed, pinGreen, pinBlue])


def setupZL():
	pinRed=Led(mymcp2,"gpioa",2)
	pinGreen=Led(mymcp2,"gpioa",1)
	pinBlue=Led(mymcp2,"gpioa",0)
	
	return ([pinRed, pinGreen, pinBlue])


def setupVo():
	pinRed=Led(mymcp1,"gpioa",6)
	pinGreen=Led(mymcp1,"gpioa",7)
	pinBlue=Led(mymcp1,"gpiob",7)
	
	return([pinRed, pinGreen, pinBlue])


# -------------------------
# LED management
# -------------------------

def ledOff():
	# LEDs ausschalten
	setAlle(99)
	return


def setPinMCP(pinRed, pinGreen, pinBlue, state):
	# state:
	#	2	zu hoch				blau
	#	1	knapp zu hoch		gelb
	#	0	waagrecht			weiß
	#	-1	knapp zu niedrig	gelb
	#	-2 	zu niedrig			grün
	#	99						LED aus
	#
	pinRed.off();
	pinBlue.off();
	pinGreen.off();

	if state == 99:
		return
	elif state == 2:
		pinBlue.on()
	elif state == 1:
		pinBlue.blink(0.1, 0.2)
	elif state == 0:
		pinRed.on()
	elif state == -1:
		pinGreen.blink(0.1, 0.2)
	elif state == -2:
		pinGreen.on();
	return


def setPins(position,state):
	if position == "HR":
		pins=LED_HR
	elif position == "HL":
		pins=LED_HL
	elif position == "VR":
		pins=LED_VR
	elif position == "VL":
		pins=LED_VL
	elif position == "ZR":
		pins=LED_ZR
	elif position == "ZL":
		pins=LED_ZL
	elif position == "Vo":
		pins=LED_Vo
	
	setPinMCP(pins[0], pins[1], pins[2], state)


def setAlle(state):
	positions = ['HR', 'HL', 'ZR','ZL', 'VR', 'VL', 'Vo']
	for pos in positions:
		setPins(pos,state)
	return
	
def checkTolerance(origValue, adjustValue, toleranceValue):
	# values within the tolerance are evaluated as horizontal
	
	# value adjustment
	value = origValue - adjustValue
	
	if (abs(value) < toleranceValue):
		# value within tolerance 
		value = 0
	
	return value

def checkApproximation(state, value, approximationValue):
	newState = state
	# If the sensor value lies within the approximate values, the LED should indicate the approximation to the horizontal
	if (abs(value) < approximationValue):
		# value approximately horizontal 
		if (state < 0):
			newState = -1
		else:
			newState = 1
	print (state, abs(value), approximationValue, "-->", newState)
	
	return newState


def LED(origX, origY, origZ, adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY):
	#*************************************
	# Activation of the LEDs
	#*************************************
	#
	# Please note:
	# it is assumed that the caravan will be brought into the horizontal position in the following steps:
	# - first the caravan axle is brought into the horizontal position. 
	#   Only the LEDs on the axle are relevant until they are white.
	# - The longitudinal axis is then brought into the horizontal position via the nose wheel. 
	#   Only the LED on the nose wheel is relevant until it is white.
	# - Finally, all pillars are brought to tension. 
	#   The LEDs are all white at first (axis and longitudinal axis horizontal) 
	#   and only indicate whether the pillars are tensioned on one side.  
	#
	# Therefore the LEDS at the corners and at the nose wheel show only the (approximation) position in the longitudinal axis. 
	# The LEDs on the caravan axle indicate the position in the transverse axis.
	#
	#*************************************

	# x = Längsachse
	# y = Querachse
	
	# Adjustment sensor installation deviation
	x = checkTolerance(origX, adjustX, toleranceX)
	y = checkTolerance(origY, adjustY, toleranceY)

	# x  < 0: hinten tiefer
	# y > 0: rechts tiefer
	
	#--------------------------------------------------------------------------
	# step one (or three) - we try to bring the axle into horizontal position
	#--------------------------------------------------------------------------
	if (x  < 0 and y > 0):
		# Wagen ist vorne und rechts tief, hinten und links hoch
		setPins('HR',0)
		setPins('HL',checkApproximation(2, x, approximationX))
		setPins('ZR',checkApproximation(-2, y, approximationY))
		setPins('ZL',checkApproximation(2, y, approximationY))
		setPins('VR',checkApproximation(-2, x, approximationX))
		setPins('VL',0)
		setPins('Vo',checkApproximation(-2, x, approximationX))
	elif (x  < 0 and y < 0):
		# Wagen ist vorne und links tief, hinten und rechts hoch
		setPins('HR',checkApproximation(2, x, approximationX))
		setPins('HL',0)
		setPins('ZR',checkApproximation(2, y, approximationY))
		setPins('ZL',checkApproximation(-2, y, approximationY))
		setPins('VR',0)
		setPins('VL',checkApproximation(-2, x, approximationX))
		setPins('Vo',checkApproximation(-2, x, approximationX))
	elif (x  > 0 and y > 0):
		# Wagen ist hinten und rechts tief, links und vorne hoch
		setPins('HR',checkApproximation(-2, x, approximationX))
		setPins('HL',0) 
		setPins('ZR',checkApproximation(-2, y, approximationY))
		setPins('ZL',checkApproximation(2, y, approximationY))
		setPins('VR',0) 
		setPins('VL',checkApproximation(2, x, approximationX))
		setPins('Vo',checkApproximation(2, x, approximationX))
	elif (x  > 0 and y < 0):
		# Wagen ist hinten und links tief
		setPins('HR',0) 
		setPins('HL',checkApproximation(-2, x, approximationX))
		setPins('ZR',checkApproximation(2, y, approximationY))
		setPins('ZL',checkApproximation(-2, y, approximationY))
		setPins('VR',checkApproximation(2, x, approximationX))
		setPins('VL',0) 
		setPins('Vo',checkApproximation(2, x, approximationX))
	elif (x == 0 and y > 0):
		# Wagen ist vorne und hinten in Waage und rechts tief
		setPins('HR',checkApproximation(-2, x, approximationX))
		setPins('HL',checkApproximation(2, x, approximationX))
		setPins('ZR',checkApproximation(-2, y, approximationY))
		setPins('ZL',checkApproximation(2, y, approximationY))
		setPins('VR',checkApproximation(-2, x, approximationX))
		setPins('VL',checkApproximation(2, x, approximationX))
		setPins('Vo',0)
	elif (x == 0 and y < 0):
		# Wagen ist ist vorne und hinten in Waage und links tief
		setPins('HR',checkApproximation(2, x, approximationX))
		setPins('HL',checkApproximation(-2, x, approximationX))
		setPins('ZR',checkApproximation(2, y, approximationY))
		setPins('ZL',checkApproximation(-2, y, approximationY))
		setPins('VR',checkApproximation(2, x, approximationX))
		setPins('VL',checkApproximation(-2, x, approximationX))
		setPins('Vo',0)
	#---------------------------------------------------------------------------------------
	# step two (or three) - we try to bring the longitudinal axis into horizontal position
	#---------------------------------------------------------------------------------------
	elif (x  < 0 and y == 0):
		# Wagen ist vorne tief und rechts und links in Waage
		setPins('HR',checkApproximation(2, x, approximationX))
		setPins('HL',checkApproximation(2, x, approximationX))
		setPins('ZR',0)
		setPins('ZL',0)
		setPins('VR',checkApproximation(-2, x, approximationX))
		setPins('VL',checkApproximation(-2, x, approximationX))
		setPins('Vo',checkApproximation(-2, x, approximationX))
	elif (x  > 0 and y == 0):
		# Wagen ist hinten tief und rechts und links in Waage
		setPins('HR',checkApproximation(-2, x, approximationX))
		setPins('HL',checkApproximation(-2, x, approximationX))
		setPins('ZR',0)
		setPins('ZL',0)
		setPins('VR',checkApproximation(2, x, approximationX))
		setPins('VL',checkApproximation(2, x, approximationX))
		setPins('Vo',checkApproximation(2, x, approximationX))
	elif (x == 0 and y == 0):
		# Wagen ist vollstaendig in der Waage
		setAlle(0)
	return
	
def main():
	# -------------------------
	# main 
	# -------------------------

	global LED_HR, LED_HL, LED_ZR, LED_ZL, LED_VR, LED_VL, LED_Vo

	# avoid outliers - init values
	lastX = None
	lastY = None
	lastZ = None
	secondLastX = None
	
	# process call parameters
	writeFile = 0
	if len(sys.argv) >= 2:
		writeFile = int(sys.argv[1])
		# delete file to start clean
		deleteFile()

	# read defaults
	# The 3-axis sensor may not be installed exactly horizontally. The values to compensate for this installation difference are read from a file.
	# --> adjustX, adjustY, adjustZ
	# In addition, the LEDs should already indicate "horizontal" as soon as the deviation from the horizontal is within a tolerance.
	# --> approximationX, approximationY
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY) = readAdjustment()
	
	# initialize LEDs
	LED_HR=setupHR()
	LED_HL=setupHL()
	LED_ZR=setupZR()
	LED_ZL=setupZL()
	LED_VR=setupVR()
	LED_VL=setupVL()
	LED_Vo=setupVo()

	# read sensor and adjust LEDs
	while True:
		try:
			i=0
			arrayX = []
			arrayY = []
			arrayZ = []
			
			# read sensor 200 times and put values in a list
			while i < 200:
				(x, y, z) = accelerometer.acceleration
				arrayX.append(x)
				arrayY.append(y)
				arrayZ.append(z)
				i += 1
				# no sleep here, because the accuracy of Python/Raspberry Sleep is not sufficient anyway
				# instead a high number of passes over the loop variable
				
			# normalize values over the calculation of the median (extreme values/outliers are not considered)
			# Adjustment of the values by subtraction of the initial value
			x = statistics.median(arrayX)
	
			# determine the index of the first occurrence of x in the list
			try:
				i = arrayX.index(x)
				# set the counterparts for y and z belonging to the value x
				y = arrayY[i]
				z = arrayZ[i]
			except (ValueError, IndexError):
				# the median did not result in a value that appears in the list (i.e. an actually calculated value).
				# Then set the other median values as well
				y = statistics.median(arrayY)
				z = statistics.median(arrayZ)
			
			if writeFile == 1:
				write2file(x, y, z, checkTolerance(x, adjustX, toleranceX), checkTolerance(y, adjustY, toleranceY), z-adjustZ, lastX, secondLastX)

			ledX = x
			ledY = y
			ledZ = z
			
			# avoid outliers
			# if lastX and secondLastX have already been assigned values once 
			# and the current value is not equal to lastX and is also not equal to secondLastX, 
			# but the two values lastX and secondLastX are equal, it may be an outlier. 
			# Then the current values are not used for LED control, but the previous values.
			#Only the comparison with the X values is necessary, because y and z are dependent on x.
			if (lastX != None and secondLastX != None):
				if (x != lastX and x != secondLastX and lastX == secondLastX):
					ledX = lastX
					ledY = lastY
					ledZ = lastZ
			
			LED(ledX, ledY, ledZ, adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY)
			
			# avoid outliers - swap vars
			secondLastX = lastX
			lastX = x
			lastY = y
			lastZ = z

			sleep(.1)
		except KeyboardInterrupt:
			ledOff()
			break
		except:
			print("unprocessed Error:", sys.exc_info()[0])
			ledOff()
			raise

if __name__ == "__main__":
	main()
