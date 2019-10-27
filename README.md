# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. [MagicMirror](https://magicmirror.builders/) is used for presentation.

<table width="100%" border="0">
	<tbody>
		<tr>
   <td>
    <img src="https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-320.jpg">
   </td>
			<td>
    <img src="https://github.com/spitzlbergerj/CaravanPi/raw/master/images/CaravanPi-MagicMirror-320.jpg">
   </td>
		</tr>
	</tbody>
</table>

I have developed the CaravanPi for use in a caravan. But the CaravanPi can also be used very well in motorhomes. Only the position determination and display with the LEDs must be adapted, since the display via LEDs makes no sense here. But the indication of the height differences at the corners will help here. I plan these adjustments in a later expansion step.

***Please read the [Wiki](https://github.com/spitzlbergerj/CaravanPi/wiki) before you start with your construction! There you'll find a lot of information to my idea behind CaravanPi and a lot of technical details.***

## Software

Different Python scripts are used to read out the different sensors. These scripts write the values after reading to different files with current time stamps. Thus, on the one hand, the current value display is possible and on the other hand, history data can be graphically displayed in a later expansion step.

To display all information the grandiose software [MagicMirror](https://magicmirror.builders/) is used. This software, which runs on modules, can be designed very flexibly and also comes with a number of existing modules that can usefully supplement the display in the caravan and motorhome. For the display of the sensor data own MMM modules ([MMM-CaravanPiPosition](https://github.com/spitzlbergerj/MMM-CaravanPiPosition), [MMM-CaravanPiClimate](https://github.com/spitzlbergerj/MMM-CaravanPiClimate), [MMM-CaravanPiTemperature](https://github.com/spitzlbergerj/MMM-CaravanPiTemperature), [MMM-CaravanPiGasWeight](https://github.com/spitzlbergerj/MMM-CaravanPiGasWeight)) were developed.

In order for the displays and scripts to work, various default settings such as the length and width of the caravan, the tare of the gas scale, the empty weight of the gas cylinder and the distance between the 3-axis sensor and the outer walls are necessary. These data are permanently stored in files. These values can be entered via a configuration website. 

In addition to this website for the default values, the MagicMirror display can be set via another configuration website.

## Installation Raspberry Pi incl. MagicMirror

First of all instll the raspberry pi including the display software MagicMirror. The repository MagicMirror describes the installation of a Raspberry Pi incl. the MagicMirror base very well. Please use this [manual](https://github.com/MichMich/MagicMirror#raspberry-pi).

## Installation of this module

`git clone https://github.com/spitzlbergerj/CaravanPi`

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



## Installation

## links


 
