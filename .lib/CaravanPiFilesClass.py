#!/usr/bin/python3
# coding=utf-8
# filesClass.py
#
# liest und schreibt Werte aus den und in die default files
#
#Since this class is not initialized via __init__, the functions do not contain a fist parameter self
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
	# the gas cylinder number is appended to the file name specified here
	fileGasScale = "/home/pi/CaravanPi/defaults/gasScaleDefaults"
	# the tank number is appended to the file name specified here
	fileTanks = "/home/pi/CaravanPi/defaults/tankDefaults"
	fileTestColor = "/home/pi/CaravanPi/temp/testColor"

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
	#		length body			legth of the body of the caravan without drawbar
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

	def readGasScale(gasCylinderNumber):
		try:
			filename = CaravanPiFiles.fileGasScale + '{:.0f}'.format(gasCylinderNumber)
			file = open(filename)
			
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
			print ("readGasScale: The file ", filename, " could not be read. unprocessed Error:", sys.exc_info()[0])
			return(0,0,0)

	def writeGasScale(gasCylinderNumber, test, screen, tare, emptyWeight, fullWeight):
		try:
			strTare = '{:.0f}'.format(tare)
			strEmptyWeight = '{:.0f}'.format(emptyWeight)
			strFullWeight = '{:.0f}'.format(fullWeight)
			
			filename = CaravanPiFiles.fileGasScale + '{:.0f}'.format(gasCylinderNumber)
			if test == 1:
				file = open(filename+"_test", 'w')
			else:
				file = open(filename, 'w')
				
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
			print("writeGasScale: The file ", filename, " could not be written - unprocessed Error:", sys.exc_info()[0])
			raise
			return -1


	# ---------------------------------------------------------------------------------------------
	# filling levels
	#
	# level 1 is the smallest amount of water, level 4 is the largest amount of water in the tank
	#
	# content of file
	# 		liter level 1		amount of water in the tank at level 1 
	#		liter level 2		amount of water in the tank at level 2
	#		liter level 3		amount of water in the tank at level 3
	#		liter level 4		amount of water in the tank at level 4
	# ----------------------------------------------------------------------------------------------

	def readFillLevels(tankNumber):
		try:
			filename = CaravanPiFiles.fileTanks + '{:.0f}'.format(tankNumber)
			file = open(filename)
			
			strLevel1 = file.readline()
			strLevel2 = file.readline()
			strLevel3 = file.readline()
			strLevel4 = file.readline()
			
			file.close()
			
			level1 = float(strLevel1)
			level2 = float(strLevel2)
			level3 = float(strLevel3)
			level4 = float(strLevel4)
			
			return(level1, level2, level3, level4)
		except:
			# Lesefehler
			print ("readFillLevels: The file ", filename, " could not be read. unprocessed Error:", sys.exc_info()[0])
			return(0,0,0)

	def writeFillLevels(tankNumber, test, screen, level1, level2, level3, level4):
		try:
			strLevel1 = '{:.0f}'.format(level1)
			strLevel2 = '{:.0f}'.format(level2)
			strLevel3 = '{:.0f}'.format(level3)
			strLevel4 = '{:.0f}'.format(level4)
			
			filename = CaravanPiFiles.fileTanks + '{:.0f}'.format(tankNumber)
			if test == 1:
				file = open(filename+"_test", 'w')
			else:
				file = open(filename, 'w')
				
			file.write(strLevel1 + "\n")
			file.write(strLevel2 + "\n")
			file.write(strLevel3 + "\n")
			file.write(strLevel4)
			
			file.close()
			
			if screen == 1:
				print("Fill Level 1 liter: ",strLevel1)
				print("Fill Level 2 liter: ",strLevel2)
				print("Fill Level 3 liter: ",strLevel3)
				print("Fill Level 4 liter: ",strLevel4)
			
			return 0
		except:
			print("writeFillLevels: The file ", filename, " could not be written - unprocessed Error:", sys.exc_info()[0])
			raise
			return -1


	# ---------------------------------------------------------------------------------------------
	# testColor
	#
	# content of file
	# 		color			Color to show for testing LEDs 
	# ----------------------------------------------------------------------------------------------

	def readTestColor():
		try:
			file = open(CaravanPiFiles.fileTestColor)
			strColor = file.readline()
			file.close()
			
			return(strColor)
		except:
			# Lesefehler
			print ("readTestColor: The file ", CaravanPiFiles.fileTestColor, " could not be read. unprocessed Error:", sys.exc_info()[0])
			return("")

	def writeTestColor(test, screen, color):
		try:
			if color == "-2" or color == "-1" or color == "0" or color == "1" or color == "2": 
				if test == 1:
					file = open(CaravanPiFiles.fileTestColor+"_test", 'w')
				else:
					file = open(CaravanPiFiles.fileTestColor, 'w')
					
				file.write(color)
				file.close()
				
				if screen == 1:
					print("color: ",color)
				
				return 0
			else:
				return -2
		except:
			print("writeTestColor: The file ", CaravanPiFiles.fileTestColor, " could not be written - unprocessed Error:", sys.exc_info()[0])
			raise
			return -1


