#! /usr/bin/python3
# coding=utf-8
# volt2file.py
#
# liest den StromPi3 aus und schreibt die Volt in eine Datei
#
#-------------------------------------------------------------------------------

import time
import sys
import datetime
import RPi.GPIO as GPIO

import serial
import os

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from CaravanPiFilesClass import CaravanPiFiles

# -----------------------------------------------
# serial port handling
# -----------------------------------------------

wide_range_volt_min = 4.8
battery_volt_min = 0.5
mUSB_volt_min = 4.1

wideLevel100 = 12.4
wideLevel050 = 12.2
wideLevel025 = 12.0

breakS = 0.1
breakL = 0.5

serial_port = serial.Serial()

serial_port.baudrate = 38400
serial_port.port = '/dev/serial0'
serial_port.timeout = 1
serial_port.bytesize = 8
serial_port.stopbits = 1
serial_port.parity = serial.PARITY_NONE

if serial_port.isOpen(): serial_port.close()
serial_port.open()

# ------------------------------.----------------
# read serial port 
# -----------------------------------------------

def readSerialPort():
    serial_port.write(str.encode('quit'))
    time.sleep(breakS)
    serial_port.write(str.encode('\x0D'))
    time.sleep(breakL)

    serial_port.write(str.encode('status-rpi'))
    time.sleep(1)
    serial_port.write(str.encode('\x0D'))
    sp3_time = serial_port.readline(9999);
    sp3_date = serial_port.readline(9999);
    sp3_weekday = serial_port.readline(9999);
    sp3_modus = serial_port.readline(9999);
    sp3_alarm_enable = serial_port.readline(9999);
    sp3_alarm_mode = serial_port.readline(9999);
    sp3_alarm_hour = serial_port.readline(9999);
    sp3_alarm_min = serial_port.readline(9999);
    sp3_alarm_day = serial_port.readline(9999);
    sp3_alarm_month = serial_port.readline(9999);
    sp3_alarm_weekday = serial_port.readline(9999);
    sp3_alarmPoweroff = serial_port.readline(9999);
    sp3_alarm_hour_off = serial_port.readline(9999);
    sp3_alarm_min_off = serial_port.readline(9999);
    sp3_shutdown_enable = serial_port.readline(9999);
    sp3_shutdown_time = serial_port.readline(9999);
    sp3_warning_enable = serial_port.readline(9999);
    sp3_serialLessMode = serial_port.readline(9999);
    sp3_intervalAlarm = serial_port.readline(9999);
    sp3_intervalAlarmOnTime = serial_port.readline(9999);
    sp3_intervalAlarmOffTime = serial_port.readline(9999);
    sp3_batLevel_shutdown = serial_port.readline(9999);
    sp3_batLevel = serial_port.readline(9999);
    sp3_charging = serial_port.readline(9999);
    sp3_powerOnButton_enable = serial_port.readline(9999);
    sp3_powerOnButton_time = serial_port.readline(9999);
    sp3_powersave_enable = serial_port.readline(9999);
    sp3_poweroffMode = serial_port.readline(9999);
    sp3_poweroff_time_enable = serial_port.readline(9999);
    sp3_poweroff_time = serial_port.readline(9999);
    sp3_wakeupweekend_enable = serial_port.readline(9999);
    sp3_ADC_Wide = float(serial_port.readline(9999))/1000;
    sp3_ADC_BAT = float(serial_port.readline(9999))/1000;
    sp3_ADC_USB = float(serial_port.readline(9999))/1000;
    sp3_ADC_OUTPUT = float(serial_port.readline(9999))/1000;
    sp3_output_status = serial_port.readline(9999);
    sp3_powerfailure_counter = serial_port.readline(9999);
    sp3_firmwareVersion = serial_port.readline(9999);
    
    serial_port.close()
    
    return(sp3_ADC_Wide, sp3_ADC_USB, sp3_ADC_BAT, sp3_batLevel)

def batterylevel_converter(batterylevel):

    switcher = {
        1: '10%',
        2: '25%',
        3: '50%',
        4: '100%',
    }
    return switcher.get(batterylevel)

def widelevel_converter(wideVolt):
    global wideLevel025, wideLevel050, wideLevel100
    
    erg='0%'
    if (wideVolt >= wideLevel100):
        erg = '100%'
    elif (wideVolt >= wideLevel050):
        erg = '50%'
    elif (wideVolt >= wideLevel025):
        erg = '25%'

    return erg

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def write2file(wideVolt, usbVolt, batteryVolt, batteryLevel, ACVolt):
	try:
		dateiName = "/home/pi/CaravanPi/values/voltage"
		file = open(dateiName, 'a')
		str_from_time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		strWideVolt = '{:.3f}'.format(wideVolt)
		strWideLevel = widelevel_converter(wideVolt)
		strUsbVolt = '{:.3f}'.format(usbVolt)
		strBatteryVolt = '{:.3f}'.format(batteryVolt)
		strBatteryLevel = batterylevel_converter(int(batteryLevel))
		strACVolt = '{:.3f}'.format(ACVolt)
		file.write("\n"+ "voltage " + str_from_time_now + " " + strWideVolt + " " + strWideLevel + " " + strUsbVolt + " " + strBatteryVolt + " " + strBatteryLevel + " " + strACVolt)
		file.close()
		return 0
	except:
		# Schreibfehler
		print ("Die Datei konnte nicht geschrieben werden.")
		return -1

def main():
	# -------------------------
	# main 
	# -------------------------
	global wideLevel025, wideLevel050, wideLevel100

	GPIO.setwarnings(False)
	

	# -------------------------
	# read defaults
	# -------------------------
	(wideLevel025, wideLevel050, wideLevel100) = CaravanPiFiles.readVoltageLevels()


	(sp3Wide, sp3USB, sp3BAT, sp3BatLevel) = readSerialPort()

	try:
		if sp3Wide <= wide_range_volt_min:
			sp3Wide = 0

		if sp3USB <= mUSB_volt_min:
			sp3USB = 0

		if sp3BAT <= battery_volt_min:
			sp3BAT = 0

		write2file(sp3Wide, sp3USB, sp3BAT, sp3BatLevel, 0)

	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
	
	cleanAndExit()


if __name__ == "__main__":
	main()
