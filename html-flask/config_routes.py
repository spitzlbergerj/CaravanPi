#
#
#

import sys
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

cplib = CaravanPiFiles()



def register_config_routes(app):

	@app.route('/configs', methods=['GET', 'POST'])
	def config_home():
		return render_template('config.html')

	@app.route('/config_caravanpi', methods=['GET', 'POST'])
	def config_caravanpi():

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('config_home'))  # Leitet um zur `/configs`-Route

			if 'submit' in request.form:
				# Daten aus dem Formular extrahieren
				countGasScales = request.form.get('countGasScales')
				countTanks = request.form.get('countTanks')
				write2file = request.form.get('write2file')
				write2MariaDB = request.form.get('write2MariaDB')
				send2MQTT = request.form.get('send2MQTT')
				MariaDBhost = request.form.get('MariaDBhost')
				MariaDBuser = request.form.get('MariaDBuser')
				MariaDBpasswd = request.form.get('MariaDBpasswd')
				MariaDBdatabase = request.form.get('MariaDBdatabase')
				MQTTbroker = request.form.get('MQTTbroker')
				MQTTport = request.form.get('MQTTport')
				MQTTuser = request.form.get('MQTTuser')
				MQTTpassword = request.form.get('MQTTpassword')
				countClimateSensors = request.form.get('countClimateSensors')

				print(countGasScales, countTanks, write2file, write2MariaDB, send2MQTT, MariaDBhost, MariaDBuser, MariaDBpasswd, MariaDBdatabase, MQTTbroker, MQTTport, MQTTuser, MQTTpassword, countClimateSensors)

				# Konvertierung der Daten in die richtigen Typen (z.B. in float)
				try:
					countGasScales = int(countGasScales) if countGasScales and 1 <= int(countGasScales) <= 2 else None
					countTanks = int(countTanks) if countTanks and 1 <= int(countTanks) <= 3 else None
					write2file = write2file if write2file else None
					write2MariaDB = write2MariaDB if write2MariaDB else None
					send2MQTT = send2MQTT if send2MQTT else None
					MariaDBhost = MariaDBhost if MariaDBhost else None
					MariaDBuser = MariaDBuser if MariaDBuser else None
					MariaDBpasswd = MariaDBpasswd if MariaDBpasswd else None
					MariaDBdatabase = MariaDBdatabase if MariaDBdatabase else None
					MQTTbroker = MQTTbroker if MQTTbroker else None
					MQTTport = int(MQTTport) if MQTTport else None
					MQTTuser = MQTTuser if MQTTuser else None
					MQTTpassword = MQTTpassword if MQTTpassword else None
					countClimateSensors = int(countClimateSensors) if countClimateSensors and 1 <= int(countClimateSensors) <= 2 else None
				except ValueError:
					# Behandlung von Konvertierungsfehlern
					flash('Fehler in Wertebehandlung')
					pass

				# Aufruf der Funktion zum Schreiben der Daten
				cplib.writeCaravanPiDefaults(countGasScales, countTanks, write2file, write2MariaDB, MariaDBhost, MariaDBuser, MariaDBpasswd, MariaDBdatabase, send2MQTT, MQTTbroker, MQTTport, MQTTuser, MQTTpassword, countClimateSensors)
				flash('Die Werte wurden erfolgreich gespeichert') 

			return redirect(url_for('config_caravanpi'))

		caravanpiDefaults_tuple = cplib.readCaravanPiDefaults()
		print(caravanpiDefaults_tuple)
		if caravanpiDefaults_tuple is None:
			caravanpiDefaults = {}
		else:
			# Umwandlung des Tupels in ein Dictionary
			caravanpiDefaults = {
				'countGasScales': caravanpiDefaults_tuple[0],
				'countTanks': caravanpiDefaults_tuple[1],
				'write2file': caravanpiDefaults_tuple[2],
				'write2MariaDB': caravanpiDefaults_tuple[3],
				'MariaDBhost': caravanpiDefaults_tuple[4],
				'MariaDBuser': caravanpiDefaults_tuple[5],
				'MariaDBpasswd': caravanpiDefaults_tuple[6],
				'MariaDBdatabase': caravanpiDefaults_tuple[7],
				'send2MQTT': caravanpiDefaults_tuple[8],
				'MQTTbroker': caravanpiDefaults_tuple[9],
				'MQTTport': caravanpiDefaults_tuple[10],
				'MQTTuser': caravanpiDefaults_tuple[11],
				'MQTTpassword': caravanpiDefaults_tuple[12],
				'countClimateSensors': caravanpiDefaults_tuple[13]
			}
		return render_template('config_caravanpi.html', caravanpiDefaults=caravanpiDefaults)

	@app.route('/config_dimension_caravan', methods=['GET', 'POST'])
	def config_dimension_caravan():

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('config_home'))  # Leitet um zur `/configs`-Route

			if 'submit' in request.form:
				# Daten aus dem Formular extrahieren
				lengthOverAll = request.form.get('lengthOverAll')
				widthOverAll = request.form.get('widthOverAll')
				lengthBody = request.form.get('lengthBody')

				print(lengthOverAll, widthOverAll, lengthBody)

				# Konvertierung der Daten in die richtigen Typen (z.B. in float)
				try:
					lengthOverAll = int(lengthOverAll) if lengthOverAll else None
					widthOverAll = int(widthOverAll) if widthOverAll else None
					lengthBody = int(lengthBody) if lengthBody else None
				except ValueError:
					# Behandlung von Konvertierungsfehlern
					flash('Fehler in Wertebehandlung')
					pass

				# Aufruf der Funktion zum Schreiben der Daten
				cplib.writeDimensions(lengthOverAll, widthOverAll, lengthBody)
				flash('Die Werte wurden erfolgreich gespeichert') 

			return redirect(url_for('config_dimension_caravan'))

		dimensions_tuple = cplib.readDimensions()
		print(dimensions_tuple)
		if dimensions_tuple is None:
			dimensions = {}
		else:
			# Umwandlung des Tupels in ein Dictionary
			dimensions = {
				'lengthOverAll': dimensions_tuple[0],
				'widthOverAll': dimensions_tuple[1],
				'lengthBody': dimensions_tuple[2]
			}
		return render_template('config_dimension_caravan.html', dimensions=dimensions)

	@app.route('/config_lagesensor', methods=['GET', 'POST'])
	def config_lagesensor():

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('config_home'))  # Leitet um zur `/configs`-Route

			if 'submit' in request.form:
				# Daten aus dem Formular extrahieren
				adjustX = request.form.get('adjustX')
				adjustY = request.form.get('adjustY')
				adjustZ = request.form.get('adjustZ')
				toleranceX = request.form.get('toleranceX')
				toleranceY = request.form.get('toleranceY')
				approximationX = request.form.get('approximationX')
				approximationY = request.form.get('approximationY')
				distRight = request.form.get('distRight')
				distFront = request.form.get('distFront')
				distAxis = request.form.get('distAxis')

				# Konvertierung der Daten in die richtigen Typen (z.B. in float)
				try:
					adjustX = float(adjustX) if adjustX else None
					adjustY = float(adjustY) if adjustY else None
					adjustZ = float(adjustZ) if adjustZ else None
					toleranceX = float(toleranceX) if toleranceX else None
					toleranceY = float(toleranceY) if toleranceY else None
					approximationX = float(approximationX) if approximationX else None
					approximationY = float(approximationY) if approximationY else None
					distRight = int(distRight) if distRight else None
					distFront = int(distFront) if distFront else None
					distAxis = int(distAxis) if distAxis else None

				except ValueError:
					# Behandlung von Konvertierungsfehlern
					flash('Fehler in Wertebehandlung')
					pass

				# Aufruf der Funktion zum Schreiben der Daten
				cplib.writeAdjustment(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis)

				flash('Die Werte wurden erfolgreich gespeichert') 

			return redirect(url_for('config_lagesensor'))

		lagesensor_tuple = cplib.readAdjustment()
		print(lagesensor_tuple)
		if lagesensor_tuple is None:
			lagesensor = {}
		else:
			# Umwandlung des Tupels in ein Dictionary
			lagesensor = {
				'adjustX': lagesensor_tuple[0],
				'adjustY': lagesensor_tuple[1],
				'adjustZ': lagesensor_tuple[2],
				'toleranceX': lagesensor_tuple[3],
				'toleranceY': lagesensor_tuple[4],
				'approximationX': lagesensor_tuple[5],
				'approximationY': lagesensor_tuple[6],
				'distRight': lagesensor_tuple[7],
				'distFront': lagesensor_tuple[8],
				'distAxis': lagesensor_tuple[9]
			}
		return render_template('config_lagesensor_default.html', lagesensor=lagesensor)

	@app.route('/config_gaswaage', methods=['GET', 'POST'])
	def config_gaswaage():

		# Ermitteln der Anzahl der Gasflaschenwaagen
		caravanpiDefaults_tuple = cplib.readCaravanPiDefaults()
		if caravanpiDefaults_tuple is None:
			anzWaagen = 1
		else:
			anzWaagen = caravanpiDefaults_tuple[0]

		print(f'Waagen: {anzWaagen}')

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('config_home'))  # Leitet um zur `/configs`-Route

			if 'submit' in request.form:
				for i in range(1, anzWaagen + 1):
					# Daten aus dem Formular extrahieren, spezifisch für jede Waage
					leergewicht = request.form.get(f'leergewicht_{i}')
					gasgewicht = request.form.get(f'gasgewicht_{i}')
					gpioHX711Dout = request.form.get(f'gpioHX711Dout_{i}')
					gpioHX711Sck = request.form.get(f'gpioHX711Sck_{i}')
					channelHX711 = request.form.get(f'channelHX711_{i}')
					refUnitHX711 = request.form.get(f'refUnitHX711_{i}')

					try:
						leergewicht = int(leergewicht) if leergewicht else None
						gasgewicht = int(gasgewicht) if gasgewicht else None
						gpioHX711Dout = int(gpioHX711Dout) if gpioHX711Dout and 1 <= int(gpioHX711Dout) <= 40 else None
						gpioHX711Sck = int(gpioHX711Sck) if gpioHX711Sck and 1 <= int(gpioHX711Sck) <= 40 else None
						channelHX711 = channelHX711 if channelHX711 in ['A', 'B'] else None
						refUnitHX711 = float(refUnitHX711) if refUnitHX711 else None
					except ValueError:
						# Behandlung von Konvertierungsfehlern
						flash(f'Fehler in Wertebehandlung für Waage {i}')
						continue

					# Aufruf der Funktion zum Schreiben der Daten, spezifisch für jede Waage
					cplib.writeGasScale(i, leergewicht, gasgewicht, gpioHX711Dout, gpioHX711Sck, channelHX711, refUnitHX711)
					flash(f'Die Werte für Waage {i} wurden erfolgreich gespeichert')

			return redirect(url_for('config_gaswaage'))

		gaswaage_tuples = []

		for i in range(1, anzWaagen + 1):
			gaswaage_tuple = cplib.readGasScale(i)
			print(i, gaswaage_tuple)

			if gaswaage_tuple is None:
				gaswaage_tuple = (1, 1, 1, 1, 'X', 0.0)

			# Umwandlung des Tupels in ein Dictionary und Hinzufügen zum Array
			gaswaage = {
				'leergewicht': gaswaage_tuple[0],
				'gasgewicht': gaswaage_tuple[1],
				'gpioHX711Dout': gaswaage_tuple[2],
				'gpioHX711Sck': gaswaage_tuple[3],
				'channelHX711': gaswaage_tuple[4],
				'refUnitHX711': gaswaage_tuple[5],
			}
			gaswaage_tuples.append(gaswaage)
	
		return render_template('config_gaswaage.html', gaswaagen=gaswaage_tuples, anzWaagen=anzWaagen)

	@app.route('/config_tanks', methods=['GET', 'POST'])
	def config_tanks():

		# Ermitteln der Anzahl der Gasflaschenwaagen
		caravanpiDefaults_tuple = cplib.readCaravanPiDefaults()
		if caravanpiDefaults_tuple is None:
			anzTanks = 1
		else:
			anzTanks = caravanpiDefaults_tuple[1]

		print(f'Tanks: {anzTanks}')

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('config_home'))  # Leitet um zur `/configs`-Route

			if 'submit' in request.form:
				for i in range(1, anzTanks + 1):
					# Daten aus dem Formular extrahieren, spezifisch für jede Waage
					level1 = request.form.get(f'level1_{i}')
					level2 = request.form.get(f'level2_{i}')
					level3 = request.form.get(f'level3_{i}')
					level4 = request.form.get(f'level4_{i}')

					try:
						level1 = float(level1) if level1 else None
						level2 = float(level2) if level2 else None
						level3 = float(level3) if level3 else None
						level4 = float(level4) if level4 else None
					except ValueError:
						# Behandlung von Konvertierungsfehlern
						flash(f'Fehler in Wertebehandlung für Tank {i}')
						continue

					# Aufruf der Funktion zum Schreiben der Daten, spezifisch für jede Waage
					cplib.writeFillLevels(i, level1, level2, level3, level4)
					flash(f'Die Werte für Tank {i} wurden erfolgreich gespeichert')

			return redirect(url_for('config_tanks'))

		tank_tuples = []

		for i in range(1, anzTanks + 1):
			tank_tuple = cplib.readFillLevels(i)
			print(i, tank_tuple)
			if tank_tuple is None:
				tank_tuple = (0.0, 0.0, 0.0, 0.0)

			# Umwandlung des Tupels in ein Dictionary und Hinzufügen zum Array
			tank = {
				'level1': tank_tuple[0],
				'level2': tank_tuple[1],
				'level3': tank_tuple[2],
				'level4': tank_tuple[3],
			}
			tank_tuples.append(tank)
	
		return render_template('config_tanks.html', tanks=tank_tuples, anzTanks=anzTanks)

	@app.route('/config_voltage', methods=['GET', 'POST'])
	def config_voltage():

		if request.method == 'POST':
			if 'cancel' in request.form:
				return redirect(url_for('config_home'))  # Leitet um zur `/configs`-Route

			if 'submit' in request.form:
				# Daten aus dem Formular extrahieren, spezifisch für jede Waage
				level1 = request.form.get('level1')
				level2 = request.form.get('level2')
				level3 = request.form.get('level3')

				try:
					level1 = float(level1) if level1 else None
					level2 = float(level2) if level2 else None
					level3 = float(level3) if level3 else None
				except ValueError:
					# Behandlung von Konvertierungsfehlern
					flash('Fehler in Wertebehandlung')
					pass

				# Aufruf der Funktion zum Schreiben der Daten, spezifisch für jede Waage
				cplib.writeVoltageLevels(level1, level2, level3)
				flash(f'Die Werte für die Batterie Level wurden erfolgreich gespeichert')

			return redirect(url_for('config_voltage'))

		batterie_tuple = cplib.readVoltageLevels()
		print(batterie_tuple)
		if batterie_tuple is None:
			batterie_tuple = (0.0, 0.0, 0.0)

		# Umwandlung des Tupels in ein Dictionary und Hinzufügen zum Array
		batterie = {
			'level1': batterie_tuple[0],
			'level2': batterie_tuple[1],
			'level3': batterie_tuple[2],
		}
	
		return render_template('config_voltage.html', batterie=batterie)


