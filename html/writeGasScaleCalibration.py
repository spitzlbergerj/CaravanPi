#!/usr/bin/python3
# coding=utf-8
# writeGasScaleDefaults.py
#
# liest die Daten aus einem Webformular und generiert daraus die unterschiedlichen Config Files
#
#-------------------------------------------------------------------------------

from sre_constants import CATEGORY_UNI_NOT_LINEBREAK
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
from hx711 import HX711
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
	cgi_testgewicht = form.getvalue('kal-testgewicht')

	flasche=float(cgi_number)
	testgewicht =float(cgi_testgewicht)

	# verhindern einer Division durch 0
	if (testgewicht == 0):
		testgewicht = 1

	#print(cgi_number, cgi_testgewicht)
	
	# Lesen der bisherigen Default Werte
	if (cgi_number != None):
		(emptyWeight, fullWeight, pin_dout, pin_sck, channel, refUnit) = CaravanPiFiles.readGasScale(flasche)

	subprocess.run(["python3","/home/pi/CaravanPi/gas-weight/gasScaleCalibration.py", "-c", "-e", cgi_testgewicht, "-g", cgi_number, "-w", "5"])


if __name__ == "__main__":
	main()
