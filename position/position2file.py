#!/usr/bin/python3
# coding=utf-8
# position2file.py
#
# nutzt die aus dem Beschleunigungssensor ADXL345 gelesenen Lagewerte
# um den Wohnwagen über LEDs auszurichten
#
# Aufruf-Parameter
# positionLive.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
#
#-------------------------------------------------------------------------------

import time, datetime
import statistics
import signal
import sys
from time import sleep
import os
import getopt

# imports for sensor ADXL345
import board
import busio
import adafruit_adxl34x

# imports for the calculation of position differences
import math

# import for GPIO Input tactile switches
import RPi.GPIO as GPIO

# import for opening URL to change update Intervall on magic Mirror
import urllib.request

# -----------------------------------------------
# libraries from CaravanPi
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from mcp23017 import mcp23017,pin
from CaravanPiLedClass import Led
from CaravanPiFilesClass import CaravanPiFiles

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
# x longitudinal direction
# y traverse direction
# z vertical direction
adjustX = 0
adjustY = 0
adjustZ = 0
# manual correction with tactile switch to mark the current position in transverse direction as horizontal
globY = 0
globAdjustY = 0
globAdjustSwitchY = 0
# what is still considered horizontal
toleranceX = 0
toleranceY = 0
# When should the approach color be selected?
approximationX = 0
approximationY = 0
# Distance of the 3-axis sensor to the right side (in driving direction) and to the front of the caravan 
# If the 3-axis sensor is mounted behind the axis (in driving direction), 
# the distance to the axis (distAxis) is positive. Otherwise this constant is negative.
# in mm
distRight = 0
distFront = 0
distAxis = 0
# dimensions Caravan (in mm)
lengthOverAll = 0
lengthBody = 0
width = 0

# live and non-live mode
# live mode: 
# - liveMode = 1
# - leds on
# - measurement every 1/10 second
# - switch 'now horizontal' is on
# non-live mode
# - liveMode = 0
# - leds off
# - Measurement every 60 seconds
# - switch 'now horizontal' out of order
liveMode = 0

# files
filePosition = "/home/pi/CaravanPi/values/position"

# LED threads
LED_HR = [None, None, None]
LED_HL = [None, None, None]
LED_ZR = [None, None, None]
LED_ZL = [None, None, None]
LED_VR = [None, None, None]
LED_VL = [None, None, None]
LED_Vo = [None, None, None]

# tactile switch to set the current position in transverse direction as horizontal
pinSwitchNowHorizontal = 6
# tactile switch to activate the 'live' mode
pinSwitchLive = 13
pinLEDLive = 5
 
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
	print ("  -l   start in 'live' mode\n")


# -------------------------
# 3-axis-sensor 
# -------------------------

def write2file(toFile, toScreen, x, y, z, adjustX, adjustY, adjustZ, lastX, secondLastX, diffHL, diffHR, diffVL, diffVR, diffZL, diffZR, diffVo):
	global filePosition
	
	try:
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strX = '{:.6f}'.format(x)
		strY = '{:.6f}'.format(y)
		strZ = '{:.6f}'.format(z)
		strAdjustX = '{:.6f}'.format(adjustX)
		strAdjustY = '{:.6f}'.format(adjustY)
		strDiffHL = '{:.0f}'.format(diffHL)
		strDiffHR = '{:.0f}'.format(diffHR)
		strDiffVL = '{:.0f}'.format(diffVL)
		strDiffVR = '{:.0f}'.format(diffVR)
		strDiffZL = '{:.0f}'.format(diffZL)
		strDiffZR = '{:.0f}'.format(diffZR)
		strDiffVo = '{:.0f}'.format(diffVo)
		if (lastX == None):
			strLastX = "none"
		else:
			strLastX = '{:.6f}'.format(lastX)
		if (secondLastX == None):
			strSecondLastX = "none"
		else:
			strSecondLastX = '{:.6f}'.format(secondLastX)

		valueStr = "\n"+ str_from_time_now + " adjusted_tolerant " + strAdjustX + " " + strAdjustY + " original " + strX + " " + strY + " " + strZ + " last_secondlastX " + strLastX + " " + strSecondLastX + " differences " + strDiffHL + " " + strDiffHR + " " + strDiffZL + " " + strDiffZR + " " + strDiffVL + " " + strDiffVR + " " + strDiffVo

		if toFile == 1:
			file = open(filePosition, 'a')
			file.write(valueStr)
			file.close()
		
		if toScreen == 1:
			print(valueStr)
		
		return 0
	except:
		print("write2file: The file could not be written - unprocessed Error:", sys.exc_info()[0])
		raise
		return -1

