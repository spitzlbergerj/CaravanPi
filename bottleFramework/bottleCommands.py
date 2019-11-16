#!/usr/bin/python3
# coding: utf8
# Webservice starten

from bottle import route, run, template
import subprocess
import time
import shlex

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
	else:
		return template('<b>Kommando nicht korrekt</b>!')


run(host='0.0.0.0', port=8089, debug=True)