#!/usr/bin/python3
# coding: utf8
# Webservice starten

from bottle import route, run, template
import subprocess
import time
import sys
import shlex
import requests

# -----------------------------------------------
# libraries from CaravanPi
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFunctionsClass import CaravanPiFunctions


@route('/ConfigSite/<cmd>')
def index(cmd):
	if cmd == "positionCalibration":
		cmdstring = 'python3 /home/pi/CaravanPi/position/setupPositionDefaults.py';
		subprocess.Popen(shlex.split(cmdstring));
		return template('<b>Kommando {{cmdstring}} ausgeführt</b>!', cmdstring=cmdstring)
	elif cmd == "gasScaleCalibration":
		cmdstring = 'python3 /home/pi/CaravanPi/gas-weight/setupGasscaleDefaults.py';
		subprocess.Popen(shlex.split(cmdstring));
		return template('<b>Kommando {{cmdstring}} ausgeführt</b>!', cmdstring=cmdstring)
	elif cmd == "LEDtest":
		pid = CaravanPiFunctions.process_running("position2file.py")
		cmdstring = 'kill -SIGUSR2 '+ str(pid);
		subprocess.Popen(shlex.split(cmdstring));
		return template('<b>Kommando {{cmdstring}} ausgeführt</b>!', cmdstring=cmdstring)
	elif cmd == "MMtest":
		cmdstring = 'http://127.0.0.1:8080/api/module/alert/showalert?message=Dies%20ist%20ein%20Test&timer=4000';
		r = requests.get(url = cmdstring);
		return template('<b>Kommando {{cmdstring}} ausgeführt</b>!', cmdstring=cmdstring)
	else:
		return template('<b>Kommando nicht korrekt</b>!')


run(host='0.0.0.0', port=8089, debug=True)
