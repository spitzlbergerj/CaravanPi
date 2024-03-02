import subprocess
import threading
import os
import glob
from datetime import datetime
from flask import Flask, Response, render_template

# importieren der weiteren Flask-Python-Files
from checks_routes import register_checks_routes
from config_routes import register_config_routes
from calibration_routes import register_calibration_routes
from test_routes import register_test_routes

app = Flask(__name__)
app.secret_key = 'd@o842FTz-_M2hbcU37N-ynvcwMNLe4tEoiZoH@4' # Zeichenfolge ist nicht wichtig, sollte kompliziert sein

# registieren der importierten Routen
register_checks_routes(app)
register_config_routes(app)
register_calibration_routes(app)
register_test_routes(app)

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
		files_info.append({
			'name': os.path.basename(file),
			'size': size,
			'mtime': mtime
		})
	files_info.sort(key=lambda x: x['name'].lower())
	return render_template('list_logs.html', files_info=files_info)

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

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
