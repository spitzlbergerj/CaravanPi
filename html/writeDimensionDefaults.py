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
	
	cgi_lengthOverAll = form.getvalue('laenge-alles')
	cgi_width = form.getvalue('breite-alles')
	cgi_lengthBody = form.getvalue('laenge-aufbau')
	
	#print(cgi_lengthOverAll, cgi_width, cgi_lengthBody)
	
	if (cgi_lengthOverAll != None and cgi_width != None and cgi_lengthBody != None):
		lengthOverAll = float(cgi_lengthOverAll)
		width = float(cgi_width)
		lengthBody = float(cgi_lengthBody)
		CaravanPiFiles.writeDimensions(0, 0, lengthOverAll, width, lengthBody)

	# Ergebnis Website schreiben
	print("Content-Type: text/html; charset=utf-8\n\n")
	print("<html>")
	
	print("<head>")
	print("<title>CaravanPi Konfiguration</title>")
	print("<meta http-equiv='refresh' content='2; URL=dimensions.php'>")
	print("<link rel='stylesheet' type='text/css' href='css/main.css'>")
	print("<link rel='stylesheet' type='text/css' href='css/custom.css'>")
	print("</head>")

	print("<body>")
	print('<header class="header">CaravanPi Konfiguration - Dimensionen Cravan / Wohnmobil</header>')
	if (cgi_lengthOverAll != None and cgi_width != None and cgi_lengthBody != None):
		print("Die eingegebenen Werte wurden erfolgreich gespeichert")
	else:
		print("ES KONNTEN KEINE WERTE AUS DEM FORMULAR GELESEN WERDEN!")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
