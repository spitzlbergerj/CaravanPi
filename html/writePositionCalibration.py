#!/usr/bin/python3
# coding=utf-8
# writeScaleCalibration.py
#
# startet Kalibrierung
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
import os
import subprocess


# CGI handling
import cgi
import cgitb

# import for opening URL to change update Intervall on magic Mirror
import urllib.request

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

	# change update Intervall on MagicMirror
	urllib.request.urlopen('http://127.0.0.1:8089/ConfigSite/positionCalibration')

	# subprocess.run(["python3","/home/pi/CaravanPi/position/setupPositionDefaults.py"])

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
	print("Der Lage-Sensor wurde neu kalibriert.")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
