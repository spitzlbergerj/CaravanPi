#!/usr/bin/python
# coding=utf-8
# bms2file.py
#
# schreibt die aus dem Batteriemanagement gelesenen Werte ans Ende einer Datei 
# 
# Dieser Code basiert auf https://github.com/GemZ/LiontronBmsInfo
#
#-------------------------------------------------------------------------------

import sys
import argparse
import pexpect
import json


# -----------------------------------------------
# CaravanPi File/MARIADB/MQTT library einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

def connectBMS(args, gattchild):
	# Verbindung herstellen
	for attempt in range(10):
		try:
			if args.screen: 
				print("verbinde zum BMS (Versuch:", attempt+1, ")")
			gattchild.sendline("connect")
			gattchild.expect("Connection successful", timeout=1)
		except pexpect.TIMEOUT:
			if args.screen: 
				# print(gattchild.before)
				pass
			continue
		else: # keine exception, also erfolgreich
			if args.screen:
				print("BMS Verbindung hergestellt")
			return 1
	else: # alle 10 Schleifen mit except
		if args.screen: 
			print ("BMS Verbindung timeout!")
		gattchild.sendline("exit")
		return 0   


def readBMS(args, gattchild, startAddress, anzAntworten):
	# Request data until data is recieved or max attempt is reached
	# Voltage and other information
	for attempt in range(10):
		try:
			resp=b''
			if args.screen: 
				print("BMS Datenabfrage (Versuch:", attempt+1, ")")

			gattchild.sendline(f"char-write-req 0x0015 {startAddress}")
			gattchild.expect("Notification handle = 0x0011 value: ", timeout=1)
			gattchild.expect("\r\n", timeout=0)

			if args.screen: 
				print("BMS gelesen, Antwort 1: ", gattchild.before)

			resp+=gattchild.before

			if anzAntworten == 2:
				gattchild.expect("Notification handle = 0x0011 value: ", timeout=1)
				gattchild.expect("\r\n", timeout=0)

				if args.screen: 
					print("BMS gelesen, Antwort 2: ", gattchild.before)

				resp+=gattchild.before

		except pexpect.TIMEOUT:
			continue
		else:
			return resp
	else: 
		resp=b''
		if args.screen: 
			print ("BMS Anfrage timeout!")
			print(gattchild.before)
		return resp


