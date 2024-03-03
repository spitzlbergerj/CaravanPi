#!/usr/bin/python3
# coding=utf-8
# CaravanPiClass.py
#
# prüft die Existenz eines Prozesses anhand dessen Namens
#
#Since this class is not initialized via __init__, the functions do not contain a fist parameter self
#
#-------------------------------------------------------------------------------
import os
import time
import psutil
import sys
import subprocess




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
	def process_running(self, partial_name):
		# Bestimmt die PID eines laufenden Prozesses anhand seines Namens.
		for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
			# Überprüft, ob der gesuchte Prozessname in der Kommandozeile enthalten ist
			if partial_name in ' '.join(proc.info['cmdline']):
				return proc.pid
		return 0
	
	# -----------------------------------------------
	# sende ein signal an einen Prozess, der einen String enthält
	# sende das Signal nur an den ersten gefunden
	# dies ist notwendig, da der prozess in der Prozessliste zweimal auftritt, da er durch cron gestartet wird
	# -----------------------------------------------

	def send_signal_to_process(self, partial_name, signal2process):
		found_process = None

		pid = self.process_running(partial_name)

		if pid:
			found_process = psutil.Process(pid)

			# gibt es Kindprozesse?
			# also wurde von crontab gestartet?
			children = found_process.children()
			if children:
				try:
					children[0].send_signal(signal2process)
					print(f"Signal {signal2process} wurde erfolgreich an Kindprozess {children[0].pid} gesendet.")
				except Exception as e:
					print(f"Fehler beim Senden von {signal2process} an Kindprozess {children[0].pid}: {e}")
					return -1
			else:
				# Versucht, das Signal an den Prozess (ohne Kindprozesse) zu senden
				# Prozess wurde anscheinend manuell gestartet
				try:
					found_process.send_signal(signal2process)
					print(f"Signal {signal2process} wurde erfolgreich an Prozess {found_process.pid} gesendet.")
				except Exception as e:
					print(f"Fehler beim Senden von {signal2process} an Prozess {found_process.pid}: {e}")
					return -1

			return 0
		else:
			print(f"Kein Prozess mit Teilstring '{partial_name}' gefunden.")
			return -1
		
	
	def start_process_in_background(self, command):
		try:
			# Stellt sicher, dass der Befehl als Hintergrundprozess läuft
			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			print(f"Prozess {process.pid} wurde erfolgreich im Hintergrund gestartet.")
			return 0
		except Exception as e:
			print(f"Fehler beim Starten des Prozesses: {e}")
			return -1

	
	# -----------------------------------------------
	# Spiele Alarmtöne
	# -----------------------------------------------
	def play_alarm_single(self, gpio, buzzer_pin, alarmnr):
		gpio.setmode(gpio.BCM)
		gpio.setup(buzzer_pin, gpio.OUT)

		# Muster für die verschiedenen Alarme als Liste von (Tonlänge, Pausenlänge)-Tupeln (jeweils in Sekunden)
		# Wartezeit beim letzten Eintrag immer 0.1, damit die Alarmausgabe keine zusätzlcihe Wartezeit verursacht, die bei Abschalten des Alarms über Config dann fehlt
		patterns = {
			0: [(0.05, 0.1), (0.5, 0.1)],  # Standardmuster für andere Alarme
			1: [(0.05, 0.1), (0.05, 0.1), (0.5, 0.1)],  # Alarm 1
			2: [(0.05, 0.1), (0.05, 0.1), (0.05, 0.1), (0.5, 0.1)],  # Alarm 2
			3: [(0.05, 0.1), (0.05, 0.1), (0.05, 0.1), (0.05, 0.1), (0.5, 0.1)],  # Alarm 2
		}

		# Muster basierend auf alarmnrsetzen
		pattern = patterns.get(alarmnr, patterns[0])

		# Durchlaufe das gewählte Muster
		for tone_length, pause_length in pattern:
			gpio.output(buzzer_pin, gpio.HIGH)
			time.sleep(tone_length)
			gpio.output(buzzer_pin, gpio.LOW)
			time.sleep(pause_length)

		return True

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
		
