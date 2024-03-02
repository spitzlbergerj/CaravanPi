#!/usr/bin/python3
# coding=utf-8
# buttontest.py
#
# LED leuchtet, wenn Button auf Website gedrückt wird
#
#-------------------------------------------------------------------------------

import time
import RPi.GPIO as io

LED_PIN = 21

def main():
	# -------------------------
	# main 
	# -------------------------

	# GPIO konfigurieren
	io.setmode(io.BCM)

	io.setup(LED_PIN, io.OUT)

	io.output(LED_PIN, io.LOW)
	io.output(LED_PIN, io.HIGH)
	time.sleep(1)
	io.output(LED_PIN, io.LOW)
	io.cleanup()
	
	print ("Content-Type: text/html; charset=utf-8\n\n")
	print ("<html>")
	print ("<body>")
	print ('<SCRIPT language="JavaScript">')
	print ('<!--')
	print ('setTimeout("window.location.href=' + "'index.html'" + '",0);')
	print ('// -->')
	print ('</SCRIPT>')
	print ("</body>")
	print ("</html>")
	

if __name__ == "__main__":
	main()
