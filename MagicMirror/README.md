# Display CaravanPi values through Magic Mirror
CaravanPi uses the MagicMirror software to display all measurement results. For MagicMirror, corresponding CaravanPi modules have been developed, which are described in more detail below. 

The subdirectories config and css contain corresponding sample files which can be used to configure the MagicMirror. For this purpose, the corresponding passages from the individual files must be entered into the corresponding files in the Magic Mirror directory. 

## Magic Mirror modules
The following modules were created:

- [MMM-CaravanPiClimate](https://github.com/spitzlbergerj/MMM-CaravanPiTemperature)
- [MMM-CaravanPiGasWeight](https://github.com/spitzlbergerj/MMM-CaravanPiGasWeight)
- [MMM-CaravanPiPosition](https://github.com/spitzlbergerj/MMM-CaravanPiPosition)
- [MMM-CaravanPiTemperature](https://github.com/spitzlbergerj/MMM-CaravanPiTemperature)

### MMM-CaravanPiClimate
The MMM-CaravanPiClimate module displays climate values from the BME280 sensors. The corresponding Python scripts in CaravanPi can be found in the CaravanPi/climate/ directory.

<img src="https://raw.githubusercontent.com/spitzlbergerj/MMM-CaravanPiTemperature/master/img/MMM-CaravanPiTemperature-Screendump-Boxlines.jpg">

### MMM-CaravanPiGasWeight
The MMM-CaravanPiGasWeight module displays measured values from the gas cylinder scale. The corresponding Python scripts in CaravanPi can be found in the CaravanPi/gas-weight/ directory.

<img src="https://raw.githubusercontent.com/spitzlbergerj/MMM-CaravanPiGasWeight/master/img/MMM-CaravanPiGasWeight-Screendump-Boxlines.jpg">

### MMM-CaravanPiPosition
The MMM-CaravanPiPosition module displays measured values and calculation results based on them from the ADXL345 position sensor. The corresponding Python scripts in CaravanPi are located in the CaravanPi/position/ directory.

<img src="https://raw.githubusercontent.com/spitzlbergerj/MMM-CaravanPiPosition/master/img/MMM-CaravanPiPosition-Screendump.jpg">


### MMM-CaravanPiTemperature
The MMM-CaravanPiTemperature module displays measured values from the DS18B20 wired thermal sensors. The corresponding Python scripts in CaravanPi can be found in the CaravanPi/temperature/ directory.

<img src="https://raw.githubusercontent.com/spitzlbergerj/MMM-CaravanPiTemperature/master/img/MMM-CaravanPiTemperature-Screendump-Boxlines.jpg">
