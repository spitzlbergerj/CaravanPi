![CaraavanPiLogo](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-Logo.png)  
# CaravanPi

- [Website](https://www.CaravanPi.de)
- 
- [deutsches Wiki](https://github.com/spitzlbergerj/CaravanPi/wiki/Home/)

- [Movitation](#motivation)
- [Functionality](#functionality)
- [Caravan or Motorhome?](#caravan-or-motorhome)
- [current development state](#current-development-state)
- [Components](#components)
- [Documentation (Wiki)](#wiki)
- [To Do](#to-do)


## Motivation

deutsch | english
----- | -----
System zur Messung und Anzeige verschiedener Sensorenwerte in Wohnwagen, Caravans und Wohnmobilen, wie z.B. Klimawerte, Füllstände von Tanks und Gasflaschen sowie Nivellierungsdaten. Zur Darstellung wird die Software <a href="https://magicmirror.builders/">Magic Mirror</a> verwendet. | System for measuring and displaying various values in caravans and motor homes, including climatic values, filling levels of tanks and gas cylinders and levelling data. <a href="https://magicmirror.builders/">Magic Mirror</a> is used for presentation.
Es existiert eine Schritt für Schritt Anleitung in deutsch. Englische Schnipsel sind bereits vorhanden und werden ausgebaut werden.|There is a step by step guide in German. English snippets are already available and will be extended.
[direkt zur Anleitung](https://github.com/spitzlbergerj/CaravanPi/wiki/Home/)|[directly to assembly instructions](https://github.com/spitzlbergerj/CaravanPi/wiki/Wiki-Home-english)

schematic drawing | MagicMirror display
----- | -----
![schema](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-320.jpg) | ![MagicMirror](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-MagicMirror-320.jpg)
[full size image](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi.jpg) | [full size image](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-MagicMirror.jpg) 

## Circuit design
deutsch | english
----- | -----
Nun ist auch das Platinen Design abgeschlossen. Die Platine wurde ausführlich getestet und funktioniert einwandfrei | For the CaravanPi, there is now a circuit board design that can be produced by appropriate service providers, also pre-assembled. 
front | back
![front](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/doku/CaravanPi-Platine-Vorderseite.png) | ![front](https://github.com/spitzlbergerj/CaravanPi/raw/master/images/doku/CaravanPi-Platine-Rückseite.png) 
Alle zum Bestellen der Platine benötigten Angaben und Dateien befinden sich im Verzeichnis circuit-board | All information and files needed to order the board are located in the directory circuit-board
Die Platine ist aus SMD Bauteilen aufgebaut. Als Klemmen werden WAGO Klemmen verwendet. | The board is built from SMD components. WAGO PCB terminal blocks are used as cable clamps.


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

## Caravan or motorhome

The CaravanPi was designed and developed for use in a caravan. But the CaravanPi can also be used very well in motorhomes. Only the position determination and display with the LEDs must be adapted, since the display via LEDs makes no sense here. But the indication of the height differences at the corners will help also in motorhomes.

## Current development state

(Oktober 2020)
All sensors (temperature, climate, 3-axis, load cell) are now working and all values are read and stored cyclically. The levelling of the caravan by means of the LEDs works reliably. The display of all collected data on the MagicMirror also works. And there is now a German Wiki with a step-by-step guide, which was tested in parallel by an interested person. Appropriate circuit diagrams exist for all components of the caravanPi, which facilitate reproduction and are useful for troubleshooting. 

A website where all necessary configurations can be done is also working.

With a friend I am also working on the "circuit board design" and on the sensible combination of all components in one housing.

The CaravanPi including all sensors is installed in my Tabbert caravan and tested there. Everything works perfectly. The next step is the circuit board design, so that the creation of the necessary circuit board is considerably simplified.

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
    - DS18B20 temperature sensor
    - MCP23017 GPIO extension
    - I2C extender
  - RGB LEDs
  - buzzer
  - and more

## Wiki

All components, the software, the assembly, the installation, the configuration and much more is explained in detail in the Wiki.

***Please read the [Wiki](https://github.com/spitzlbergerj/CaravanPi/wiki) before you start with your construction! There you'll find a lot of information to my idea behind CaravanPi and a lot of technical details.***

## To Do
- ~~development of a circuit board,~~
- ~~circuit board, which can then be purchased, etched or ordered from a online circuid board shop~~
- ~~python and MMM-Module for filling level in fresh water tank~~
- python and MMM-Module for filling level in waste tank
- adopt climate section for the BME 680 with air qualitiy value
- ~~do all the documentation~~
