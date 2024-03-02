#!/usr/bin/python
# coding=utf-8
# v230Check.py
#
# überprüft das Vorhandensein von 230V
#
# nutzt dazu eine Spezialplatine und einen ADC1115
# Wenn 230v nicht da ist, wird ein Alarmton ausgegeben bis der Landstrom zurückkehrt
#
# ist 230v vorhanden, wird in den Defaults der Alarm wieder eingeschaltet, so dass ein 
# vorübergehend über die Config ausgeschalteter Alarm wieder aktiviert wird, sobald Landstrom wieder da ist
#
#-------------------------------------------------------------------------------

import sys
import argparse
import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles
from CaravanPiFunctionsClass import CaravanPiFunctions


def main():
	# ArgumentParser-Objekt erstellen
	parser = argparse.ArgumentParser(description='Lesen aller Temperatursensoren am 1-Wire-Bus')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe auf dem Bildschirm')
	parser.add_argument('-c', '--check', action='store_true', 
						help='Führt den Funktionstest aus')
	parser.add_argument('-d', '--delay', type=str, default='60',
						help='Wartezeit zwischen zwei Messungen in Sekunden')

	# Argumente parsen
	args = parser.parse_args()
	delay = float(args.delay)

	# Libraries anbinden
	cplib = CaravanPiFiles()
	cpfunc = CaravanPiFunctions()

	buzzer_pin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/BuzzerGPIOPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/BuzzerGPIOPin") is not None else -1
	if buzzer_pin == -1:
		print("Buzzer GPIO Pin nicht richtig konfiguriert - Programmende")
		return False

	# ist die 230V Überwachung konfiguriert?
	v230CheckInstalled = bool(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckInstalled")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckInstalled") is not None else False
	v230CheckADCPin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckADCPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckADCPin") is not None else -1
	v230CheckAlarmActive = bool(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive") is not None else False
						  
	print(f"ADC Pin: {v230CheckADCPin}, Alarm aktiv: {v230CheckAlarmActive}")

	if not v230CheckInstalled:
		print(f"keine 230V Überwachung konfiguriert - Skript beenden")
		return False

	# Verbindung zum AD Wandler herstellen
	connectOK = False
	try:
		# Create the I2C bus
		i2c = busio.I2C(board.SCL, board.SDA)

		# Create the ADC object using the I2C bus
		ads = ADS.ADS1015(i2c)

		connectOK = True
	except:
		print(f"AD Wandler nicht gefunden - Skript beenden")
		connectOK = False

	# nur Check?
	if args.check:
		# nur Check, daher Abschluss hier
		if connectOK:
			print("erfolgreich")
			return True
		else:
			print("Connect nicht möglich")
			return False

	# Connect fehlgeschlagen, dann beenden
	if not connectOK:
		return False

	# Schweelwerte holen
	v1 = float(cplib.readCaravanPiConfigItem("voltageDefaults/level1")) if cplib.readCaravanPiConfigItem("voltageDefaults/level1") is not None else 0
	v2 = float(cplib.readCaravanPiConfigItem("voltageDefaults/level2")) if cplib.readCaravanPiConfigItem("voltageDefaults/level2") is not None else 0
	v3 = float(cplib.readCaravanPiConfigItem("voltageDefaults/level3")) if cplib.readCaravanPiConfigItem("voltageDefaults/level3") is not None else 0
						  
	print(f"Level 1: {v1}, Level 2: {v2}, Level 3: {v3}")

	# GPIO für Buzzer initialisieren
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	
	# Create single-ended input on channel 0
	if v230CheckADCPin == 0: 
		channel = AnalogIn(ads, ADS.P0)
	elif v230CheckADCPin == 1: 
		channel = AnalogIn(ads, ADS.P1)
	elif v230CheckADCPin == 2: 
		channel = AnalogIn(ads, ADS.P2)
	elif v230CheckADCPin == 3: 
		channel = AnalogIn(ads, ADS.P3)
	else:
		print("AnalogIn Pin ist falsch, SOLL: 0 - 3, IST: {v230CheckADCPin}")
		return False
	
	errorcount = 0

	try: # Main program loop
		while True:  
			try:
				print("Analog: {:>5}\t{:>5.3f}".format(channel.value, channel.voltage))

				print("---")

				v3 = 3

				if channel.voltage <= v3:
					# Ladung nicht mehr ausreichend
					if v230CheckAlarmActive:
						cpfunc.play_alarm_single(GPIO, buzzer_pin, 2)
				else:
					# Ladung ausreichend
					# Alarm wieder einschalten
					cplib.writeCaravanPiConfigItem("v230CheckAlarmActive", 1)
					v230CheckAlarmActive = True
					
				time.sleep(delay)

			except Exception as e:
				print(f"Fehler {e} ist aufgetreten")
				# alle anderen Fehler
				errorcount = errorcount + 1
				if errorcount > 30:
					print("zu viele Fehler")
					return False
				continue
				
			else:
				# kein Fehler aufgetreten
				errorcount = 0

	except KeyboardInterrupt:
		# Savenging work after the end of the program
		print('Script end!')
			

if __name__=="__main__":
	result = main()
	sys.exit(result)