# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

This project is currently under development!

## Motivation
In a caravan or motorhome there are a number of measuring points. In many cases the measured values are even displayed. As a rule, however, the different systems are independent of each other and supply separate displays or displays. With this project the different measuring points are to be evaluated via a system (Raspberry Pi) and displayed elegantly and configurably.

## Measuring points

The following data points are to be read in or created:
- Climate data (temperature, air pressure, humidity) inside and outside the caravan or motor home
- Temperature data in the refrigerator, preferably at different levels in the refrigerator
- Filling levels of fresh water and waste-holding tank
- Filling level of the gas cylinder via a scale

In addition, the horizontal position of the caravan or motor home should be determined and suitably displayed. A series of RGB LEDs at the corners of the caravan near the corner steadies will indicate in which direction the caravan or motor home needs to be cranked.

## Used components and sensors

The entire project is based on a **Raspberry Pi** with various sensors and corresponding software. Of course you can also use other components than the ones listed here. The brand names are only examples.

I used the following sensors for my setup:
- Single point load cell for weighing the gas cylinder ([Bosche H10A for 20 kg](https://www.bosche.eu/en/scale-components/load-cells/single-point-load-cell/single-point-load-cell-h10a)) 
- hx711 for evaluating the signals from the load cell ([ARCELI CJMCU-711 HX711](https://smile.amazon.de/gp/product/B07MY2PBY4/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
- ADXL345 Triple-Axis Accelerometer to determine the position of the caravan ([Adafruit ADXL345](https://smile.amazon.de/gp/product/B01BT4N9BC/ref))
- BME280 Barometric sensor for temperature, humidity and air pressure ([AZDelivery GY-BME280](https://smile.amazon.de/gp/product/B07FS95JXT/ref))
- DS18B20 Temperature sensor encapsulated in stainless steel [AZDelivery 1M Cable DS18B20](https://smile.amazon.de/gp/product/B075FYYLLV/ref)
- RGB LED to indicate the tilt angle 
- various buttons, resistors, diodes

## Software

Different Python scripts are used to read out the different sensors. They read out the values and write them to different files with current time stamps. Thus, on the one hand, the current value display is possible and on the other hand, history data can be graphically displayed in a later expansion step.

For the display of all information the grandiose software [MagicMirror](https://magicmirror.builders/) is used. This software, which runs on modules, can be designed very flexibly and also comes with a number of existing modules that can usefully supplement the display in the caravan and motorhome. For the display of the sensor data own MMM modules ([MMM-Caravan](https://github.com/spitzlbergerj/MMM-Caravan)) were developed.

## position determination and display for a caravan

The horizontal position of the caravan is determined by the 3 axis accelerometer. This shows the respective acceleration due to gravity for the axes x, y and z in m/s². Knowing that the maximum acceleration displayed per axis is approx. 10.3 m/s², these values can be used to determine the position angle for the longitudinal and transverse axes of the caravan.

Due to the dimensions of a medium to large caravan, the angles result in the respective corrections at the corners of the caravan, which are displayed there by means of RGB LEDs. In order to be able to perceive the displays inuitively, I have chosen the display color blue (= sky) for a too high position. A too low position of the corner is indicated as green (= meadow). A position close to the horizontal position is displayed as yellow (= attention as with traffic lights). The horizontal position is displayed as white. 

Due to the construction with a GPIO Extender, only the 8 mixed colors from the basic colors of the RGB LEDs can be used, since the Extender does not support PWM.

I have provided a total of 7 RGB LEDs on the caravan:

Four LEDs indicate the position at the four corners of the caravan. Two LEDs indicate the position of the caravan on the axis in transverse direction. And one LED indicates the position of the caravan on the drawbar in the longitudinal direction. 

The alignment of the caravan can be done as follows using these 7 LEDs:
- First, the caravan is brought into the horizontal position by lifting one of the tyres, e.g. with a [lifting cushion] (https://www.emukairlift.de/) in the transverse direction.
- The caravan is then brought into the horizontal position in both directions via the nose wheel in the longitudinal direction.
- Now the four corner supports can be tensioned. The LEDS at the four corners will help.

The position determination is designed for caravans. However, it can certainly also be adapted for campers with minor modifications.


## Installation Raspberry Pi incl. MagicMirror

The repository MagicMirror describes the installation of a Raspberry Pi incl. the MagicMirror base very well. Please use this [manual](https://github.com/MichMich/MagicMirror#raspberry-pi).

## Installation of other libraries used

### I2C Bus

### Sensor libraries

### Adafruit CricuitPython


## Hardware structure

### Construction of a scale for gas cylinders

### Extension GPIO Pins on the Raspberry Pi

### Extension of the I2C bus

### One-Wire devices like the temperature sensors


## Housing construction



 
