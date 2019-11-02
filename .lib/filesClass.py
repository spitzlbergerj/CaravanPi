#!/usr/bin/python3
# coding=utf-8
# filesClass.py
#
# liest und schreibt Werte aus den und in die default files
#
#-------------------------------------------------------------------------------

import sys

class CaravanPiFiles:

	# -----------------------------------------------
	# global variables
	# -----------------------------------------------

	# files
	fileAdjustments = "/home/pi/CaravanPi/defaults/adjustmentPosition"
	fileDimensions = "/home/pi/CaravanPi/defaults/dimensionsCaravan"
	fileGasScale = "/home/pi/CaravanPi/defaults/gasScaleDefaults1"

	# ---------------------------------------------------------------------------------------------
	# adjustmentPosition
	#
	# content of file
	# 		adjustment X		X value, if caravan is in horizontal position
	#		adjustment Y		Y value, if caravan is in horizontal position
	#		adjustment Z		Z value, if caravan is in horizontal position
	#		tolerance X			deviation in X direction, which is still considered horizontal 
	#		tolerance Y			deviation in Y direction, which is still considered horizontal
	#		approximation X		at which deviation from the horizontal the LEDs should flash
	#		approximation Y		at which deviation from the horizontal the LEDs should flash
	#		distance right		distance of the sensor from the right side
	#		distance front		distance of the sensor from the front side
	# 		distance axis		Distance of the sensor from the axis in longitudinal direction
	# ----------------------------------------------------------------------------------------------

	def readAdjustment():
		try:
			file = open(CaravanPiFiles.fileAdjustments)
			
			strAdjustX = file.readline()
			strAdjustY = file.readline()
			strAdjustZ = file.readline()
			strtoleranceX = file.readline()
			strtoleranceY = file.readline()
			strApproximationX = file.readline()
			strApproximationY = file.readline()
			strDistRight = file.readline()
			strDistFront = file.readline()
			strDistAxis = file.readline()
			
			file.close()
			
			adjustX = float(strAdjustX)
			adjustY = float(strAdjustY)
			adjustZ = float(strAdjustZ)
			toleranceX = float(strtoleranceX)
			toleranceY = float(strtoleranceY)
			approximationX = float(strApproximationX)
			approximationY = float(strApproximationY)
			distRight = float(strDistRight)
			distFront = float(strDistFront)
			distAxis = float(strDistAxis)
			
			return(adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis)
		except:
			# Lesefehler
			print ("readAdjustment: The file ", CaravanPiFiles.fileAdjustments, " could not be read. unprocessed Error:", sys.exc_info()[0])
			return(0,0,0,0,0,0,0,0,0,0)

	def writeAdjustment(test, screen, adjustX, adjustY, adjustZ, toleranceX, toleranceY, approximationX, approximationY, distRight, distFront, distAxis):
		try:
			strAdjustX = '{:.6f}'.format(adjustX)
			strAdjustY = '{:.6f}'.format(adjustY)
			strAdjustZ = '{:.6f}'.format(adjustZ)
			strtoleranceX = '{:.6f}'.format(toleranceX)
			strtoleranceY = '{:.6f}'.format(toleranceY)
			strApproximationX = '{:.6f}'.format(approximationX)
			strApproximationY = '{:.6f}'.format(approximationY)
			strDistRight = '{:.0f}'.format(distRight)
			strDistFront = '{:.0f}'.format(distFront)
			strDistAxis = '{:.0f}'.format(distAxis)
			
			if test == 1:
				file = open(CaravanPiFiles.fileAdjustments+"_test", 'w')
			else:
				file = open(CaravanPiFiles.fileAdjustments, 'w')
		
			file.write(strAdjustX + "\n")
			file.write(strAdjustY + "\n")
			file.write(strAdjustZ + "\n")
			file.write(strtoleranceX + "\n")
			file.write(strtoleranceY + "\n")
			file.write(strApproximationX + "\n")
			file.write(strApproximationY + "\n")
			file.write(strDistRight + "\n")
			file.write(strDistFront + "\n")
			file.write(strDistAxis)
			
			file.close()
			
			if screen == 1:
				print("adjustX: ",strAdjustX)
				print("AdjustY: ",strAdjustY)
				print("AdjustZ: ",strAdjustZ)
				print("toleranceX: ",strtoleranceX)
				print("toleranceY: ",strtoleranceY)
				print("ApproximationX: ",strApproximationX)
				print("ApproximationY: ",strApproximationY)
				print("DistRight: ",strDistRight)
				print("DistFront: ",strDistFront)
				print("DistAxis: ",strDistAxis)

			
			return 0
		except:
			print("writeAdjustments: The file ", CaravanPiFiles.fileAdjustments, " could not be written - unprocessed Error:", sys.exc_info()[0])
			raise
			return -1

	# ---------------------------------------------------------------------------------------------
	# dimensions
	#
	# content of file
	# 		length over all		length of the caravan over all 
	#		width				width of the caravan over all
	#		lenght body			legth of the body of the caravan without drawbar
	# ----------------------------------------------------------------------------------------------

	def readDimensions():
		try:
			file = open(CaravanPiFiles.fileDimensions)
			
			strLengthOverAll = file.readline()
			strWidth = file.readline()
			strLengthBody = file.readline()
			
			file.close()
			
			lengthOverAll = float(strLengthOverAll)
			lengthBody = float(strLengthBody)
			width = float(strWidth)
			
			return(lengthOverAll, width, lengthBody)
		except:
			# Lesefehler
			print ("readDimensions: The file ", CaravanPiFiles.fileDimensions, " could not be read. unprocessed Error:", sys.exc_info()[0])
			return(0,0,0)

	def writeDimensions(test, screen, lengthOverAll, width, lengthBody):
		try:
			strLengthOverAll = '{:.0f}'.format(lengthOverAll)
			strWidth = '{:.0f}'.format(width)
			strLengthBody = '{:.0f}'.format(lengthBody)
			
			if test == 1:
				file = open(CaravanPiFiles.fileDimensions+"_test", 'w')
			else:
				file = open(CaravanPiFiles.fileDimensions, 'w')
				
			file.write(strLengthOverAll + "\n")
			file.write(strWidth + "\n")
			file.write(strLengthBody)
			
			file.close()
			
			if screen == 1:
				print("lengthOverAll: ",strLengthOverAll)
				print("width: ",strWidth)
				print("lengthBody: ",strLengthBody)
			
			return 0
		except:
			print("writeDimensions: The file ", CaravanPiFiles.fileDimensions, " could not be written - unprocessed Error:", sys.exc_info()[0])
			raise
			return -1


	# ---------------------------------------------------------------------------------------------
	# gas scale
	#
	# content of file
	# 		tare			value from gas scale without a gas cylinder 
	#		empty weight	weight of the empty gas cylinder
	#		full weight		weight of the full gas cylinder
	# ----------------------------------------------------------------------------------------------

	def readGasScale():
		try:
			file = open(CaravanPiFiles.fileGasScale)
			
			strTare = file.readline()
			strEmptyWeight = file.readline()
			strFullWeight = file.readline()
			
			file.close()
			
			tare = float(strTare)
			emptyWeight = float(strEmptyWeight)
			fullWeight = float(strFullWeight)
			
			return(tare, emptyWeight, fullWeight)
		except:
			# Lesefehler
			print ("readGasScale: The file ", CaravanPiFiles.fileGasScale, " could not be read. unprocessed Error:", sys.exc_info()[0])
			return(0,0,0)

	def writeGasScale(test, screen, tare, emptyWeight, fullWeight):
		try:
			strTare = '{:.0f}'.format(tare)
			strEmptyWeight = '{:.0f}'.format(emptyWeight)
			strFullWeight = '{:.0f}'.format(fullWeight)
			
			if test == 1:
				file = open(CaravanPiFiles.fileGasScale+"_test", 'w')
			else:
				file = open(CaravanPiFiles.fileGasScale, 'w')
				
			file.write(strTare + "\n")
			file.write(strEmptyWeight + "\n")
			file.write(strFullWeight)
			
			file.close()
			
			if screen == 1:
				print("tare: ",strTare)
				print("emptyWeight: ",strEmptyWeight)
				print("fullWeight: ",strFullWeight)
			
			return 0
		except:
			print("writeGasScale: The file ", CaravanPiFiles.fileGasScale, " could not be written - unprocessed Error:", sys.exc_info()[0])
			raise
			return -1


