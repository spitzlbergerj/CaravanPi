#!/usr/bin/python
from mcp23017 import mcp23017,pin
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT, initial=0)
GPIO.setup(16, GPIO.OUT, initial=0)
GPIO.setup(18, GPIO.OUT, initial=0)
GPIO.setup(20, GPIO.OUT, initial=0)
GPIO.setup(23, GPIO.OUT, initial=0)
GPIO.setup(24, GPIO.OUT, initial=0)

mymcp=mcp23017()


def setPinMCP(pinRed, pinGreen, pinBlue, state):
	pinRed.disable();
	pinBlue.disable();
	pinGreen.disable();

	if state == 99:
		return
	elif state < 0:
		pinGreen.enable()
	elif state == 0:
		pinRed.enable()
	elif state > 0:
		pinBlue.enable()
	return

def setPinGPIO(nrRed, nrGreen, nrBlue, state):
	GPIO.output(nrRed, 0)
	GPIO.output(nrGreen, 0)
	GPIO.output(nrBlue, 0)

	if state == 99:
		return
	elif state < 0:
		GPIO.output(nrGreen, 1)
	elif state == 0:
		GPIO.output(nrRed, 1)
	elif state > 0:
		GPIO.output(nrBlue, 1)
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


print "reset"
setAlle(-1)
sleep (.1)
setAlle(0)
sleep (.1)
setAlle(1)
sleep (.1)
setAlle(99)
sleep(1)

zaehler = 0
while True:
	
	#*************************************
	# einlesen der Winkelwerte
	#
	# x = Winkel in Laengsrichtung 
	#     negativer Winkel = vorne tiefer
	#
	# y = Winkel in Querrichtung
	#     negativer Winkel = rechts tiefer
	#
	# z = irrelevant
	#
	#*************************************
	
	if zaehler == 0:
		x = -1
		y = -.8
		z = 0
	else:
		x = x + zaehler / 10
		y = y + zaehler / 10
	
	zaehler = zaehler + 1
	
	#*************************************
	# Einstellen der LEDs
	#*************************************
	
	if (x < 0 and y < 0):
		# Wagen ist vorne und rechts tiefer
		positions = ['HR', 'VL']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZL', 'HL']
		for pos in positions:
			setPins(pos,1)
		positions = ['ZR','VR']
		for pos in positions:
			setPins(pos,-1)
		setPins('Vo',-1)
	elif (x < 0 and y > 0):
		# Wagen ist vorne und links tief
		positions = ['VR', 'HL']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZR', 'HR']
		for pos in positions:
			setPins(pos,1)
		positions = ['ZL','VL']
		for pos in positions:
			setPins(pos,-1)
		setPins('Vo',-1)
	elif (x < 0 and y == 0):
		# Wagen ist vorne tief und rechts und links in Waage
		positions = ['VR', 'VL']
		for pos in positions:
			setPins(pos,-1) 
		positions = ['ZR', 'ZL']
		for pos in positions:
			setPins(pos,0)
		positions = ['HR','HL']
		for pos in positions:
			setPins(pos,1)
		setPins('Vo',-1)
	elif (x > 0 and y < 0):
		# Wagen ist hinten und rechts tief
		positions = ['VR', 'HL']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZR', 'HR']
		for pos in positions:
			setPins(pos,-1)
		positions = ['ZL','VL']
		for pos in positions:
			setPins(pos,1)
		setPins('Vo',1)
	elif (x > 0 and y > 0):
		# Wagen ist hinten und links tief
		positions = ['VL', 'HR']
		for pos in positions:
			setPins(pos,0) 
		positions = ['ZR', 'VR']
		for pos in positions:
			setPins(pos,1)
		positions = ['ZL','HL']
		for pos in positions:
			setPins(pos,1)
		setPins('Vo',-1)
	elif (x > 0 and y == 0):
		# Wagen ist hinten tief und rechts und links in Waage
		positions = ['VR', 'VL']
		for pos in positions:
			setPins(pos,1) 
		positions = ['ZR', 'ZL']
		for pos in positions:
			setPins(pos,0)
		positions = ['HR','HL']
		for pos in positions:
			setPins(pos,-1)
		setPins('Vo',1)
	elif (x == 0 and y < 0):
		# Wagen ist vorne und hinten in Waage und rechts tief
		positions = ['VR', 'ZR', 'HR']
		for pos in positions:
			setPins(pos,-1) 
		positions = ['VL', 'ZL', 'HL']
		for pos in positions:
			setPins(pos,1)
		setPins('Vo',0)
	elif (x == 0 and y > 0):
		# Wagen ist ist vorne und hinten in Waage und links tief
		positions = ['VR', 'ZR', 'HR']
		for pos in positions:
			setPins(pos,1) 
		positions = ['VL', 'ZL', 'HL']
		for pos in positions:
			setPins(pos,-1)
		setPins('Vo',0)
	elif (x == 0 and y == 0):
		# Wagen ist vollstaendig in der Waage
		setAlle(0)

	sleep(1)