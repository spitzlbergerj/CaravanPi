#!/usr/bin/python3
# coding=utf-8
# writeConfig.py
#
# liest die Daten aus einem Webformular und generiert daraus die unterschiedlichen Config Files
#
#-------------------------------------------------------------------------------

import time, datetime
import signal
import sys
from time import sleep
import os

# CGI handling
import cgi
import cgitb


# -----------------------------------------------
# global variables
# -----------------------------------------------

# Correction of axis values
adjustX = 0
adjustY = 0
adjustZ = 0
# what is still considered horizontal
toleranceX = 0
toleranceY = 0
# When should the approach color be selected?
approximationX = 0
approximationY = 0

# files
fileAdjustments = "/home/pi/CaravanPi/defaults/adjustmentPosition"

# -------------------------
# 3-axis-sensor 
# -------------------------

def readAdjustment():
	global fileAdjustments
	
	try:
		dateiName = fileAdjustments
		file = open(dateiName)
		strAdjustX = file.readline()
		strAdjustY = file.readline()
		strAdjustZ = file.readline()
		strtoleranceX = file.readline()
		strtoleranceY = file.readline()
		strApproximationX = file.readline()
		strApproximationY = file.readline()
		file.close()
		adjustX = float(strAdjustX)
		adjustY = float(strAdjustY)
		adjustZ = float(strAdjustZ)
		toleranceX = float(strtoleranceX)
		toleranceY = float(strtoleranceY)
		approximationX = float(strApproximationX)
		approximationY = float(strApproximationY)
		return(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY)
	except:
		# Lesefehler
		print ("readAdjustment: The file could not be read.")
		return(0,0,0,0,0,0,0)

def writeAdjustments(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, shouldBePrinted):
	global fileAdjustments
	
	try:
		dateiName = fileAdjustments
		# test
		dateiName = fileAdjustments+"-test"

		file = open(dateiName, 'w')
		strAdjustX = '{:.6f}'.format(adjustX) + "\n"
		strAdjustY = '{:.6f}'.format(adjustY) + "\n"
		strAdjustZ = '{:.6f}'.format(adjustZ) + "\n"
		strtoleranceX = '{:.6f}'.format(toleranceX) + "\n"
		strtoleranceY = '{:.6f}'.format(toleranceY) + "\n"
		strApproximationX = '{:.6f}'.format(approximationX) + "\n"
		strApproximationY = '{:.6f}'.format(approximationY) + "\n"
		file.write(strAdjustX)
		file.write(strAdjustY)
		file.write(strAdjustZ)
		file.write(strtoleranceX)
		file.write(strtoleranceY)
		file.write(strApproximationX)
		file.write(strApproximationY)
		file.close()
		
		if (shouldBePrinted == 1):
			print("adjustX: "+strAdjustX)
			print("adjustY: "+strAdjustY)
			print("adjustZ: "+strAdjustZ)
			print("toleranceX: "+strtoleranceX)
			print("toleranceY: "+strtoleranceY)
			print("approximationX: "+strApproximationX)
			print("approximationY: "+strApproximationY)

		return 0
	except:
		print("writeAdjustments: The file could not be written - unprocessed Error:", sys.exc_info()[0])
		raise
		return -1

	
def main():
	# -------------------------
	# main 
	# -------------------------

	# lesen der Werte aus der HTML format
	cgitb.enable(display=0, logdir="/var/log/apache2")
	
	form = cgi.FieldStorage()
	
	gastaratxt =  form.getvalue('gastaratxt')
	tolx =  form.getvalue('tolx')
	toly =  form.getvalue('toly')
	approxx =  form.getvalue('approxx')
	approxy =  form.getvalue('approxy')
	

	# read defaults
	# The 3-axis sensor may not be installed exactly horizontally. The values to compensate for this installation difference are read from a file.
	# --> adjustX, adjustY, adjustZ
	# In addition, the LEDs should already indicate "horizontal" as soon as the deviation from the horizontal is within a tolerance.
	# --> approximationX, approximationY
	(adjustX_orig, adjustY_orig, adjustZ_orig, toleranceX_orig, toleranceY_orig, approximationX_orig, approximationY_orig) = readAdjustment()
	
	
	# writeAdjustments(x, y, z, toleranceX_orig, toleranceY_orig, approximationX_orig, approximationY_orig, shouldBePrinted)
	
	
	
	# Ergebnis Website schreiben
	print ("Content-Type: text/html; charset=utf-8\n\n")
	print ("<html>")
	print ("<body>")
	print ("<h1>Werte gelesen</h1>")
	print ("<p>")
	print (form)
	print ("</p>")
	if "name" not in form or "addr" not in form:
		print ("<H1>Error</H1>")
		print ("Please fill in the name and addr fields.")
	print ("<p>toleranceX: ")
	print (tolx)
	print ("</p>")
	print ("<p>toleranceY: ")
	print (toly)
	print ("</p>")
	print ("<p>approximationX: ")
	print (approxx)
	print ("</p>")
	print ("<p>approximationY: ")
	print (approxy)
	print ("</p>")
	print ("<p>gastaratxt: ")
	print (gastaratxt)
	print ("</p>")
	print ("</body>")
	print ("</html>")


if __name__ == "__main__":
	main()
