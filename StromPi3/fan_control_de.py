from gpiozero import CPUTemperature, PWMLED
from time import sleep

led = PWMLED(2)	# PWM-Pin (GPIO 2)

startTemp = 55	# Temperatur bei der der Luefter an geht

pTemp = 4		# Proportionalanteil
iTemp = 0.2		# Integralanteil

fanSpeed = 0	# Lueftergeschwindigkeit
sum = 0			# Speichervariable fuer iAnteil


while True:		# Regelschleife
	cpu = CPUTemperature()		# Auslesen der aktuellen Temperaturwerte
	actTemp = cpu.temperature	# Aktuelle Temperatur als float-Variable

	diff = actTemp - startTemp
	sum = sum + diff
	pDiff = diff * pTemp
	iDiff = sum * iTemp
	fanSpeed = pDiff + iDiff + 35
 

	if fanSpeed > 100:
		fanSpeed = 100
	elif fanSpeed < 35:
		fanSpeed = 0
	
	if sum > 100:
		sum = 100
	elif sum < -100:
		sum = -100
	
	#print(str(actTemp) + "C, " + str(fanSpeed))
	
	led.value = fanSpeed / 100	# PWM Ausgabe

	sleep(1)