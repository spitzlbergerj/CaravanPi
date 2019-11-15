#!/usr/bin/python3
# coding=utf-8
# writeConfig.py
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
from filesClass import CaravanPiFiles

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
	
	cgi_adjustX = form.getvalue('adjustX')
	cgi_adjustY = form.getvalue('adjustY')
	cgi_adjustZ = form.getvalue('adjustZ')
	
	#print(cgi_adjustX, cgi_adjustY, cgi_adjustZ)
	
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis) = CaravanPiFiles.readAdjustment()
	
	if (cgi_adjustX != None and cgi_adjustY != None and cgi_adjustZ != None):
		adjustX = float(cgi_adjustX)
		adjustY = float(cgi_adjustY)
		adjustZ = float(cgi_adjustZ)
		CaravanPiFiles.writeAdjustment(0, 0, adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis)

	# Ergebnis Website schreiben
	print("Content-Type: text/html; charset=utf-8\n\n")
	print("<html>")
	
	print("<head>")
	print("<title>CaravanPi Konfiguration</title>")
	print("<meta http-equiv='refresh' content='2; URL=position.php'>")
	print("<link rel='stylesheet' type='text/css' href='css/main.css'>")
	print("<link rel='stylesheet' type='text/css' href='css/custom.css'>")
	print("</head>")

	print("<body>")
	print('<header class="header">CaravanPi Konfiguration - manuelle Einstellungen Lage-Sensor</header>')
	if (cgi_adjustX != None and cgi_adjustY != None and cgi_adjustZ != None):
		print("Die eingegebenen Werte wurden erfolgreich gespeichert")
	else:
		print("ES KONNTEN KEINE WERTE AUS DEM FORMULAR GELESEN WERDEN!")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
