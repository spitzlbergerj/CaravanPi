#!/usr/bin/python
from mcp23017 import mcp23017,pin
from time import sleep
 
mymcp=mcp23017()
mypin=pin(mymcp,"gpioa",0)
while True:
	mypin.enable()
	sleep(1)
	mypin.disable()
	sleep(1)