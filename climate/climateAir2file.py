#!/usr/bin/python
# coding=utf-8
# climateAir2file.py
#
# liest Klima- und Luftqualitätswerte aus einem BME680 Sensor
#
# Aufruf-Parameter
# positionLive.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
#
#-------------------------------------------------------------------------------

import smbus
import time
import datetime
import sys
import getopt
import bme680

# -----------------------------------------------
# libraries from CaravanPi
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

# -----------------------------------------------
# global variables
# -----------------------------------------------
DEVICE = 0x76    # for compatibility reasons

# -------------------------
# call options 
# -------------------------
shortOptions = 'hfsd:'
longOptions = ['help', 'file', 'screen', 'device=']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h -f -s -l")
	print ("  -h        show this guide")
	print ("  -f        write values to file ")
	print ("  -s        display values on this screen\n")
	print ("  -d <nr>   device address in hexadecimal notation (default 76)\n")

def write2file(chip_id, device, temperature, pressure, humidity, gasResistanca):
		try:
				sensorId = "BME680-" + str(chip_id) + "-" + str(device)
				dateiName = "/home/pi/CaravanPi/values/" + sensorId
				file = open(dateiName, 'a')
				str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
				strTemperature = '{:.1f}'.format(temperature)
				strPressure = '{:.1f}'.format(pressure)
				strHumidity = '{:.1f}'.format(humidity)
				strGasResistance = '{:.1f}'.format(humidity)

				file.write("\n" + sensorId + " " + str_from_time_now + " " +
									 strTemperature + " " + strPressure + " " + strHumidity + " " + strGasResistance)
				file.close()
				return 0
		except:
				# Schreibfehler
				print("Die Datei konnte nicht geschrieben werden.")
				return -1


def main():
	# -------------------------
	# main 
	# -------------------------

	global DEVICE, DEVICE1, DEVICE2

	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeFile = 0
	displayScreen = 0

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
			print("output also to file")
			writeFile = 1
		elif o == "--screen" or o == "-s":
			print("output also to this screen")
			displayScreen = 1
		elif o == "--device" or o == "-d":
			DEVICE = int(a,16)
			print("Device number ", '{:.0f}'.format(DEVICE))


	for a in args:
		print("further argument: ", a)
	
	# -------------------------
	# initialize sensor
	# -------------------------

	sensor = bme680.BME680(DEVICE)

	# setzen der Oversample Werte
	# je höher der Wert
	# desto größer ist die Reduktion von Störungen
	# desto kleiner ist die Präzision
	sensor.set_humidity_oversample(bme680.OS_2X)
	sensor.set_pressure_oversample(bme680.OS_4X)
	sensor.set_temperature_oversample(bme680.OS_8X)

	# setzen eines Filters, der schnelle Änderugnen (öffne iner Tür) herausfiltert
	sensor.set_filter(bme680.FILTER_SIZE_3)

	# Gas Sensor benötigt eine Heizung und mehr Zeit für das Auslesen
	sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
	sensor.set_gas_heater_temperature(320)
	sensor.set_gas_heater_duration(150)
	sensor.select_gas_heater_profile(0)

	chip_id = 9999

	# -------------------------
	# read sensor
	# -------------------------

	# mehrmals vorab lesen
	print("Probelesen ...")
	i = 0
	while i < 3:
		gelesen = sensor.get_sensor_data()
		print("... ", i, gelesen)
		i += 1
		time.sleep(2)

	if sensor.get_sensor_data():
		print("Daten erfolgreich gelesen ...")
		if writeFile == 1:
			print("in Datei schreiben ...")
			write2file(chip_id, DEVICE, sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sensor.data.gas_resistance)

		if displayScreen == 1:
			print("Chip ID         :", chip_id)
			print("Temperature     : {0:.2f} °C".format(sensor.data.temperature))
			print("Pressure        : {0:.2f} hPa".format(sensor.data.pressure))
			print("Humidity        : {0:.2f} %RH".format(sensor.data.humidity))
			print("Luft Widerstand : {0} Ohms".format(sensor.data.gas_resistance))
	else:
			print("Fehler beim Lesen des BME680 Sensors")

if __name__ == "__main__":
		main()
