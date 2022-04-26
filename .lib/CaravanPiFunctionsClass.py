#!/usr/bin/python3
# coding=utf-8
# CaravanPiClass.py
#
# prüft die Existenz eines Prozesses anhand dessen Namens
#
#Since this class is not initialized via __init__, the functions do not contain a fist parameter self
#
#-------------------------------------------------------------------------------
import sys
import os


class CaravanPiFunctions:

	# -----------------------------------------------
	# global variables
	# -----------------------------------------------


	# -----------------------------------------------
	# determine process number pid
	# -----------------------------------------------
	def process_running(name):
		for fso in os.listdir('/proc'):
			path = os.path.join('/proc', fso)
			if os.path.isdir(path):
				try:
					# das Verzeichnis eines Prozesses trägt die
					# numerische UID als Namen
					uid = int(fso)
					stream = open(os.path.join(path, 'cmdline'))
					cmdline = stream.readline()
					stream.close()
					if name in cmdline and "/bin/sh" not in cmdline:
						return uid
				except ValueError:
					# kein Prozessverzeichnis
					continue
		return 0
		