def main():
	# ArgumentParser-Objekt erstellen
	parser = argparse.ArgumentParser(description='Lesen aller Temperatursensoren am 1-Wire-Bus')
	parser.add_argument('-s', '--screen', action='store_true',
						help='Ausgabe auf dem Bildschirm')
	parser.add_argument('-c', '--check', action='store_true', 
						help='Führt den Funktionstest aus')
	parser.add_argument("-d", "--device", 
					 help="Bluetooth Adresse der Batterie")

	# Argumente parsen
	args = parser.parse_args()

	# Adresse des BMS holen
	cplib = CaravanPiFiles()
	BMSaddress = cplib.readCaravanPiConfigItem("caravanpiDefaults/LiontronMACAddress")

	if args.device:
		print(f"Standardadresse {BMSaddress} wird ersetzt durch Parameterwert {args.device} ersetzt")
		BMSaddress = args.device

	# Run gatttool interactively.
	child = pexpect.spawn("gatttool -I -b {0}".format(BMSaddress))

	connectOK = connectBMS(args, child)

	print(f"Verbindung hergestellt? {connectOK}")


	if args.check:
		# nur Check, daher Abschluss hier
		if connectOK:
			print("erfolgreich")
			child.sendline("disconnect")
			child.sendline("exit")
			return 0
		else:
			print("Connect nicht möglich")
			return -1

	# Connect fehlgeschlagen, dann beenden
	if not connectOK:
		return -1
	
	resp1 = readBMS(args, child, "dda50300fffd77", 2)
	resp2 = readBMS(args, child, "dda50400fffc77", 1)
	resp3 = readBMS(args, child, "dda50500fffb77", 1)

	# Verbindung trennen
	if args.screen: 
		print("BMS Verbindung trennen")
	child.sendline("disconnect")
	child.sendline("exit")

	if args.screen: 
		print(resp1)
		print(resp2)
		print(resp3)

	# Entfernen des letzten Bytes, da Abschlusszeichen
	resp1 = resp1[:-1]
	resp2 = resp2[:-1]
	resp3 = resp3[:-1]

	# Umwandeln in ein Bytearray
	# dabei wandelt "decode" zunächst in Hex um
	response1=bytearray.fromhex(resp1.decode())
	response2=bytearray.fromhex(resp2.decode())
	response3=bytearray.fromhex(resp3.decode())

	if args.screen: 
		print(response1)
		print(response2)
		print(response3)

	rawdat={}
	if (response1.endswith(b'w')) and (response1.startswith(b'\xdd\x03')):
		response1=response1[4:]

		rawdat['Vmain']=int.from_bytes(response1[0:2], byteorder = 'big',signed=True)/100.0 #total voltage [V]
		rawdat['Imain']=int.from_bytes(response1[2:4], byteorder = 'big',signed=True)/100.0 #current [A]
		rawdat['RemainAh']=int.from_bytes(response1[4:6], byteorder = 'big',signed=True)/100.0 #remaining capacity [Ah]
		rawdat['NominalAh']=int.from_bytes(response1[6:8], byteorder = 'big',signed=True)/100.0 #nominal capacity [Ah]
		rawdat['NumberCycles']=int.from_bytes(response1[8:10], byteorder = 'big',signed=True) #number of cycles
		rawdat['ProtectState']=int.from_bytes(response1[16:18],byteorder = 'big',signed=False) #protection state
		rawdat['ProtectStateBin']=format(rawdat['ProtectState'], '016b') #protection state binary
		rawdat['SoC']=int.from_bytes(response1[19:20],byteorder = 'big',signed=False) #remaining capacity [%]
		rawdat['TempC1']=(int.from_bytes(response1[23:25],byteorder = 'big',signed=True)-2731)/10.0
		rawdat['TempC2']=(int.from_bytes(response1[25:27],byteorder = 'big',signed=True)-2731)/10.0

		rawdat['ProtectStateText']=""
		if (rawdat['ProtectStateBin'][0:13]) == '0000000000000':
			rawdat['ProtectStateText']="ok";
		
		if (rawdat['ProtectStateBin'][0]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, CellBlockOverVolt";
		if (rawdat['ProtectStateBin'][1]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, CellBlockUnderVol";
		if (rawdat['ProtectStateBin'][2]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, BatteryOverVol";
		if (rawdat['ProtectStateBin'][3]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, BatteryUnderVol";
		if (rawdat['ProtectStateBin'][4]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, ChargingOverTemp";
		if (rawdat['ProtectStateBin'][5]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, ChargingLowTemp";
		if (rawdat['ProtectStateBin'][6]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, DischargingOverTemp";
		if (rawdat['ProtectStateBin'][7]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, DischargingLowTemp";
		if (rawdat['ProtectStateBin'][8]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, ChargingOverCurrent";
		if (rawdat['ProtectStateBin'][9]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, DischargingOverCurrent"; 
		if (rawdat['ProtectStateBin'][10]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, ShortCircuit";
		if (rawdat['ProtectStateBin'][11]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, ForeEndICError";
		if (rawdat['ProtectStateBin'][12]) == "1":
			rawdat['ProtectStateText']=f"{rawdat['ProtectStateText']}, MOSSoftwareLockIn";

	if (response2.endswith(b'w')) and (response2.startswith(b'\xdd\x04')):
		response2=response2[4:-3]
		cellcount=len(response2)//2
		if args.screen: print ("Detected Cellcount: ",cellcount)
		for cell in range(cellcount):
			#print ("Cell:",cell+1,"from byte",cell*2,"to",cell*2+2)
			rawdat['Vcell'+str(cell+1)]=int.from_bytes(response2[cell*2:cell*2+2], byteorder = 'big',signed=True)/1000.0

	if (response3.endswith(b'w')) and (response3.startswith(b'\xdd\x05')):
		response3=response3[4:-3]
		rawdat['Name']=response3.decode("ASCII")

	# Print JSON
	print (json.dumps(rawdat, indent=1, sort_keys=False))

	# Sensorwerte verarbeiten
	cplib.handle_sensor_values(
		args.screen,								# Anzeige am Bildschirm?
		"batterymanagement",						# sensor_name = Datenbankname
		rawdat['Name'],								# sensor_id = Filename und Spalte in der Datenbank
		[
			"spannung_main",
			"spannung_zelle1",
			"spannung_zelle2",
			"spannung_zelle3",
			"spannung_zelle4",
			"kapazitaet",
			"temperatur",
			"ladezyklen",
			"strom",
			"status",
			"status_binary",
			"status_text",
			"SoC",
		],											# Liste Spaltennamen
		(
			rawdat['Vmain'],
			rawdat['Vcell1'],
			rawdat['Vcell2'],
			rawdat['Vcell3'],
			rawdat['Vcell4'],
			rawdat['RemainAh'],
			rawdat['TempC1'],
			rawdat['NumberCycles'],
			rawdat['Imain'],
			rawdat['ProtectState'],
			rawdat['ProtectStateBin'],
			rawdat['ProtectStateText'],
			rawdat['ProtectStateBin'],
		)											# Tupel Sensorwerte
	)    

	return 0          

if __name__=="__main__":
	result = main()
	sys.exit(result)