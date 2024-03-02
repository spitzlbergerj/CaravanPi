import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw', 'v'))

print('[press ctrl+c to end the script]') 

try: # Main program loop
	while True:  
		print("0: {:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
		print("1: {:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
		print("2: {:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
		print("3: {:>5}\t{:>5.3f}".format(chan3.value, chan2.voltage))

		print("---")
		
		time.sleep(0.5)
		
except KeyboardInterrupt:
	# Savenging work after the end of the program
	print('Script end!')