# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

## .lib

libraries for the used sensors

hx711py from https://github.com/tatobari/hx711py
I have adapted this library so that it is now python3 compatible. For this I used 2to3.

mcp23017.py von http://www.gsurf.de/mcp23017-i2c-mit-python-steuern/

ledClass.py zur Ansteuerung der LEDs über Threads

filesCaravan.py contains functions for reading and writing default files
