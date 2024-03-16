import subprocess
import threading
import os
import glob
import sys
from datetime import datetime
from flask import Flask, Response, render_template, redirect, url_for, flash

# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles
from CaravanPiFunctionsClass import CaravanPiFunctions

cplib = CaravanPiFiles()


# importieren der weiteren Flask-Python-Files
from checks_routes import register_checks_routes
from config_routes import register_config_routes
from calibration_routes import register_calibration_routes
from test_routes import register_test_routes
from actors_routes import register_actors_routes

app = Flask(__name__)
app.secret_key = 'd@o842FTz-_M2hbcU37N-ynvcwMNLe4tEoiZoH@4' # Zeichenfolge ist nicht wichtig, sollte kompliziert sein

# registieren der importierten Routen
register_checks_routes(app)
register_config_routes(app)
register_calibration_routes(app)
register_test_routes(app)
register_actors_routes(app)

# Unterstützungsfunktionen

def get_i2cdetect_output():
	try:
		# Führen Sie den Befehl aus und erfassen Sie die Ausgabe
		result = subprocess.run(['/usr/sbin/i2cdetect', '-y', '1'], capture_output=True, text=True, check=True)
		output = result.stdout
	except subprocess.CalledProcessError as e:
		# Falls ein Fehler auftritt, geben Sie eine entsprechende Nachricht zurück
		output = f"Ein Fehler ist aufgetreten: {e}"
	return output

# definieren der zentralen Routen

@app.route('/')
def home():
	# Startseite, von der aus die Checks gestartet werden
	return render_template('index-flask.html')  # Startseite mit einem Button oder automatischer Weiterleitung zu '/check_database'

@app.route('/show_config')
def show_config():
	config_path = '/home/pi/CaravanPi/defaults/caravanpiConfig.xml'
	if os.path.exists(config_path):
		with open(config_path, 'r') as file:
			xml_content = file.read()
		return Response(xml_content, mimetype='text/xml')
	else:
		return "Die Konfigurationsdatei konnte nicht gefunden werden.", 404

@app.route('/list_logs')
def list_logs():
	# Pfad zum Verzeichnis, das die .log Dateien enthält
	logs_directory = '/home/pi/CaravanPi/.log'
	# Erstellen der Liste aller .log Dateien
	log_files = glob.glob(os.path.join(logs_directory, '*.log'))
	# Liste für die Dateiinformationen
	files_info = []
	for file in log_files:
		# Dateigröße in Bytes
		size = os.path.getsize(file)
		# Letzte Änderung als Datum
		mtime = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
		# Letzten 15 Zeilen der Datei
		with open(file, 'r', encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()[-30:]
		files_info.append({
			'name': os.path.basename(file),
			'size': size,
			'mtime': mtime,
			'last_lines': lines
		})
	files_info.sort(key=lambda x: x['name'].lower())
	return render_template('list_logs.html', files_info=files_info)

@app.route('/i2cdetect')
def i2cdetect():
	# Rufen Sie die Funktion auf, um die i2cdetect-Ausgabe zu erhalten
	i2cdetect_output = get_i2cdetect_output()
	# Senden Sie die Ausgabe als Response zurück, hier als einfacher Text
	return Response(i2cdetect_output, mimetype='text/plain')

@app.route('/reboot')
def reboot_system():
	# Startet den Reboot in einem separaten Thread nach einer Verzögerung
	threading.Timer(5, lambda: subprocess.run(['sudo', 'reboot'])).start()
	# Rendert sofort eine Seite, die dem Benutzer mitteilt, dass ein Neustart im Gange ist
	return render_template('reboot_shutdown.html')

@app.route('/shutdown')
def shutdown_system():
	# Startet den Reboot in einem separaten Thread nach einer Verzögerung
	threading.Timer(5, lambda: subprocess.run(['sudo', 'shutdown', '-h', 'now'])).start()
	# Rendert sofort eine Seite, die dem Benutzer mitteilt, dass ein Neustart im Gange ist
	return render_template('reboot_shutdown.html')

@app.route('/aktor/alarm_230v_aus')
def aktor_alarm_230v_aus():
	print("Alarm 230v in Config ausschalten")
	cplib.writeCaravanPiConfigItem("caravanpiDefaults/v230CheckAlarmActive", 0)
	flash('Alarm wurde ausgeschaltet') 
	return redirect(url_for('home'))

@app.route('/aktor/alarm_12v_bord_aus')
def aktor_alarm_12v_bord_aus():
	print("Alarm 12v bord in Config ausschalten")
	cplib.writeCaravanPiConfigItem("caravanpiDefaults/v12BatteryCheckAlarmActive", 0)
	flash('Alarm wurde ausgeschaltet') 
	return redirect(url_for('home'))

@app.route('/aktor/alarm_12v_car_aus')
def aktor_alarm_12v_car_aus():
	print("Alarm 12v car in Config ausschalten")
	cplib.writeCaravanPiConfigItem("caravanpiDefaults/v12CarCheckAlarmActive", 0)
	flash('Alarm wurde ausgeschaltet') 
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
