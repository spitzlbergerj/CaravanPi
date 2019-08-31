# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

# Climate sensors

I use the Bosch BME280 to determine the temperature, the air pressure and the pleasure humidity. The sensor determines these data reliably in the smallest space. I use two of these sensors. One monitors the interior of the caravan, one monitors the exterior. I am still looking for a suitable location for the sensor.


## I2C Bus Extender
The BME280 I use can be addressed via the I2C bus. Since I want to place the two sensors optimally in and on the caravan (e.g. far away from heat sources like Raspberry or refrigerator), I2C bus extenders are necessary. As cable I use a Cat6 cable.
