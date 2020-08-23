#!/usr/bin/python3
# coding=utf-8
# LEDtest.py
#
# steuert die LEDs an, die über MCP23017 angeschlossen sind
#
# Aufruf-Parameter
#
#-------------------------------------------------------------------------------

import smbus
import time

# I2C-Adresse des MCP23017
# initiate GPIO port expander
mcp1address = 0x20
mcp2address = 0x21

output = 0x00
input = 0xFF

banka = 0x00
bankb = 0x01

pinsAout = 0x14
pinsBout = 0x15

# Pins binär 76543210
mcp1ablau = 0x49
mcp1arot = 0x92
mcp1agruen = 0x24
mcp1bblau = 0x00
mcp1brot = 0x00
mcp1bgruen = 0x80

mcp2ablau = 0x49
mcp2arot = 0x92
mcp2agruen =0x24
mcp2bblau = 0x01
mcp2brot = 0x02
mcp2bgruen = 0x84

# Erzeugen einer I2C-Instanz und Öffnen des Busses
mcp23017 = smbus.SMBus(1)

# Konfiguration der MCP23017
mcp23017.write_byte_data(mcp1address,banka,output) # MCP23017 #1 Bank A Output 
mcp23017.write_byte_data(mcp1address,bankb,output) # MCP23017 #1 Bank B Output

mcp23017.write_byte_data(mcp2address,banka,output) # MCP23017 #2 Bank A Output
mcp23017.write_byte_data(mcp2address,bankb,output) # MCP23017 #2 Bank B Output

# alle aus
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
mcp23017.write_byte_data (mcp1address,pinsBout,0x00)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
mcp23017.write_byte_data (mcp2address,pinsBout,0x00)


# alle LEDs MCP #1 der Reihe nach jeweils blau, rot grün
print("der Reihe nach alle LED blau, dann rot, dann grün")
mcp23017.write_byte_data (mcp1address,pinsAout,0x01)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x02)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x04)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x08)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x10)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x20)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x40)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x80)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp1address,pinsBout,0x80)
time.sleep(1)

# alle aus
mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
mcp23017.write_byte_data (mcp1address,pinsBout,0x00)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
time.sleep(1)

# alle LEDs MCP #2 der Reihe nach jeweils blau, rot, grün
mcp23017.write_byte_data (mcp2address,pinsAout,0x01)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x02)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x04)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x08)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x10)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x20)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x40)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x80)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x80)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x01)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x02)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
time.sleep(1)
mcp23017.write_byte_data (mcp2address,pinsBout,0x04)
time.sleep(1)


# Blinkschleife
while True:
  # alle LEDs aus
  mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
  mcp23017.write_byte_data (mcp1address,pinsBout,0x00)
  mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
  mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
  time.sleep(1)
  # blaue LEDs an
  print("LED blau")
  mcp23017.write_byte_data (mcp1address,pinsAout,mcp1ablau)
  mcp23017.write_byte_data (mcp1address,pinsBout,mcp1bblau)
  mcp23017.write_byte_data (mcp2address,pinsAout,mcp2ablau)
  mcp23017.write_byte_data (mcp2address,pinsBout,mcp2bblau)
  time.sleep(2)
  
  # alle LEDs aus
  mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
  mcp23017.write_byte_data (mcp1address,pinsBout,0x00)
  mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
  mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
  time.sleep(1)
  # rote LEDs an
  print("LED rot")
  mcp23017.write_byte_data (mcp1address,pinsAout,mcp1arot)
  mcp23017.write_byte_data (mcp1address,pinsBout,mcp1brot)
  mcp23017.write_byte_data (mcp2address,pinsAout,mcp2arot)
  mcp23017.write_byte_data (mcp2address,pinsBout,mcp2brot)
  time.sleep(2)
    
  # alle LEDs aus
  mcp23017.write_byte_data (mcp1address,pinsAout,0x00)
  mcp23017.write_byte_data (mcp1address,pinsBout,0x00)
  mcp23017.write_byte_data (mcp2address,pinsAout,0x00)
  mcp23017.write_byte_data (mcp2address,pinsBout,0x00)
  time.sleep(1)
  # gruene LEDs an
  print("LED gruen")
  mcp23017.write_byte_data (mcp1address,pinsAout,mcp1agruen)
  mcp23017.write_byte_data (mcp1address,pinsBout,mcp1bgruen)
  mcp23017.write_byte_data (mcp2address,pinsAout,mcp2agruen)
  mcp23017.write_byte_data (mcp2address,pinsBout,mcp2bgruen)
  time.sleep(2)
