# BottleFramework

Das sog. bottleFramework stellt einen Webservice zur Verfügung, der es erlaubt, durch aufrufen bestimmter Webadressen Funktionen auszulösen.

Im CaravanPi wird das BottleFramework genutzt um Konfigurationsarbeiten anzustoßen

## Definierte Websites

### http://<IP des CaravanPi>:8089/ConfigSite/positionCalibration

		cmdstring = 'python3 /home/pi/CaravanPi/position/setupPositionDefaults.py';

        
### http://<IP des CaravanPi>:8089/ConfigSite/gasScaleCalibration":
		cmdstring = 'python3 /home/pi/CaravanPi/gas-weight/setupGasscaleDefaults.py';

### http://<IP des CaravanPi>:8089/ConfigSite/LEDtest":
		pid = CaravanPiFunctions.process_running("position2file.py")

### http://<IP des CaravanPi>:8089/ConfigSite/MMtest":

Anzeige einer Testnachricht auf dem MagicMirror
