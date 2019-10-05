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

# LED threads
LED_HR = [None, None, None]
LED_HL = [None, None, None]
LED_ZR = [None, None, None]
LED_ZL = [None, None, None]
LED_VR = [None, None, None]
LED_VL = [None, None, None]
LED_Vo = [None, None, None]

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
	setAlle("off")
	return

def setPinMCP(pinRed, pinGreen, pinBlue, state):
	# state:
	#	2	zu hoch				blau
	#	1	knapp zu hoch		blau blinkend
	#	0	waagrecht			weiß
	#	-1	knapp zu niedrig	grün blinkend
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
	

	
def main():
	# -------------------------
	# main 
	# -------------------------
	
	global LED_HR, LED_HL, LED_ZR, LED_ZL, LED_VR, LED_VL, LED_Vo
	
	# initialize LEDs
	LED_HR=setupHR()
	LED_HL=setupHL()
	LED_ZR=setupZR()
	LED_ZL=setupZL()
	LED_VR=setupVR()
	LED_VL=setupVL()
	LED_Vo=setupVo()
	
	while True:
		try:
			states = [99, 0, 2, -2, 1, 0, -1, 0]
			for i in states:
				print (i)
				setAlle(i)
				sleep(2)
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
