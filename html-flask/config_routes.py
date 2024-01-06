#
#
#

import sys
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
					lengthOverAll = float(lengthOverAll) if lengthOverAll else None
					widthOverAll = float(widthOverAll) if widthOverAll else None
					lengthBody = float(lengthBody) if lengthBody else None
				except ValueError:
					# Behandlung von Konvertierungsfehlern
					print (Fehler in Wertebehandlung)
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
