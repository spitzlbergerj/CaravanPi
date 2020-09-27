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
	
	cgi_number = form.getvalue('tankNumber')
	tankNumber = int(cgi_number)
	cgi_level1 = form.getvalue('level1')
	cgi_level2 = form.getvalue('level2')
	cgi_level3 = form.getvalue('level3')
	cgi_level4 = form.getvalue('level4')
	
	# print(cgi_number, cgi_level1, cgi_level2, cgi_level3, cgi_level4)

	if (cgi_number != None):
		(level1, level2, level3, level4) = CaravanPiFiles.readFillLevels(tankNumber)
	
	if (cgi_number != None and cgi_level1 != None and cgi_level2 != None and cgi_level3 != None and cgi_level4 != None):
		level1 = float(cgi_level1)
		level2 = float(cgi_level2)
		level3 = float(cgi_level3)
		level4 = float(cgi_level4)
		CaravanPiFiles.writeFillLevels(tankNumber, 0, 0, level1, level2, level3, level4)

	# Ergebnis Website schreiben
	print("Content-Type: text/html; charset=utf-8\n\n")
	print("<html>")
	
	print("<head>")
	print("<title>CaravanPi Konfiguration</title>")
	print("<meta http-equiv='refresh' content='2; URL=fill-levels.php'>")
	print("<link rel='stylesheet' type='text/css' href='css/main.css'>")
	print("<link rel='stylesheet' type='text/css' href='css/custom.css'>")
	print("</head>")

	print("<body>")
	print('<header class="header">CaravanPi Konfiguration - Füllstände Tanks</header>')
	if (cgi_number != None and cgi_level1 != None and cgi_level2 != None and cgi_level3 != None and cgi_level4 != None):
		print("Die eingegebenen Werte wurden erfolgreich gespeichert")
	else:
		print("ES KONNTEN KEINE WERTE AUS DEM FORMULAR GELESEN WERDEN!")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
