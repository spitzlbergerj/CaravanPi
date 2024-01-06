from flask import Flask, render_template

# importieren der weiteren Flask-Python-Files
from checks_routes import register_checks_routes
from config_routes import register_config_routes

app = Flask(__name__)
app.secret_key = 'd@o842FTz-_M2hbcU37N-ynvcwMNLe4tEoiZoH@4' # Zeichenfolge ist nicht wichtig, sollte kompliziert sein

# registieren der importierten Routen
register_checks_routes(app)
register_config_routes(app)

# definieren der zentralen Routen

@app.route('/')
def home():
    # Startseite, von der aus die Checks gestartet werden
    return render_template('index-flask.html')  # Startseite mit einem Button oder automatischer Weiterleitung zu '/check_database'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
