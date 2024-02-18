# ------------------------------------------------------------------------------------
# Flask Routen für die Kalibrierungen
# ------------------------------------------------------------------------------------

import sys
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------

sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

cplib = CaravanPiFiles()
caravanpiDefaults_tuple = cplib.readCaravanPiDefaults()
if caravanpiDefaults_tuple is None:
	gasscales_max = 0
else:
	gasscales_max = caravanpiDefaults_tuple[0] if caravanpiDefaults_tuple[0] is not None else 0


# -----------------------------------------------
# Routen
# -----------------------------------------------

def register_calibration_routes(app):

	# -----------------------------------------------
	# zentrale Variable als app Bestandteil
	# -----------------------------------------------

	# Definieren der Kalibrierungsoptionen als Konfigurationseinstellung
	app.config['CALIBRATION_OPTIONS'] = {
		'gasscales': {
			'name': 'Kalibrierung der Gasflaschenwaagen',
			'instructions': 'Bitte führen Sie die Kalibrierung der Waagen nur bei ausgerichtetem Caravan bzw. Wohnmobil durch. Positionieren Sie dann ein Testgewicht auf der Waage und geben Sie dessen Gewicht unten an. Tragen Sie ebenfalls die Wartezeit ein, die vor der Kalibrierung gewartet werden soll, um Schwingungen abklingen zu lassen. Wählen Sie zudem aus, welche Waage kalibriert werden soll. Starten Sie dann die Kalibrierung durch einen Klick auf den Start Button',
			'max_scales': gasscales_max,
			'script' : '/home/pi/CaravanPi/gas-weight/gasScaleCalibration.py -g NR -e WEIGHT -w WAIT -s',
			'scale_number' : 0,
			'weight' : 0,
			'wait_time' : 0,
		},
		'lagesensor': {
			'name': 'Kalibrierung des Lagesensors',
			'instructions': 'Bitte richten Sie den Caravan bzw. das Wohnmobil möglichst exakt waagrecht aus. Während der Kalibrierung dürfen sich im Caravan bzw. im Wohnmobil keine Personen aufhalten. Ebenso sollten Geräte, die Vibrationen verursachen können, vollständig ausgeschaltet sein. Lassen Sie das Fahrzeug dann einige Minuten ruhig und unverändert stehen, bis alle Schwingungen abgeklungen sind. Starten Sie dann die Kalibrierung durch klick auf den Button unten. Die Kalibrierungssequenz wird weitere zwei Minuten warten, bevor die Sensordaten ausgelesen werden. Der Summer signalisiert dann die eigentliche Kalibrierung.',
			'script' : '/home/pi/CaravanPi/position/setupPositionDefaults.py -w WAIT',
			'wait_time' : 0,
		}
	}

	@app.route('/calibration')
	def route_calibration_home():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		return render_template('calibration_base_template.html', stage='choose', calibration_options=calibration_options)

	@app.route('/calibration/gasscales')
	def route_gasscales_calibration():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		return render_template('calibration_base_template.html', stage='input_gasscales', calibration_options=calibration_options)
		
	@app.route('/calibration/lagesensor')
	def route_positionsensor_calibration():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		return render_template('calibration_base_template.html', stage='input_lagesensor', calibration_options=calibration_options)

	@app.route('/calibration/execute/gasscales', methods=['POST'])
	def route_execute_gasscale_calibration():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		calibration_options['gasscales']['scale_number'] = request.form['scale_number']
		calibration_options['gasscales']['weight'] = request.form['weight']
		calibration_options['gasscales']['wait_time'] = request.form['wait_time']

		# Rendern des Templates mit Stage 'progress'
		return render_template('calibration_base_template.html', stage='progress_gasscale', calibration_options=calibration_options, scale_number=calibration_options['gasscales']['scale_number'], weight=calibration_options['gasscales']['weight'], wait_time=calibration_options['gasscales']['wait_time'])

	@app.route('/calibration/running/gasscales')
	def route_calibration_gasscale_running():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		scale_number = calibration_options['gasscales']['scale_number']
		weight = calibration_options['gasscales']['weight']
		wait_time = calibration_options['gasscales']['wait_time']
		script = app.config['CALIBRATION_OPTIONS']['gasscales']['script']

		# Ersetzen der Platzhalter in dem Skriptpfad mit den Formulardaten
		script_with_params = f'python3 {script.replace("NR", scale_number).replace("WEIGHT", weight).replace("WAIT", wait_time)}'
		print(script_with_params)

		# Aufruf des Skripts mit den ersetzen Parametern
		subprocess.run(script_with_params.split(), check=True)

		return redirect(url_for('route_calibration_complete'))


	@app.route('/calibration/execute/lagesensor', methods=['POST'])
	def route_execute_lagesensor_calibration():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		wait_time = request.form['wait_time']
		script = app.config['CALIBRATION_OPTIONS']['lagesensor']['script']

		# Rendern des Templates mit Stage 'progress'
		response = render_template('calibration_base_template.html', stage='progress_lagesensor', calibration_options=calibration_options, wait_time=wait_time)

		# Ersetzen der Platzhalter in dem Skriptpfad mit den Formulardaten
		script_with_params = f'python3 {script.replace("WAIT", wait_time)}'
		print(script_with_params)

		# Aufruf des Skripts mit den ersetzen Parametern
		subprocess.run(script_with_params.split(), check=True)

		return redirect(url_for('route_calibration_complete'))

	@app.route('/calibration/complete')
	def route_calibration_complete():
		calibration_options = app.config['CALIBRATION_OPTIONS']

		# Anzeigen der Ergebnisse nach der Kalibrierung
		return render_template('calibration_base_template.html', stage='result', results="Ergebnisse der Kalibrierung.", calibration_options=calibration_options)
