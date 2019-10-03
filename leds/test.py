#!/usr/bin/python
from time import sleep

# -----------------------------------------------
# Sensoren libraries aus CaravanPi einbinden
# -----------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from mcp23017 import mcp23017,pin

mymcp=mcp23017()
mypin=pin(mymcp,"gpioa",0)
while True:
	mypin.enable()
	sleep(1)
	mypin.disable()
	sleep(1)