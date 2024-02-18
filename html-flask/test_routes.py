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



def register_test_routes(app):

	@app.route('/tests', methods=['GET', 'POST'])
	def tests_home():
		return render_template('tests.html')

