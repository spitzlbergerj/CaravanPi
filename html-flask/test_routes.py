#
#
#

import sys
import signal
import subprocess
import RPi.GPIO as GPIO

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles
from CaravanPiFunctionsClass import CaravanPiFunctions

cplibfiles = CaravanPiFiles()
cplibfunctions = CaravanPiFunctions()

# -----------------------------------------------
# Handling der Taster
# - Zustandsspeicherung
# - Interruptbehandlung
# -----------------------------------------------

switchTestStarted = False

# Globales Dictionary zur Speicherung der Zustände
switch_states = {
    'position': False,
    'gasscale': False,
    'horizontal': False,
    'live': False,
}

eventstriggered = False

def setup_gpio():
	eventstriggered = True
	GPIO.setmode(GPIO.BCM)

	pinSwitchPosition = 19
	GPIO.setup(pinSwitchPosition, GPIO.IN)
	GPIO.remove_event_detect(pinSwitchPosition)
	GPIO.add_event_detect(pinSwitchPosition, GPIO.RISING, callback = switchInterruptPosition, bouncetime = 400)

	pinSwitchGasscale = 22
	GPIO.setup(pinSwitchGasscale, GPIO.IN)
	GPIO.remove_event_detect(pinSwitchGasscale)
	GPIO.add_event_detect(pinSwitchGasscale, GPIO.RISING, callback = switchInterruptGasscale, bouncetime = 400)
	
	pinSwitchNowHorizontal = 6
	GPIO.setup(pinSwitchNowHorizontal, GPIO.IN)
	GPIO.remove_event_detect(pinSwitchNowHorizontal)
	GPIO.add_event_detect(pinSwitchNowHorizontal, GPIO.RISING, callback = switchInterruptNowHorizontal, bouncetime = 400)

	pinSwitchLive = 13
	GPIO.setup(pinSwitchLive, GPIO.IN)
	GPIO.remove_event_detect(pinSwitchLive)
	GPIO.add_event_detect(pinSwitchLive, GPIO.RISING, callback = switchInterruptLive, bouncetime = 400)

	pinLEDLive = 5
	GPIO.setup(pinLEDLive, GPIO.OUT)	
	GPIO.output(pinLEDLive, False)

	return 0

def release_gpio():
	if not eventstriggered:
		return 0
	
	GPIO.setmode(GPIO.BCM)

	# Entfernen der Event-Detektion
	pinSwitchPosition = 19
	GPIO.remove_event_detect(pinSwitchPosition)
	
	pinSwitchGasscale = 22
	GPIO.remove_event_detect(pinSwitchGasscale)

	pinSwitchNowHorizontal = 6
	GPIO.remove_event_detect(pinSwitchNowHorizontal)

	pinSwitchLive = 13
	GPIO.remove_event_detect(pinSwitchLive)

	return 0
    

# Funktion, die den Zustand aktualisiert
def set_switch_state(switch_name, state):
    switch_states[switch_name] = state

# Funktion, die den aktuellen Zustand abfragt
def get_switch_state(switch_name):
    return switch_states.get(switch_name, False)

def switchInterruptPosition(channel):  
	# -------------------------
	# switchInterruptPosition
	# tactile switch was pressed start calibrating the position sensor
	# -------------------------
	print ("Taster Kalibrierung Lage Sensor wurde gedrückt")
	switch_states['position'] = True  # Zustand aktualisieren

