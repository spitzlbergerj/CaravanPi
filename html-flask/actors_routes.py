#
#
#

import sys
import signal
import threading
import requests
import RPi.GPIO as GPIO

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles
from CaravanPiFunctionsClass import CaravanPiFunctions
from CaravanPiActorsClass import CaravanPiActors

cplibfiles = CaravanPiFiles()
cplibfunctions = CaravanPiFunctions()
cplibactors = CaravanPiActors()

# -----------------------------------------------
# Funktionen
# -----------------------------------------------

def toggle_led_async(url):
	# -------------------------------------------
	# LED Kommandos asynchron senden, damit die 
	# Abarbeitung der Webanfrage in Flask diese
	# Aktion nicht behindert/verzögert
	# -------------------------------------------
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("HTTP erfolgreich")
        else:
            print("HTTP nicht erfolgreich")
    except Exception as e:
        print(f'Fehler: {str(e)}')

# -----------------------------------------------
#
# Routen
#
# -----------------------------------------------

def register_actors_routes(app):

	@app.route('/actors/tastendruck', methods=['GET'])
	def actor_tastendruck():
		device_id = request.args.get('device_id')
		status = request.args.get('status')
		print(f"Aktor Event: {device_id}, {status}")

		# LED am ESP einschalten oder ausschalten

		if int(status) == 1:
			url = f'http://192.168.178.190/control?cmd=GPIO,14,1'
		else:
			url = f'http://192.168.178.190/control?cmd=GPIO,14,0'

		# Starten des asynchronen Vorgangs
		threading.Thread(target=toggle_led_async, args=(url,)).start()

		return jsonify({"message": "LED Staus wird aktualisiert"}), 202

	@app.route('/actors/LED', methods=['GET', 'POST'])
	def actor_LED():
		# URL-Parameter abrufen
		# Aufruf .../actors/LED?LED_status=on
		# 'GET' wird erlaubt, damit auch im Browser diese URL aufgerufen werden kann
		LED_status = request.args.get('LED_status')

		# oder auch
		# Daten aus dem Body des POST-Requests abrufen
		data = request.json

		if LED_status == "on":
			url = f'http://192.168.178.190/control?cmd=GPIO,14,1'
		else:
			url = f'http://192.168.178.190/control?cmd=GPIO,14,0'

		# Starten des asynchronen Vorgangs
		threading.Thread(target=toggle_led_async, args=(url,)).start()

		if request.method == 'GET':
			# URL des Referers aus den Request-Headern holen
			referer_url = request.headers.get('Referer')
			if referer_url:
				# Redirect zur ursprünglichen URL
				return redirect(referer_url)

		return jsonify({"message": "LED Staus wird aktualisiert"}), 202

