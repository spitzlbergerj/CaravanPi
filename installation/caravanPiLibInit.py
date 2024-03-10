#!/usr/bin/python3
# coding=utf-8
#
#-------------------------------------------------------------------------------

import sys
from datetime import datetime 

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles


def main():
	cplib = CaravanPiFiles()
	print("CaravanPiFiles wurde erfolgreich initialisiert und Konvertierung durchgeführt.")		

if __name__=="__main__":
	result = main()
	sys.exit(result)