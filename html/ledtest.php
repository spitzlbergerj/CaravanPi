<!DOCTYPE html>
<html>
	<head>
		<title>CaravanPi Konfiguration</title>
		
		<!-- zu verwendender Zeichensatz -->
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		
		<!-- Stylesheets -->
		<link rel="stylesheet" type="text/css" href="css/main.css">
		<link rel="stylesheet" type="text/css" href="css/custom.css">
		
		<!-- Favicon - Icon im Browser-Tab -->
		<link rel="icon" href="icons/CaravanPi.ico">
		
		<!-- Icons -->
		<link rel="apple-touch-icon" href="modules/MMM-Remote-Control/apple-touch-icon.png">
		<meta name="apple-mobile-web-app-title" content="MagicRemote">
		<meta name="apple-mobile-web-app-capable" content="yes">
		<meta name="mobile-web-app-capable" content="yes">
		<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
		
		<!-- Anweisung für Darstellung auf mobilen Devices (SmartPhone, Tablet) -->
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
		<!-- Anweisung für Goolge: Seite nicht übersetzen -->
		<meta name="google" content="notranslate" />
	</head>

	<body>
		<header class="header">CaravanPi Konfiguration - LEDs testen</header>
	
		<div class="container">
			<form class="caravanpi-form" action="ledtest.py" method="post">

				<!-- Leergewicht -->
				<div class="row">
					<div class="col-75">
						<label for="color">LED auf ff. Farbe schalten: </label>  
					</div>
					<div class="col-25">
					  <select name="color" size="1">
               <option value="2">blau</option>
              <option value="1">blau blinkend</option>
             <option selected value="0">rot</option>
              <option value="-1">grün blinkend</option>
              <option value="-2">grün</option>
            </select>
					</div>
				</div>
        
					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="LEDs für 60 Sekunden einschalten">
				</div>
			</form>
		</div>
	
		<div id="power-button" class="menu-element hidden button main-menu">
			<a class="text" href="index.html">zurück zum Konfigurationsmenü</a>
		</div>

	</body>
</html>
