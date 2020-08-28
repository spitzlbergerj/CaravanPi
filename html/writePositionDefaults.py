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
	
	cgi_tolX = form.getvalue('tolX')
	cgi_tolY = form.getvalue('tolY')
	cgi_approxX = form.getvalue('approxX')
	cgi_approxY = form.getvalue('approxY')
	cgi_distR = form.getvalue('dist-front')
	cgi_distF = form.getvalue('dist-right')
	cgi_distA = form.getvalue('dist-axis')
	
	#print(cgi_tolX, cgi_tolY, cgi_approxX, cgi_approxY, cgi_distR, cgi_distF, cgi_distA)
	
	(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis) = CaravanPiFiles.readAdjustment()
	
	if (cgi_tolX != None and cgi_tolY != None and cgi_approxX != None and cgi_approxX != None and cgi_distF != None and cgi_distR != None and cgi_distA != None):
		toleranceX = float(cgi_tolX)
		toleranceY = float(cgi_tolY)
		approximationX = float(cgi_approxX)
		approximationY = float(cgi_approxY)
		distRight = float(cgi_distR)
		distFront = float(cgi_distF)
		distAxis = float(cgi_distA)
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
	print('<header class="header">CaravanPi Konfiguration - Einstellungen Lage-Sensor</header>')
	if (cgi_tolX != None and cgi_tolY != None and cgi_approxX != None and cgi_approxX != None and cgi_distF != None and cgi_distR != None and cgi_distA != None):
		print("Die eingegebenen Werte wurden erfolgreich gespeichert")
	else:
		print("ES KONNTEN KEINE WERTE AUS DEM FORMULAR GELESEN WERDEN!")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
