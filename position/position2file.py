#!/usr/bin/python3
# coding=utf-8
# position2file.py
#
# schreibt die aus dem Beschleunigungssensor ADXL345 gelesenen Lagewerte in eine Datei
# lediglich zur generellen Anzeige nutzen.
# zum Wohnwagen ausrichten anderes Skript nutzen
#
#-------------------------------------------------------------------------------

import time, datetime
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

def write2file(x, y, z):
#	try:
		dateiName = "/home/pi/CaravanPi/values/lage"
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strX = '{:.6f}'.format(x)
		strY = '{:.6f}'.format(y)
		strZ = '{:.6f}'.format(z)
		file.write("\n"+ str_from_time_now + " " + strX + " " + strY + " " + strZ)
		file.close()
		return 0
#	except:
#		# Schreibfehler
#		print ("Die Datei konnte nicht geschrieben werden.")
#		return -1

(x, y, z) = accelerometer.acceleration
write2file(x, y, z)
