#!/usr/bin/python3
# coding=utf-8
# CaravanPiActorsClass.py
#
# Class für das Ansprechen von Aktoren
#
#-------------------------------------------------------------------------------
import os
import time
import sys
import subprocess
import requests


class CaravanPiActors:

	# -----------------------------------------------
	# global variables
	# -----------------------------------------------

	# -----------------------------------------------
	# Initialisieren
	# -----------------------------------------------

	def __init__(self):
		# nichts zu tun
		return


	# -----------------------------------------------
	# Universelle Funktion zum Senden von HTTP Requests
	#
	# 	method: Die HTTP-Methode ('GET', 'POST', etc.)
	# 	url: Die URL für den Request
	# 	kwargs: Zusätzliche Argumente für requests (z.B. json für POST-Daten)
	# 	return: Das Response-Objekt
	# -----------------------------------------------

	def send_request(self, method, url, **kwargs):
		try:
			response = requests.request(method, url, **kwargs)
			return response
		except Exception as e:
			print(f'Fehler beim Senden des Requests: {e}')
			return None

	# -----------------------------------------------
	# Sendet einen HTTP-GET-Request.
	#
	#	url: Die URL für den GET-Request
	#	params: Ein Dictionary mit URL-Parametern
	#	return: Das Response-Objekt
	# -----------------------------------------------


	def get(self, url, params=None):
		return self.send_request('GET', url, params=params)

	# -----------------------------------------------
	#	Sendet einen HTTP-POST-Request.
	#
	#	url: Die URL für den POST-Request
	#	data: Das Dictionary mit Form-Daten
	#	json: Das Dictionary mit JSON-Daten
	#	return: Das Response-Objekt
	# -----------------------------------------------

	def post(self, url, data=None, json=None):
		return self.send_request('POST', url, data=data, json=json)
