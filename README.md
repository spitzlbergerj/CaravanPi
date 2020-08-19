# CaravanPi

## detailed Wiki
[deutsches Wiki](https://github.com/spitzlbergerj/CaravanPi/wiki/Installation-(german)/)

## Motivation

deutsch | english
----- | -----
System zur Messung und Anzeige verschiedener Sensorenwerte in Wohnwagen und Wohnmobilen, wie z.B. Klimawerte, Füllstände und Nivellierungsdaten. Zur Darstellung wird die Software <a href="https://magicmirror.builders/">Magic Mirror</a> verwendet. | System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. <a href="https://magicmirror.builders/">Magic Mirror</a> is used for presentation.
Derzeit sind die meisten Beschreibungen nur in english verfügbar. Ich arbeite daran, auch diese auf deutsch zur Verfügung zu stellen|Currently most of the descriptions are only available in English. I am working on making them available in german as well
<a href="https://github.com/spitzlbergerj/CaravanPi/wiki/Installation-(german)/">[direkt zur Aufbauanleitung](https://github.com/spitzlbergerj/CaravanPi/wiki/Installation-(german)/)|[directly to assembly instructions](https://github.com/spitzlbergerj/CaravanPi/wiki/Installation)

schematic drawing | MagicMirror display
----- | -----
![schema](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-320.jpg) | ![MagicMirror](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-MagicMirror-320.jpg)
[full size image](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi.jpg) | [full size image](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-MagicMirror.jpg) 

## Functionality
The CaravanPi has actually the following functionalities:
- Display of various data in a caravan or motorhome
  - Several climate sensors (e.g. inside and outside) with temperature, air pressure, air humidity
  - Multiple temperature sensors (e.g. freezer compartment, refrigerator)
  - Several filling levels (e.g. fresh water tank, waste water tank)
  - Filling level of a gas cylinder via weight determination
- Saving of all sensor data, so that course analyses can be made and represented
- Display of the current position of the caravan or motorhome using a display and LEDs at the corners of the caravan
- Calibration of the gas scale and the position sensor via keystroke
- Adaptation of all constants via a website
- Use of the display and also the configuration website via mobile devices
- Use other MagicMirror modules on the same display
- and more (to come) ....

## Caravan or motorhome?

The CaravanPi was designed and developed for use in a caravan. But the CaravanPi can also be used very well in motorhomes. Only the position determination and display with the LEDs must be adapted, since the display via LEDs makes no sense here. But the indication of the height differences at the corners will help here.

## Current development status (November 2019)

All sensors are now working and all values are read and stored cyclically. The levelling of the caravan by means of the LEDs works reliably. The display of all collected data on the MagicMirror also works.

I'm currently working on a website where all necessary configurations can be done.

I am also working on the "circuit board design" and on the sensible combination of all components in one housing.

## Components

The CaravanPi consists of the following components:
- Raspberry Pi
- software MagicMirror incl. new modules MMM-CaravanPi*
- apache webserver
- a lot of Python scripts
- a lot of hardware like 
  - Battery hat ([StromPi](https://strompi.joy-it.net/))
  - Load cell (Bosche)
  - various sensors
    - ADXL345 - 3-axis position sensor
    - hx711 - scale control
    - BME280 - climate sensor
    - ?? temperature sensor
    - MCP23017 GPIO extension
    - I2C extender
  - RGB LEDs
  - buzzer
  - and more

## Wiki

All components, the software, the assembly, the installation, the configuration and much more is explained in detail in the Wiki.

***Please read the [Wiki](https://github.com/spitzlbergerj/CaravanPi/wiki) before you start with your construction! There you'll find a lot of information to my idea behind CaravanPi and a lot of technical details.***
