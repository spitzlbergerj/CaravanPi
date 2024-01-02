#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bme280.py
#  Read data from a digital pressure sensor.
#
#  Official datasheet available from :
#  https://www.bosch-sensortec.com/bst/products/all_products/bme280
#
# Author : Matt Hawkins
# Date   : 21/01/2018
#
# https://www.raspberrypi-spy.co.uk/
#
#  Additions to read two BME280 Sensors
#  Addition of skript arguments - climate2file <address> <toFile>
#    address = 76 or 77
#    toFile = 1 (write to file) or 0 (write to console)
#  Additons to write values to file
#
# Author : Josef Spitzlberger
# Date   : 21/08/2019
#
# Date: 02.01.2024
# Verbesserung bei der Parameterverarbeitung
# Anpassung an neue zentrale Funktionen in der Class CaravanPiFiles
# Formatierung der Funktion
#--------------------------------------
import smbus
import time
import argparse
import sys
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles


DEVICE1 = 0x76      # Default device I2C address
DEVICE2 = 0x77      # Second device I2C address
DEVICE = DEVICE1    # for compatibility reasons


bus = smbus.SMBus(1)	# Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
						# Rev 1 Pi uses bus 0

def getShort(data, index):
	# return two bytes from data as a signed 16-bit value
	return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
	# return two bytes from data as an unsigned 16-bit value
	return (data[index+1] << 8) + data[index]

def getChar(data,index):
	# return one byte from data as a signed char
	result = data[index]
	if result > 127:
		result -= 256
	return result

def getUChar(data,index):
	# return one byte from data as an unsigned char
	result =  data[index] & 0xFF
	return result

def readBME280ID(addr=DEVICE):
	# Chip ID Register Address
	REG_ID     = 0xD0
	try:
		(chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
		return (chip_id, chip_version)
	except Exception as e:
		print(f"ERROR - Fehler beim Lesen von BME280 ID an Adresse {addr}: {e}")
		return (None, None)

def readBME280All(addr=DEVICE):
	# Register Addresses
	REG_DATA = 0xF7
	REG_CONTROL = 0xF4
	REG_CONFIG  = 0xF5

	REG_CONTROL_HUM = 0xF2
	REG_HUM_MSB = 0xFD
	REG_HUM_LSB = 0xFE

	# Oversample setting - page 27
	OVERSAMPLE_TEMP = 2
	OVERSAMPLE_PRES = 2
	MODE = 1

	try:
		# Oversample setting for humidity register - page 26
		OVERSAMPLE_HUM = 2
		bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

		control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
		bus.write_byte_data(addr, REG_CONTROL, control)

		# Read blocks of calibration data from EEPROM
		# See Page 22 data sheet
		cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
		cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
		cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

		# Convert byte data to word values
		dig_T1 = getUShort(cal1, 0)
		dig_T2 = getShort(cal1, 2)
		dig_T3 = getShort(cal1, 4)

		dig_P1 = getUShort(cal1, 6)
		dig_P2 = getShort(cal1, 8)
		dig_P3 = getShort(cal1, 10)
		dig_P4 = getShort(cal1, 12)
		dig_P5 = getShort(cal1, 14)
		dig_P6 = getShort(cal1, 16)
		dig_P7 = getShort(cal1, 18)
		dig_P8 = getShort(cal1, 20)
		dig_P9 = getShort(cal1, 22)

		dig_H1 = getUChar(cal2, 0)
		dig_H2 = getShort(cal3, 0)
		dig_H3 = getUChar(cal3, 2)

		dig_H4 = getChar(cal3, 3)
		dig_H4 = (dig_H4 << 24) >> 20
		dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

		dig_H5 = getChar(cal3, 5)
		dig_H5 = (dig_H5 << 24) >> 20
		dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

		dig_H6 = getChar(cal3, 6)

		# Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
		wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
		time.sleep(wait_time/1000)  # Wait the required time  

		# Read temperature/pressure/humidity
		data = bus.read_i2c_block_data(addr, REG_DATA, 8)
		pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
		temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
		hum_raw = (data[6] << 8) | data[7]

		#Refine temperature
		var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
		var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
		t_fine = var1+var2
		temperature = float(((t_fine * 5) + 128) >> 8);

		# Refine pressure and adjust for temperature
		var1 = t_fine / 2.0 - 64000.0
		var2 = var1 * var1 * dig_P6 / 32768.0
		var2 = var2 + var1 * dig_P5 * 2.0
		var2 = var2 / 4.0 + dig_P4 * 65536.0
		var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
		var1 = (1.0 + var1 / 32768.0) * dig_P1
		if var1 == 0:
			pressure=0
		else:
			pressure = 1048576.0 - pres_raw
			pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
			var1 = dig_P9 * pressure * pressure / 2147483648.0
			var2 = pressure * dig_P8 / 32768.0
			pressure = pressure + (var1 + var2 + dig_P7) / 16.0

		# Refine humidity
		humidity = t_fine - 76800.0
		humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
		humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
		if humidity > 100:
			humidity = 100
		elif humidity < 0:
			humidity = 0

		return temperature/100.0,pressure/100.0,humidity
	except Exception as e:
		print(f"ERROR - Fehler beim Lesen von BME280 all: {e}")
		return None, None, None

def main():
	global DEVICE

	# ArgumentParser-Objekt erstellen
	parser = argparse.ArgumentParser(description='Lesen des Klimasensors und Verarbeiten der Sensorwerte')
	parser.add_argument('-i', '--i2c', type=str, choices=['76', '77'], default='76',
						help='I2C Bus Adresse (76 or 77)')
	parser.add_argument('-f', '--file', action='store_true',
						help='schreiben in ein File - obsoloet durch globale xml Konfiguration')
	parser.add_argument('-s', '--screen', action='store_true',
						help='ausgeben am Bildschirm')

	# Argumente parsen
	args = parser.parse_args()

	# DEVICE entsprechend des Arguments setzen
	if args.i2c == '76':
		DEVICE = DEVICE1
	elif args.i2c == '77':
		DEVICE = DEVICE2

	# Sensordaten lesen
	chip_id, chip_version = readBME280ID(DEVICE)
	temperature, pressure, humidity = readBME280All(DEVICE)

	# Sensorwerte verarbeiten
	# Erstellen einer Instanz der CaravanPi Library
	cplib = CaravanPiFiles()
	cplib.handle_sensor_values(
		args.screen,										# Anzeige am Bildschirm?
		"klimasensor",										# sensor_name = Datenbankname
		"BME280-" + str(chip_id) + str(DEVICE),				# sensor_id = Filename und Spalte in der Datenbank
		["temperatur", "luftdruck", "luftfeuchtigkeit"],	# Liste Spaltennamen
		(temperature, pressure, humidity)					# Tupel Sensorwerte
	)              

if __name__=="__main__":
	main()
