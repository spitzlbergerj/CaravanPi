#!/usr/bin/python
# coding=utf-8
# v12Check.py
#
# überprüft das Vorhandensein von 12V
# Dabei mehrere 12V Eingänge überwacht werden, bei geeignetem Parameter
#
# nutzt dazu einen Spannungsteiler, einen LevelConverter und einen ADC1115
# Wenn 12V nicht da ist oder ein zu niedriges Spannungslevel vorhanden ist, wird ein Alarmton ausgegeben
#
# ist ein ausreichendes Level wieder vorhanden, wird in den Defaults der Alarm wieder eingeschaltet, so dass ein 
# vorübergehend über die Config ausgeschalteter Alarm wieder aktiviert wird
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
	parser = argparse.ArgumentParser(description='Überwachung der 12V Versorgung')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe auf dem Bildschirm')
	parser.add_argument('-c', '--check', action='store_true', 
						help='Führt den Funktionstest aus')
	parser.add_argument('-d', '--delay', type=str, default='30',
						help='Wartezeit zwischen zwei Messungen in Sekunden, default=30')
	parser.add_argument('-b', '--battery', type=str, choices=['car', 'bord'], default='bord',
						help='12V Anschluss wählen zwischen "bord" und "car", default = "bord"')

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

	# ist die 12V Überwachung konfiguriert?
	if args.battery == "bord":
		v12CheckInstalled = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckInstalled"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckInstalled") is not None else False
		v12CheckADCPin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckADCPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckADCPin") is not None else -1
		v12CheckAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckAlarmActive"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckAlarmActive") is not None else False
		v12xmlItemAlarm = "v12BatteryCheckAlarmActive"
	elif args.battery == "car":
		v12CheckInstalled = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v12CarCheckInstalled"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v12CarCheckInstalled") is not None else False
		v12CheckADCPin = int(cplib.readCaravanPiConfigItem("caravanpiDefaults/v12CarCheckADCPin")) if cplib.readCaravanPiConfigItem("caravanpiDefaults/v12CarCheckADCPin") is not None else -1
		v12CheckAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem("caravanpiDefaults/v12CarCheckAlarmActive"), "bool") if cplib.readCaravanPiConfigItem("caravanpiDefaults/v12CarCheckAlarmActive") is not None else False
		v12xmlItemAlarm = "v12CarCheckAlarmActive"
	else:
		print(f"falscher Battery Parameter - Skript beenden")
		return False

	v12Level1 = float(cplib.readCaravanPiConfigItem("voltageDefaults/level1")) if cplib.readCaravanPiConfigItem("voltageDefaults/level1") is not None else -1
	v12Level2 = float(cplib.readCaravanPiConfigItem("voltageDefaults/level2")) if cplib.readCaravanPiConfigItem("voltageDefaults/level2") is not None else -1
	v12Level3 = float(cplib.readCaravanPiConfigItem("voltageDefaults/level3")) if cplib.readCaravanPiConfigItem("voltageDefaults/level3") is not None else -1

	if v12Level1 == -1 or v12Level2 == -1 or v12Level3 == -1:
		print(f"Batterie Default Level nicht korrekt definiert ({v12Level1}, {v12Level2}, {v12Level3}) - Skript beenden")
		return False

	print(f"ADC Pin: {v12CheckADCPin}, Alarm aktiv: {v12CheckAlarmActive}, Delay: {delay} Sekunden, Levels: {v12Level1}, {v12Level2}, {v12Level3}")

	if not v12CheckInstalled:
		print(f"keine 12V Überwachung für {args.battery} konfiguriert - Skript beenden")
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
	if v12CheckADCPin == 0: 
		channel = AnalogIn(ads, ADS.P0)
	elif v12CheckADCPin == 1: 
		channel = AnalogIn(ads, ADS.P1)
	elif v12CheckADCPin == 2: 
		channel = AnalogIn(ads, ADS.P2)
	elif v12CheckADCPin == 3: 
		channel = AnalogIn(ads, ADS.P3)
	else:
		print("AnalogIn Pin ist falsch, SOLL: 0 - 3, IST: {v12CheckADCPin}")
		return False
	
	errorcount = 0
	v12DropDetected = False

	# Umrechnung der Batterie Levels nach dem Logiklevel Wandler 
	# ????

	# Test mit 5 Volt
	v12Level1 = 1.2
	v12Level2 = 1.6
	v12Level3 = 1.7

	try: # Main program loop
		while True:  
			try:
				# Einlesen, ob Alarm ausgegeben werden soll
				v12CheckAlarmActive = cplib.typwandlung(cplib.readCaravanPiConfigItem(f"caravanpiDefaults/{v12xmlItemAlarm}"), "bool") if cplib.readCaravanPiConfigItem(f"caravanpiDefaults/{v12xmlItemAlarm}") is not None else False
				if not v12CheckAlarmActive:
					print("Alarm über Config ausgeschaltet")

				# Eine voll geladene Batterie gibt etwa 13.3 Volt aus, unter 12 Volt gilt eine Batterie als leer
				print(f"{datetime.now().strftime('%Y%m%d %H:%M:%S')}: ", "Analog: {:>5}, {:>5.3f}, ".format(channel.value, channel.voltage))

				if channel.voltage <= v12Level1:
					print(f"Batterie leer bei {channel.voltage} Volt")
					# Batterie leer
					v12DropDetected = True
					# Alarm ausgeben, wenn nicht abgeschaltet
					if v12CheckAlarmActive:
						cpfunc.play_alarm_single(GPIO, buzzer_pin, 3)
				elif channel.voltage <= v12Level2:
					print(f"Batterie ok bei {channel.voltage} Volt")
					# Batterie noch OK
					v12DropDetected = False
				elif channel.voltage > v12Level2 and channel.voltage <= v12Level3:
					print(f"Batterie voll geladen bei {channel.voltage} Volt")
					# Batterie voll
					v12DropDetected = False
				else:
					print(f"Batterie bei {channel.voltage} Volt - seltsamer Zustand")
					# Batterie überladen oder defekt ??
					v12DropDetected = True
					# Alarm ausgeben, wenn nicht abgeschaltet
					if v12CheckAlarmActive:
						cpfunc.play_alarm_single(GPIO, buzzer_pin, 3)
					
				if channel.voltage > v12Level1 and channel.voltage <= v12Level3:
					if not v12CheckAlarmActive:
						# Alarm wieder einschalten
						print("Alarm in Config einschalten")
						cplib.writeCaravanPiConfigItem(f"caravanpiDefaults/{v12xmlItemAlarm}", 1)
						v12CheckAlarmActive = True
					
				time.sleep(delayAlarm if v12DropDetected else delay)

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
		# Alarm ausgeben, dass nicht zufällig Dauerton verbleibt beim Abbrechen
		cpfunc.play_alarm_single(GPIO, buzzer_pin, 1)
		print('Script end!')
			

if __name__=="__main__":
	result = main()
	sys.exit(result)