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
from CaravanPiFunctionsClass import CaravanPiFunctions

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
	
	cgi_color = form.getvalue('color')
	
	#print(cgi_color)
	
	if (cgi_color != None):
		CaravanPiFiles.writeTestColor(0, 0, cgi_color)
		# send kill SIGUSR2 to position2file.py
		urllib.request.urlopen('http://127.0.0.1:8089/ConfigSite/LEDtest')
		if cgi_color == "-2":
			strColor = "grün"
		elif cgi_color == "-1":
			strColor = "grün blinkend"
		elif cgi_color == "0":
			strColor = "rot"
		elif cgi_color == "1":
			strColor = "blau blinkend"
		elif cgi_color == "2":
			strColor = "blau"
		elif cgi_color == "99":
			strColor = "aus"
		else:
			strColor = "----"

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
	if (cgi_color != None):
		print("Die Testroutine wurde gestartet. Die LEDs schalten für mindestens 60 Sekunden auf "+strColor)
	else:
		print("ES KONNTEN KEINE WERTE AUS DEM FORMULAR GELESEN WERDEN!")
	print("<br/><br/>Sie werden zur Eingabeseite weitergeleitet")
	print("</body>")
	print("</html>")


if __name__ == "__main__":
	main()
