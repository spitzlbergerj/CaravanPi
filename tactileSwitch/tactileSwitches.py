#!/usr/bin/python3
# coding=utf-8
# tactileSwitches.py
#
# use tactile switches to start python scripts
#
# Aufruf-Parameter
# tactileSwitches.py -f
# 	-h	display guide 
# 	-f	write values to file 
# 	-s	display values on screen 
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
import getopt
import RPi.GPIO as GPIO
import subprocess
import os


# tactile switch calibration position sensor
pinSwitchPosition = 23
# tactile switch calibration gasscale
pinSwitchGasscale = 24

# -------------------------
# call options 
# -------------------------
shortOptions = 'h'
longOptions = ['help']

def usage():
	print ("---------------------------------------------------------------------")
	print (sys.argv[0], "-h")
	print ("  -h   show this guide")

def process_running(name):
    for fso in os.listdir('/proc'):
        path = os.path.join('/proc', fso)
        if os.path.isdir(path):
            try:
                # das Verzeichnis eines Prozesses trägt die
                # numerische UID als Namen
                uid = int(fso)
                stream = open(os.path.join(path, 'cmdline'))
                cmdline = stream.readline()
                stream.close()
                if name in cmdline and "/bin/sh" not in cmdline:
                    return uid
            except ValueError:
                # kein Prozessverzeichnis
                continue
    return 0
	
def switchInterruptPosition(channel):  
	# -------------------------
	# switchInterruptPosition
	# tactile switch was pressed start calibrating the position sensor
	# -------------------------
	print ("ACHTUNG: Kalibrierung Lage Sensor wird gestartet!")
	subprocess.run(["python3","/home/pi/CaravanPi/position/setupPositionDefaults.py","-w","5"])
	pid = process_running("position2file.py")
	print ("send SIGUSR1 to process ", pid)
	os.kill(pid, signal.SIGUSR1)
	print ("ACHTUNG: Kalibrierung Lage Sensor wurde beendet")

def switchInterruptGasscale(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("ACHTUNG: Kalibrierung Gaswaage wird gestartet!")
	subprocess.run(["python3","/home/pi/CaravanPi/gas-weight/setupGasscaleDefaults.py"])
	print ("ACHTUNG: Kalibrierung Gaswaage wurde beendet")



def main():
	# -------------------------
	# main 
	# -------------------------

	# -------------------------
	# process call parameters
	# -------------------------
	opts = []
	args = []
	writeFile = 0
	displayScreen = 0
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortOptions, longOptions)
	except getopt.GetoptError:
		print("ERROR: options not correct")
		usage()
		sys.exit()
	
	for o, a in opts:
		if o == "--help" or o == "-h":
			print("HELP")
			usage()
			sys.exit()

	for a in args:
		print("further argument: ", a)
		
	
	# -------------------------
	# tactile switches
	# -------------------------
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(pinSwitchPosition, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(pinSwitchPosition, GPIO.RISING, callback = switchInterruptPosition, bouncetime = 400)

	GPIO.setup(pinSwitchGasscale, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(pinSwitchGasscale, GPIO.RISING, callback = switchInterruptGasscale, bouncetime = 400)
	
	# -------------------------
	# endless loop
	# -------------------------
	while True:
		try:
			time.sleep(.5)						
		except KeyboardInterrupt:
			GPIO.cleanup()
			break
		except:
			print("unprocessed Error:", sys.exc_info()[0])
			GPIO.cleanup()
			raise


if __name__ == "__main__":
	main()
