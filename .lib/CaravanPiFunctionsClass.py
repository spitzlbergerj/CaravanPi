#!/usr/bin/python3
# coding=utf-8
# CaravanPiClass.py
#
# prüft die Existenz eines Prozesses anhand dessen Namens
#
#Since this class is not initialized via __init__, the functions do not contain a fist parameter self
#
#-------------------------------------------------------------------------------
import sys
import os
import time


class CaravanPiFunctions:

	# -----------------------------------------------
	# global variables
	# -----------------------------------------------


	def __init__(self):
		# nichts zu tun
		return


	# -----------------------------------------------
	# determine process number pid
	# -----------------------------------------------
	def process_running(self, name):
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
	
	
	# -----------------------------------------------
	# Spiele einen Ton
	# -----------------------------------------------
	def play_tone(self, pwm, frequency, duration):
		if frequency > 0:
			pwm.ChangeFrequency(frequency)
			pwm.start(50)  # Start PWM mit 50% Tastverhältnis
		time.sleep(duration)
		pwm.stop()


	# -----------------------------------------------
	# Spiele die Melodie Erfolg
	# gpio ist bereits durch aufrufende Funktion initialisiert
	# -----------------------------------------------
	def play_melody(self, gpio, buzzer_pin, melody):
		# GPIO setup und PWM-Initialisierung
		gpio.setmode(gpio.BCM)
		gpio.setup(buzzer_pin, gpio.OUT)
		pwm = gpio.PWM(buzzer_pin, 1000)

		# Notenfrequenzen
		notes = {
			'G2': 98.00,
			'A3': 220.00,  
			'C4': 261.63,
			'E4': 329.63,
			'G4': 392.00,
			'C5': 523.25,
		}

		# Notendauern in Sekunden
		viertel = 0.25  # Kurze Noten
		halbe = 0.5  # Längere Note am Ende
		dreiviertel = 0.75  # Längere Note am Ende

		melodies = {
			'success': [
				('C4', viertel),
				('E4', viertel),
				('G4', viertel),
				('C5', halbe),
			],
			'failure': [
				('E4', halbe),
				('C4', halbe),
				('A3', halbe),
				('G2', dreiviertel),
			],
			# Hier können weitere Melodien hinzugefügt werden
		}
	
		cur_melody = melodies.get(melody, [])  # Leere Liste, falls `melody` nicht gefunden wird

	
		try:
			for note, duration in cur_melody:
				frequency = notes.get(note, 0)
				self.play_tone(pwm, frequency, duration)
				time.sleep(0.06)  # Kurze Pause zwischen den Noten
		finally:
			pwm.stop()
			gpio.cleanup(buzzer_pin)

		return 0
		
