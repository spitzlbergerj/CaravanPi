#!/usr/bin/python3
# coding=utf-8
# writeGasCylinderDefaults.py
#
# liest die Daten aus einem Webformular und generiert daraus die unterschiedlichen Config Files
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
import os

# CGI handling
import cgi
import cgitb

# -----------------------------------------------
# libraries from CaravanPi
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

# -----------------------------------------------
# global variables
# -----------------------------------------------

def main():
	# -------------------------
	# main 
	# -------------------------

	# lesen der Werte aus der HTML form
	cgitb.enable(display=0, logdir="/var/log/apache2")
	
	form = cgi.FieldStorage()
	
	cgi_number = form.getvalue('flasche-nr')
	cgi_leer = form.getvalue('gewicht-leer')
	cgi_voll = form.getvalue('gewicht-voll')
	cgi_pin_dout = form.getvalue('gpio-pin-dout')
	cgi_pin_sck = form.getvalue('gpio-pin-sck')
	cgi_channel = form.getvalue('hx711-channel')
	cgi_refUnit = form.getvalue('hx711-refUnit')
	
	# print(cgi_number, cgi_leer, cgi_voll, cgi_pin_dout, cgi_pin_sck, cgi_channel, cgi_refUnit)

	if (cgi_number != None):
		(emptyWeight, fullWeight, pin_dout, pin_sck, channel, refUnit) = CaravanPiFiles.readGasScale(float(cgi_number))
	
	if (cgi_number != None and cgi_leer != None and cgi_voll != None and cgi_pin_dout != None and cgi_pin_sck != None and cgi_channel != None and cgi_refUnit != None):
		emptyWeight = float(cgi_leer)
		fullWeight = float(cgi_voll)
		pin_dout = float(cgi_pin_dout)
		pin_sck = float(cgi_pin_sck)
		channel = cgi_channel
		refUnit = float(cgi_refUnit)

		CaravanPiFiles.writeGasScale(float(cgi_number), 0, 0, emptyWeight, fullWeight, pin_dout, pin_sck, channel, refUnit)

	# Ergebnis Website schreiben
	print("Content-Type: text/html; charset=utf-8\n\n")
	print("<html>")
	
	print("<head>")
	print("<title>CaravanPi Konfiguration</title>")
	print("<meta http-equiv='refresh' content='2; URL=gas-scale.php'>")
	print("<link rel='stylesheet' type='text/css' href='css/main.css'>")
	print("<link rel='stylesheet' type='text/css' href='css/custom.css'>")
	print("</head>")

	print("<body>")
	print('<header class="header">CaravanPi Konfiguration - Gasflaschen-Gewichte</header>')
	if (cgi_number != None and cgi_leer != None and cgi_voll != None and cgi_pin_dout != None and cgi_pin_sck != None and cgi_channel != None and cgi_refUnit != None):
		print("Die eingegebenen Werte wurden erfolgreich gespeichert")
	else:
		print("ES KONNTEN KEINE bzw. NICHT ALLE WERTE AUS DEM FORMULAR GELESEN WERDEN!")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