# -------------------------
# adjust Threats for LEDs
# -------------------------

def setupVL():
	pinBlue=Led(mymcp1,"gpioa",0)
	pinRed=Led(mymcp1,"gpioa",1)
	pinGreen=Led(mymcp1,"gpioa",2)
	
	return ([pinRed, pinGreen, pinBlue])

def setupVR():
	pinBlue=Led(mymcp1,"gpioa",3)
	pinRed=Led(mymcp1,"gpioa",4)
	pinGreen=Led(mymcp1,"gpioa",5)
	
	return([pinRed, pinGreen, pinBlue])

def setupVo():
	pinBlue=Led(mymcp1,"gpioa",6)
	pinRed=Led(mymcp1,"gpioa",7)
	pinGreen=Led(mymcp1,"gpiob",7)
	
	return([pinRed, pinGreen, pinBlue])

def setupZL():
	pinBlue=Led(mymcp2,"gpioa",0)
	pinRed=Led(mymcp2,"gpioa",1)
	pinGreen=Led(mymcp2,"gpioa",2)
	
	return ([pinRed, pinGreen, pinBlue])

def setupZR():
	pinBlue=Led(mymcp2,"gpioa",3)
	pinRed=Led(mymcp2,"gpioa",4)
	pinGreen=Led(mymcp2,"gpioa",5)
	
	return ([pinRed, pinGreen, pinBlue])


def setupHL():
	pinBlue=Led(mymcp2,"gpioa",6)
	pinRed=Led(mymcp2,"gpioa",7)
	pinGreen=Led(mymcp2,"gpiob",7)
	
	return([pinRed, pinGreen, pinBlue])

def setupHR():
	pinBlue=Led(mymcp2,"gpiob",0)
	pinRed=Led(mymcp2,"gpiob",1)
	pinGreen=Led(mymcp2,"gpiob",2)
	
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
	
	return newState


def LED(origX, origY, origZ, adjustX, adjustY, adjustSwitchY, adjustZ, toleranceX, toleranceY, approximationX, approximationY):
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
	y = checkTolerance(origY, adjustY + adjustSwitchY, toleranceY)

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

def switchInterruptNowHorizontal(channel):  
	# -------------------------
	# switchInterruptNowHorizontal
	# tactile switch was pressed to set the current position in transverse direction as horizontal
	# -------------------------

	global globY, globAdjustY, globAdjustSwitchY
	globAdjustSwitchY = globY - globAdjustY
	print (datetime.datetime.now().strftime("%Y%m%d%H%M%S "), "ACHTUNG: manuelles Waagrecht setzen in Querrichtung !!!")

