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
	delay = float(args.delay)
	delayAlarm = 1.5

	# Libraries anbinden
	cplib = CaravanPiFiles()
	cpfunc = CaravanPiFunctions()

	buzzer_pin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/BuzzerGPIOPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/BuzzerGPIOPin") is not None else -1
	if buzzer_pin == -1:
		print("Buzzer GPIO Pin nicht richtig konfiguriert - Programmende")
		return False

	# ist die 230V Überwachung konfiguriert?
	v230CheckInstalled = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckInstalled"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckInstalled") is not None else False
	v230CheckADCPin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckADCPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckADCPin") is not None else -1
	v230CheckAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive") is not None else False
	v230CheckAlarmResume = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmResume"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmResume") is not None else False
						  
	print(f"ADC Pin: {v230CheckADCPin}, Alarm aktiv: {v230CheckAlarmActive}, Delay: {delay} Sekunden")

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
	schwelle = 2.0
	v230DropDetected = False


	try: # Main program loop
		while True:  
			try:
				# Einlesen, ob Alarm ausgegeben werden soll
				v230CheckAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive") is not None else False
				if not v230CheckAlarmActive:
					print("Alarm über Config ausgeschaltet")

				# Die Check-Platine gibt 3,x Volt aus, falls keine 230 V anliegen
				# Falls 230V anliegen, ist der Wert deutlich unter 2.5 V
				print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: ", "Analog: {:>5}, {:>5.3f}, ".format(channel.value, channel.voltage))

				if channel.voltage > schwelle:
					# 230 V liegen nicht an
					v230DropDetected = True
					# Alarm ausgeben, wenn nicht abgeschaltet
					if v230CheckAlarmActive:
						cpfunc.play_alarm_single(GPIO, buzzer_pin, 2)
				else:
					# 230 Volt liegen an
					v230DropDetected = False
					
					if not v230CheckAlarmActive and v230CheckAlarmResume:
						# Alarm wieder einschalten
						print("Alarm in Config einschalten")
						cplib.writeCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive", 1)
						v230CheckAlarmActive = True
					
				cplib.handle_sensor_values(
					args.screen,    		    # Anzeige am Bildschirm?
					"spannung",      			# sensor_name = Datenbankname 
					"230v",     	# sensor_id = Filename und Spalte in der Datenbank
					["spannung"], 				# Liste Spaltennamen
					(230.0 if not v230DropDetected else 0.0 , ) # Tupel Sensorwerte
				)


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

			time.sleep(delayAlarm if v230DropDetected else delay)

	except KeyboardInterrupt:
		# Alarm ausgeben, dass nicht zufällig Dauerton verbleibt beim Abbrechen
		cpfunc.play_alarm_single(GPIO, buzzer_pin, 1)
		print('Script end!')
			

if __name__=="__main__":
	result = main()
	sys.exit(result)