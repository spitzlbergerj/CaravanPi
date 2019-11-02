# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

## Shutdown Pi through a tactile switch

To switch off the Raspberry Pi I use a tactile swith and the script published at heise.de. By the skillful choice of the GPIO pin 5 the button can switch the Pi on again.

(https://www.heise.de/ct/hotline/Ein-Ausschalter-fuer-Raspberry-Pi-und-Raspi-Zero-3892620.html?wt_mc=print.ct.2017.25.150#zsdb-article-links)

Since GPIO pin 5 is also needed for the I2C bus, an additional transistor is necessary.