def switchInterruptLive(channel):  
	# -------------------------
	# switchInterruptLive 
	# tactile switch was pressed to switch between the live mode, 
	# where the leds are working, and the normal mode, 
	# where all values are only written to a file
	#
	# if the mode changes to non-live mode, the "current position is horizontal" was disabled
	# -------------------------

	global globAdjustSwitchY
	global liveMode
	if liveMode == 1:
		print (datetime.datetime.now().strftime("%Y%m%d%H%M%S "), "ACHTUNG: Live Modus beendet !!!")
		liveMode = 0
		GPIO.output(pinLEDLive, False)
		ledOff()
		# change update Intervall on MagicMirror
		urllib.request.urlopen('http://127.0.0.1:8080/MMM-CaravanPiPosition/changeUpdateInterval')
		globAdjustSwitchY = 0
	else:
		print (datetime.datetime.now().strftime("%Y%m%d%H%M%S "), "ACHTUNG: Live Modus startet !!!")
		liveMode = 1
		GPIO.output(pinLEDLive, True)
		# change update Intervall on MagicMirror
		urllib.request.urlopen('http://127.0.0.1:8080/MMM-CaravanPiPosition/changeUpdateInterval')

def signalInterruptUSR1(signum, stack):
	# -------------------------
	# signalInterruptUSR1 
	# SIGUSR1 was send to this process (from setDefaults)
	#
	# read Defaults again
	# -------------------------

	global adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis
	print(signum, ' received: read defaults again')
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis) = CaravanPiFiles.readAdjustment()

def signalInterruptUSR2(signum, stack):
	# -------------------------
	# signalInterruptUSR1 
	# SIGUSR2 was send to this process (from Config Website)
	#
	# read color from file to test LEDs
	# first switchLiveMode if live
	# -------------------------

	print(signum, ' received: test LEDs')
	color = int(CaravanPiFiles.readTestColor())
	print('test LEDs with color ', color)
	if liveMode == 1:
		switchInterruptLive(0)
	setAlle(color)
	

	


	
