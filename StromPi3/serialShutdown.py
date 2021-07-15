#!/usr/bin/env python
import serial
import os
import time
import sys
##############################################################################
#Hier muss der wait_for_shutdowntimer eingestellt werden - dieser wartet mit dem Herunterfahren des Raspberry Pi,
# fuer den Fall dass die primaere Stromquelle wiederhergesttelt werden sollte
# Dieser Timer muss kleiner sein, als der im StromPi3 eingestellte shutdown-timer, damit sicher heruntergefahren wird.

#Here you have to set the wait_for_shutdowntimer in seconds - it waits with the shutdown of the Raspberry pi,
# in the case the primary voltage source turns back on.
# This timer have to be set lower than the configured shutdown-timer in the StromPi3 to make a safe shutdown.

##############################################################################
wait_for_shutdowntimer = 10;
##############################################################################

t=0 #Temporary time-variable

os.system('sudo date')
print ('StromPi - serial shutdown Skript started')
print ('-----------------------------------------')
print ('wait to bring up all things')
sys.stdout.flush()

time.sleep(90)

os.system('sudo date')
print ('start serial ...')
sys.stdout.flush()

ser = serial.Serial(
 port='/dev/serial0',
 baudrate = 38400,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)
counter=0

os.system('sudo date')
print ('enter loop')
sys.stdout.flush()

while 1:
 x=ser.readline()
 y = x.decode(encoding='UTF-8',errors='strict')
 if y==('xxxShutdownRaspberryPixxx\n'):
  os.system('sudo date')
  print ("PowerFail - Raspberry Pi Shutdown")
  sys.stdout.flush()
  t= wait_for_shutdowntimer + 1
 elif y==('xxx--StromPiPowerBack--xxx\n'):
  os.system('sudo date')
  print ("PowerBack - Raspberry Pi Shutdown aborted")
  sys.stdout.flush()
  t=0
 if t>0:
  t-=1
  if t == 1:
   os.system('sudo date')
   print ("shutdown Raspberry Pi in 1 second")
   sys.stdout.flush()
   time.sleep(1)
   os.system("sudo shutdown -h now")