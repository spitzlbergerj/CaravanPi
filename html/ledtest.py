#!/usr/bin/python3
# coding=utf-8
# ledtest.py
#
# startet LED Test Routinen
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
import os
import subprocess

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

	subprocess.run(["python3","/home/pi/CaravanPi/position/setupPositionDefaults.py"])

	# Ergebnis Website schreiben
	print("Content-Type: text/html; charset=utf-8\n\n")
	print("<html>")
	
	print("<head>")
	print("<title>CaravanPi Konfiguration</title>")
	print("<meta http-equiv='refresh' content='2; URL=ledtest.php'>")
	print("<link rel='stylesheet' type='text/css' href='css/main.css'>")
	print("<link rel='stylesheet' type='text/css' href='css/custom.css'>")
	print("</head>")

	print("<body>")
	print('<header class="header">CaravanPi Konfiguration - LED Test</header>')
	print("Die Testroutine wurde gestartet. Die LEDs sind für 60 Sekunden an.")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
