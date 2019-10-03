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

import signal
import sys
from time import sleep

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from mcp23017 import mcp23017,pin
from ledClass import Led

# -----------------------------------------------
# globale Variable
# -----------------------------------------------
# initiate GPIO port expander
mymcp1=mcp23017(1,0x20)
mymcp2=mcp23017(1,0x21)

# -------------------------
# functions 
# -------------------------

def ledOff():
	# LEDs ausschalten
	setAlle("off")
	return

# -------------------------
# LED management
# -------------------------

def getHR():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp1,"gpiob",3)
	pinGreen=pin(mymcp1,"gpiob",4)
	pinBlue=pin(mymcp1,"gpiob",5)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def getHL():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp1,"gpioa",3)
	pinGreen=pin(mymcp1,"gpioa",4)
	pinBlue=pin(mymcp1,"gpioa",5)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def getVR():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp1,"gpiob",0)
	pinGreen=pin(mymcp1,"gpiob",1)
	pinBlue=pin(mymcp1,"gpiob",2)
	
	return("mcp", pinRed, pinGreen, pinBlue)


def getVL():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp1,"gpioa",0)
	pinGreen=pin(mymcp1,"gpioa",1)
	pinBlue=pin(mymcp1,"gpioa",2)
	
	return ("mcp", pinRed, pinGreen, pinBlue)


def getZR():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp2,"gpioa",5)
	pinGreen=pin(mymcp2,"gpioa",4)
	pinBlue=pin(mymcp2,"gpioa",3)
	
	return ("mcp", pinRed, pinGreen, pinBlue)


def getZL():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp2,"gpioa",2)
	pinGreen=pin(mymcp2,"gpioa",1)
	pinBlue=pin(mymcp2,"gpioa",0)
	
	return ("mcp", pinRed, pinGreen, pinBlue)


def getVo():
	global mymcp1
	global mymcp2
	
	pinRed=pin(mymcp1,"gpioa",6)
	pinGreen=pin(mymcp1,"gpioa",7)
	pinBlue=pin(mymcp1,"gpiob",7)
	
	return("mcp", pinRed, pinGreen, pinBlue)

def setPinMCP(pinRed, pinGreen, pinBlue, color):
	pinRed.disable();
	pinBlue.disable();
	pinGreen.disable();

	if color == "off":
		return
	elif color == "red":
		pinRed.enable();
		pinBlue.disable();
		pinGreen.disable()
	elif color == "blue":
		pinRed.disable();
		pinBlue.enable();
		pinGreen.disable()
	elif color == "green":
		pinRed.disable()
		pinBlue.disable();
		pinGreen.enable();
	elif color == "all":
		pinRed.enable();
		pinBlue.enable()
		pinGreen.enable();
	elif color == "redblue":
		pinRed.enable();
		pinBlue.enable()
		pinGreen.disable();
	elif color == "redgreen":
		pinRed.enable();
		pinBlue.disable()
		pinGreen.enable();
	elif color == "bluegreen":
		pinRed.disable();
		pinBlue.enable()
		pinGreen.enable();
	return

def setPins(position,color):
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
	
	setPinMCP(pins[1], pins[2], pins[3], color)


def setAlle(color):
	positions = ['HR', 'HL', 'ZR','ZL', 'VR', 'VL', 'Vo']
	for pos in positions:
		setPins(pos,color)
	return
	

	
def main():
	# -------------------------
	# main 
	# -------------------------
	
	global mymcp1
	global mymcp2
	
	while True:
		try:
			VoRED = Led(mymcp1,"gpioa",6)
			VoGREEN = Led(mymcp1,"gpioa",7)
			VoBLUE = Led(mymcp1,"gpiob",7)
			
			VoRED.on()
			sleep(1)
			
			VoRED.off()
			sleep(1)
			
			VoRED.blink(0.1, 0.2)
			sleep(5)
			
			VoRED.off()
			sleep(1)
			
			colors = ["off", "red", "blue", "green", "off", "all", "off", "redblue", "redgreen","bluegreen", "all", "off"]
			for i in colors:
				print (i)
				setAlle(i)
				sleep(1)
			sleep(2)
		except KeyboardInterrupt:
			ledOff()
			break
		except:
			print("unprocessed Error:", sys.exc_info()[0])
			ledOff()
			raise

if __name__ == "__main__":
	main()
