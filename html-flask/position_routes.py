#
#
#

import sys
from flask import Flask, jsonify, render_template

sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

cplibfiles = CaravanPiFiles()

def get_position_latest_data():
	connection = cplibfiles.create_db_connection()
	if connection:
		table_name = "ausrichtung"
		columns = ['sensor_id', 'zeitstempel', 'differenz_hinten_links', 'differenz_hinten_rechts', 
				   'differenz_vorne_links', 'differenz_vorne_rechts', 'differenz_zentral_links', 
				   'differenz_zentral_rechts', 'differenz_deichsel']
		conditions = None
		order_by = "zeitstempel DESC LIMIT 1"

		latest_data = cplibfiles.read_from_table(connection, table_name, columns, conditions, order_by)
		connection.close()

		if latest_data:
			latest_data_dict = {
				'sensor_id': latest_data[0][0],
				'zeitstempel': latest_data[0][1],
				'differenz_hinten_links': latest_data[0][2],
				'differenz_hinten_rechts': latest_data[0][3],
				'differenz_vorne_links': latest_data[0][4],
				'differenz_vorne_rechts': latest_data[0][5],
				'differenz_zentral_links': latest_data[0][6],
				'differenz_zentral_rechts': latest_data[0][7],
				'differenz_deichsel': latest_data[0][8]
			}
			print('Fetched latest data:', latest_data_dict)  # Debugging-Ausgabe
			return latest_data_dict
		else:
			print('No data found.')  # Debugging-Ausgabe
			return None
	else:
		print("Keine Verbindung zur Datenbank.")  # Debugging-Ausgabe
		return None

def register_position_routes(app):

	@app.route('/position_latest_data')
	def position_latest_data():
		data = get_position_latest_data()
		if data:
			return jsonify(data)
		else:
			return jsonify({"error": "Keine Daten gefunden"}), 404

	@app.route('/actual_position')
	def actual_position():
		# Setze die Variablen für die Breite und Höhe des Bildes
		image_width = 240
		image_height = 640
		
		# Berechne die Breite und Höhe des Canvas, indem du auf jeder Seite 100px hinzufügst
		canvas_width = image_width + 200
		canvas_height = image_height + 40  # Höhe des Canvas um 40px erweitert

		border_width = "0px"  # Rahmenbreite als String

		return render_template('actual_position.html', 
							border_width=border_width, 
							image_width=image_width, 
							image_height=image_height,
							canvas_width=canvas_width,
							canvas_height=canvas_height)