def main():
	# -------------------------
	# main 
	# -------------------------

	global adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis
	global LED_HR, LED_HL, LED_ZR, LED_ZL, LED_VR, LED_VL, LED_Vo
	global globY, globAdjustY, globAdjustSwitchY
	global lengthOverAll, width, lengthBody
	global pinSwitchNowHorizontal, pinSwitchLive, pinLEDLive
	global liveMode

	# -------------------------
	# tactile switches
	# -------------------------
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(pinSwitchNowHorizontal, GPIO.IN)
	GPIO.add_event_detect(pinSwitchNowHorizontal, GPIO.RISING, callback = switchInterruptNowHorizontal, bouncetime = 400)

	GPIO.setup(pinSwitchLive, GPIO.IN)
	GPIO.add_event_detect(pinSwitchLive, GPIO.RISING, callback = switchInterruptLive, bouncetime = 400)

	GPIO.setup(pinLEDLive, GPIO.OUT)	
	GPIO.output(pinLEDLive, False)
	
	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeFile = 0
	displayScreen = 0
	liveMode=0
	
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
		elif o == "--live" or o == "-l":
			print("start in live mode")
			liveMode = 1
			GPIO.output(pinLEDLive, True)


	for a in args:
		print("further argument: ", a)
	
	
	# -------------------------
	# avoid outliers - init values
	# -------------------------
	lastX = None
	lastY = None
	lastZ = None
	secondLastX = None
	
	# read defaults
	# The 3-axis sensor may not be installed exactly horizontally. The values to compensate for this installation difference are read from a file.
	# --> adjustX, adjustY, adjustZ
	# In addition, the LEDs should already indicate "horizontal" as soon as the deviation from the horizontal is within a tolerance.
	# --> approximationX, approximationY
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis) = CaravanPiFiles.readAdjustment()
	# dimensions of the caravan
	(lengthOverAll, width, lengthBody) = CaravanPiFiles.readDimensions()

	# -------------------------
	# listen to SIGUSR1 for renew the defaults
	# -------------------------
	signal.signal(signal.SIGUSR1, signalInterruptUSR1)
	signal.signal(signal.SIGUSR2, signalInterruptUSR2)
	
	# -------------------------
	# initialize LEDs
	# -------------------------
	LED_HR=setupHR()
	LED_HL=setupHL()
	LED_ZR=setupZR()
	LED_ZL=setupZL()
	LED_VR=setupVR()
	LED_VL=setupVL()
	LED_Vo=setupVo()

	# -------------------------
	# leds off if non-live-mode
	# -------------------------
	if liveMode == 0:
		ledOff()
	
	# read sensor and adjust LEDs
	while True:
		print(datetime.datetime.now().strftime("%Y%m%d%H%M%S "), "live Modus:", liveMode)
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
			
			# save values for tactile switch adjustment
			globY = y
			globAdjustY = adjustY
			
			tolX = checkTolerance(x, adjustX, toleranceX)
			tolY = checkTolerance(y, adjustY, toleranceY)
				
			# calculate the horizontal distance
			# Attention: If the 3-axis sensor is mounted behind the axis (in driving direction), 
			# the distance to the axis is positive. Otherwise this constant is negative.
			distLeft = width - distRight
			distBack = lengthBody - distFront
			
			# ADXL345 data sheet:
			# resolution typical 3.9 mg = 0.0039g
			# arcsin(0.0039) = 0.223454 degree
			#
			# diff = dist * sin(angle)
			#
			# x is the gravity in longitudinal direction
			# arcsin (gravity) = angle
			# sin(angle) = sin(arcsin(gravity)) = gravity
			
			# difference negative = position is "too high"
			diffHL = round((distLeft * tolY / 10) + (distBack * tolX / 10) * -1)
			diffHR = round((distRight * tolY / 10) + (distBack * tolX / 10) * -1)
			diffZL = round((distLeft * tolY / 10) + (distAxis * tolX / 10))
			diffZR = round((distRight * tolY / 10) + (distAxis * tolX / 10))
			diffVL = round((distLeft * tolY / 10) + (distFront * tolX / 10))
			diffVR = round((distRight * tolY / 10) + (distFront * tolX / 10))

			# where is the sensor left or right of the middle?
			if distRight <= (width/2): 
				# sensor is on the right side in driving direction of the caravan
				diffVo = round((((width/2) - distRight) * tolY / 10) + ((distFront + (lengthOverAll - lengthBody)) * tolX / 10))
			else:
				diffVo = round((((width/2) - distLeft) * tolY / 10) + ((distFront + (lengthOverAll - lengthBody)) * tolX / 10))
			
			# one of the Z-values should be zero - normalise the others
			if diffZL >= diffZR:
				diffNormal = diffZL
			else:
				diffNormal = diffZR
				
			diffHL = diffHL - diffNormal
			diffHR = diffHR - diffNormal
			diffZL = diffZL - diffNormal
			diffZR = diffZR - diffNormal
			diffVL = diffVL - diffNormal
			diffVR = diffVR - diffNormal
			diffVo = diffVo - diffNormal
			
			# write values to file and or screen
			write2file(writeFile, displayScreen, x, y, z, tolX, tolY, z-adjustZ, lastX, secondLastX, diffHL, diffHR, diffVL, diffVR, diffZL, diffZR, diffVo)

			if liveMode == 1:
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
				
				LED(ledX, ledY, ledZ, adjustX, adjustY, globAdjustSwitchY, adjustZ, toleranceX, toleranceY, approximationX, approximationY)
				
				# avoid outliers - swap vars
				secondLastX = lastX
				lastX = x
				lastY = y
				lastZ = z

				sleep(.1)
			else:
				j=0
				while j< 120 and liveMode == 0: # 120/.5 = 60 Sekunden
					j=j+1
					sleep (.5)
				# falls inzwsichen LEDtest gestartet wurde, alle LEDs aus
				ledOff()
				
		except KeyboardInterrupt:
			ledOff()
			GPIO.cleanup()
			break
		except:
			print("unprocessed Error:", sys.exc_info()[0])
			ledOff()
			GPIO.cleanup()
			raise
			
	GPIO.cleanup()

if __name__ == "__main__":
	main()
