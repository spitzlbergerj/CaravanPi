#!/usr/bin/python
# coding=utf-8
# gassensorCheck.py
#
# überprüft laufend einen Gassensor des Typs MQ-2
#
#-------------------------------------------------------------------------------

import sys
import argparse
import time
from datetime import datetime 
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
	delay = 30

	# ArgumentParser-Objekt erstellen
	parser = argparse.ArgumentParser(description='Lesen aller Temperatursensoren am 1-Wire-Bus')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe auf dem Bildschirm')
	parser.add_argument('-c', '--check', action='store_true', 
						help='Führt den Funktionstest aus')
	parser.add_argument('-d', '--delay', type=str, default='30',
						help='Wartezeit zwischen zwei Messungen in Sekunden')

	# Argumente parsen
	args = parser.parse_args()
	delay = int(args.delay)
	delayAlarm = 2

	# Libraries anbinden
	cplib = CaravanPiFiles()
	cpfunc = CaravanPiFunctions()

	buzzer_pin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/BuzzerGPIOPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/BuzzerGPIOPin") is not None else -1
	if buzzer_pin == -1:
		print("Buzzer GPIO Pin nicht richtig konfiguriert - Programmende")
		return False

	# gibt es einen Gassensor?
	gassensorInstalled = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorInstalled"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorInstalled") is not None else False
	gassensorDigitalIn = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorDigitalIn")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorDigitalIn") is not None else -1
	gassensorAnalogIn = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAnalogIn")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAnalogIn") is not None else -1
	gassensorAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmActive"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmActive") is not None else False
	gassensorAlarmResume = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmResume"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmResume") is not None else False
						  
	print(f"Digital: {gassensorDigitalIn} , Analog: {gassensorAnalogIn}, Alarm aktiv: {gassensorAlarmActive}, Delay: {delay} Sekunden")

	if not gassensorInstalled:
		print(f"kein Gassensor konfiguriert - Skript beenden")
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
	
	# digital Pin aktivieren
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gassensorDigitalIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	
	# Create single-ended input on channel 0
	if gassensorAnalogIn == 0: 
		channel = AnalogIn(ads, ADS.P0)
	elif gassensorAnalogIn == 1: 
		channel = AnalogIn(ads, ADS.P1)
	elif gassensorAnalogIn == 2: 
		channel = AnalogIn(ads, ADS.P2)
	elif gassensorAnalogIn == 3: 
		channel = AnalogIn(ads, ADS.P3)
	else:
		print("AnalogIn Pin ist falsch, SOLL: 0 - 3, IST: {gassensorAnalogIn}")
		return False
	
	errorcount = 0
	gasDetected = False
	zaehler = 0

	try: # Main program loop
		while True:  
			zaehler += 1  
			try:
				# Einlesen, ob Alarm ausgegeben werden soll
				gassensorAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmActive"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmActive") is not None else False
				if not gassensorAlarmActive:
					print("Alarm über Config ausgeschaltet")

				print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: ", "Analog: {:>5}, {:>5.3f}, ".format(channel.value, channel.voltage), "Digital: {}".format(GPIO.input(gassensorDigitalIn)))

				if GPIO.input(gassensorDigitalIn) == 0:
					# Gas detektiert
					gasDetected = True
					# Alarm ausgeben, wenn nicht abgeschaltet
					if gassensorAlarmActive:
						cpfunc.play_alarm_single(GPIO, buzzer_pin, 1)
				else:
					# kein Gas detektiert
					gasDetected = False

					if not gassensorAlarmActive and gassensorAlarmResume:
						print("Alarm wieder einschalten")
						cplib.writeCaravanPiConfigItem("caravanpiDefaults/gassensorAlarmActive", 1)
						gassensorAlarmActive = True
					
				if not gasDetected or (gasDetected and zaehler >= (delay/delayAlarm)):
					cplib.handle_sensor_values(
						args.screen,    				    # Anzeige am Bildschirm?
						"gassensor",      					# sensor_name = Datenbankname 
						"mq-2",     						# sensor_id = Filename und Spalte in der Datenbank
						["parts_per_million", "alarm"], 	# Liste Spaltennamen
						( channel.value, gasDetected) 		# Tupel Sensorwerte
					)
					zaehler = 0

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

			time.sleep(delayAlarm if gasDetected else delay)


	except KeyboardInterrupt:
		# Alarm ausgeben, dass nicht zufällig Dauerton verbleibt beim Abbrechen
		cpfunc.play_alarm_single(GPIO, buzzer_pin, 1)
		print('Script end!')
			

if __name__=="__main__":
	result = main()
	sys.exit(result)