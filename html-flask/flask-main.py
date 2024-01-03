from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Startseite, von der aus die Checks gestartet werden
    return render_template('index-flask.html')  # Startseite mit einem Button oder automatischer Weiterleitung zu '/check_database'

@app.route('/check_database')
def check_database():
    # Database-Check durchführen
    result_database = True  # Beispiel: Ergebnis des Checks
    return render_template('check_database.html', result=result_database)

@app.route('/check_mqtt')
def check_mqtt():
    # MQTT-Check durchführen
    result_mqtt = True  # Beispiel: Ergebnis des Checks
    return render_template('check_mqtt.html', result=result_mqtt)

# Weitere Routen für weitere Checks

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
