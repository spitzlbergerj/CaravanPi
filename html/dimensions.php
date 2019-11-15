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
		
		<!-- Anwesigung für Darstellung auf mobilen Devices (SmartPhone, Tablet) -->
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
		<!-- Anweisung für Goolge: Seite nicht übersetzen -->
		<meta name="google" content="notranslate" />
	</head>

	<body>
		<header class="header">CaravanPi Konfiguration - Dimensionen Cravan / Wohnmobil</header>
		
		<?php
			$dimensions = file("/home/pi/CaravanPi/defaults/dimensionsCaravan");
			$DI_lenght = intval($dimensions[0]);
			$DI_width = intval($dimensions[1]);
			$DI_length_body = intval($dimensions[2]);
			
			/*
			echo $DI_lenght;
			echo $DI_width;
			echo $DI_length_body;
			*/
		?>
	
		<div class="container">
			<form class="caravanpi-form" action="writeDimensionDefaults.py" method="post">

				<!-- Länge über alles -->
				<div class="row">
					<div class="col-75">
						<label for="laenge-alles">Länge über alles (in mm)</label>  
					</div>
					<div class="col-25">
						<input id="alaenge" name="laenge-alles" type="number" value="<?php echo $DI_lenght; ?>" >
					</div>
				</div>

				<!-- Breite über alles -->
				<div class="row">
					<div class="col-75">
						<label for="breite-alles">Breite über alles (in mm)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="abreite" name="breite-alles" value="<?php echo $DI_width; ?>" >
					</div>
				</div>

				<!-- Länge Aufbau -->
				<div class="row">
					<div class="col-75">
						<label for="laenge-aufbau">Länge Aufbau (in mm)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="ablaenge" name="laenge-aufbau" value="<?php echo $DI_length_body; ?>" >
					</div>
				</div>

					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Dimensionen speichern">
				</div>
			</form>
		</div>
		<div id="power-button" class="menu-element hidden button main-menu">
			<a class="text" href="index.html">zurück zum Konfigurationsmenü</a>
		</div>

	</body>
</html>