def switchInterruptGasscale(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("Taster Kalibrierung Gaswaage wurde gedrückt")
	switch_states['gasscale'] = True  # Zustand aktualisieren

def switchInterruptNowHorizontal(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("Taster Querlage = Horizontal wurde gedrückt")
	switch_states['horizontal'] = True  # Zustand aktualisieren

def switchInterruptLive(channel):  
	# -------------------------
	# switchInterruptGasscale 
	# tactile switch was pressed start calibrating the gas scale
	# -------------------------
	print ("Taster Live-Modus wurde gedrückt")
	switch_states['live'] = True  # Zustand aktualisieren
	print ("--> LED Live Modus leuchtet für 1/2 Sekunde")
	GPIO.output(pinLEDLive, True)
	time.sleep(.5)
	GPIO.output(pinLEDLive, False)

# -----------------------------------------------
#
# Routen
#
# -----------------------------------------------

def register_test_routes(app):

	@app.route('/tests_home')
	def tests_home():
		global switchTestStarted
		switchTestStarted = False
		return render_template('tests_home.html')

	@app.route('/test_LEDs', methods=['GET', 'POST'])
	def route_test_LEDs():

		if request.method == 'POST':
			if 'cancel' in request.form:
				# Testfarbe auf AUS setzen
				cplibfiles.writeCaravanPiConfigItem("testColor/color", "99")

				# SIGUSR2 senden, damit Test beendet wird, allerdings nur, wenn mindestens ein Test gestartet wurde
				cplibfunctions.send_signal_to_process("position2file.py", signal.SIGUSR2)

				return redirect(url_for('tests_home'))  # Leitet um zur `/tests_home`-Route

			if 'LEDgreen' in request.form:
				# Meldung anzeigen
				flash('LEDs auf grün geschaltet')

				# Testcolor setzen
				cplibfiles.writeCaravanPiConfigItem("testColor/color", "-2")

				# SIGUSR2 senden
				cplibfunctions.send_signal_to_process("position2file.py", signal.SIGUSR2)

				return redirect(url_for('route_test_LEDs'))

			if 'LEDgreenblink' in request.form:
				# Meldung anzeigen
				flash('LEDs auf grün blinkend geschaltet')

				# Testcolor setzen
				cplibfiles.writeCaravanPiConfigItem("testColor/color", "-1")

				# SIGUSR2 senden
				cplibfunctions.send_signal_to_process("position2file.py", signal.SIGUSR2)

				return redirect(url_for('route_test_LEDs'))

			if 'LEDred' in request.form:
				# Meldung anzeigen
				flash('LEDs auf rot geschaltet')

				# Testcolor setzen
				cplibfiles.writeCaravanPiConfigItem("testColor/color", "0")

				# SIGUSR2 senden
				cplibfunctions.send_signal_to_process("position2file.py", signal.SIGUSR2)

				return redirect(url_for('route_test_LEDs'))

			if 'LEDblueblink' in request.form:
				# Meldung anzeigen
				flash('LEDs auf blau blinkend geschaltet')

				# Testcolor setzen
				cplibfiles.writeCaravanPiConfigItem("testColor/color", "1")

				# SIGUSR2 senden
				cplibfunctions.send_signal_to_process("position2file.py", signal.SIGUSR2)

				return redirect(url_for('route_test_LEDs'))
			
			if 'LEDblue' in request.form:
				# Meldung anzeigen
				flash('LEDs auf blau geschaltet')

				# Testcolor setzen
				cplibfiles.writeCaravanPiConfigItem("testColor/color", "2")

				# SIGUSR2 senden
				cplibfunctions.send_signal_to_process("position2file.py", signal.SIGUSR2)

				return redirect(url_for('route_test_LEDs'))

		return render_template('test_LEDs.html')



	@app.route('/test_switches', methods=['GET', 'POST'])
	def route_test_switches():
		global switchTestStarted

		if request.method == 'POST':
			if 'cancel' in request.form:
				switchTestStarted = False

				# GPIO säubern
				release_gpio()

				# Starten des Prozesses tactileSwitches.py, soweit er nicht schon läuft
				if cplibfunctions.process_running("tactileSwitches.py") == 0:
					cplibfunctions.start_process_in_background("python3 -u /home/pi/CaravanPi/tactileSwitch/tactileSwitches.py >/home/pi/CaravanPi/.log/tactileSwitches.log 2>&1")

				return redirect(url_for('tests_home'))  # Leitet um zur `/tests_home`-Route

			if 'start' in request.form:
				switchTestStarted = True
				# Stoppen des Prozesses tactileSwitches.py, falls er läuft
				print("Prozess stoppen ....")
				if cplibfunctions.process_running("tactileSwitches.py") > 0:
					print("Prozess läuft")
					if cplibfunctions.send_signal_to_process("tactileSwitches.py", signal.SIGKILL) != 0:
						print("Fehler beim killen")
						flash('Prozess tactileSwitches.py konnte nicht gestoppt werden')
						return render_template('test_switches.html')
					else:
						print("Prozess gekilled")
				else:
					print("Prozess läuft nicht")
						
				flash('Prozess tactileSwitches.py läuft nicht (mehr).')

				# GPIO Eventsteuerung
				setup_gpio()
			
			# Template erneut rendern
		return render_template('test_switches.html', switchTestStarted=switchTestStarted)


	@app.route('/poll_switch_status/<switch_name>')
	def poll_switch_status(switch_name):
		state = get_switch_state(switch_name)
		if state:
			set_switch_state(switch_name, False)
			# Nachricht zurückgeben 
			return jsonify({'pressed': True, 'message': f'Taster {switch_name} wurde gedrückt.'})
		else:
			return jsonify({'pressed': False})



	@app.route('/test_buzzer', methods=['GET', 'POST'])
	def route_test_buzzer():

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('tests_home'))  # Leitet um zur `/tests_home`-Route

			if 'start' in request.form:
				# Meldung anzeigen
				flash('Buzzer wurde getestet')
				flash('zunächst langsames Beepen')
				flash('dann schnelles Beepen')
				flash('dann Dauerton')
				flash('schließlich Melodie')

			try:
				# Angenommen, Ihr Skript befindet sich im selben Verzeichnis und heißt script.py
				result = subprocess.run(['python3', '/home/pi/CaravanPi/position/buzzerTest.py'], capture_output=True, text=True, check=True)
			except subprocess.CalledProcessError as e:
				print(f"Fehler beim Ausführen des Skripts: {e.stderr}")

			return redirect(url_for('route_test_buzzer'))

		return render_template('test_buzzer.html')

