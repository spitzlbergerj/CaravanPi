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

	subprocess.run(["python3","/home/pi/CaravanPi/gas-weight/setupGasscaleDefaults.py"])

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
	print('<header class="header">CaravanPi Konfiguration - Dimensionen Cravan / Wohnmobil</header>')
	print("Die Gasflaschen-Waage wurde neu kalibriert.")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
