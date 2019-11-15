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
		<header class="header">CaravanPi Konfiguration - Einstellungen Gas-Waage</header>
		
		<?php
			$gasScale = file("/home/pi/CaravanPi/defaults/gasScaleDefaults1");
			$GS_tare = floatval($gasScale[0]);
			$GS_empty = intval($gasScale[1]);
			$GS_full = intval($gasScale[2]);
			
			/*
			echo $GS_tare;
			echo $GS_empty;
			echo $GS_full;
			*/
		?>
	
		<div class="container">
			<form class="caravanpi-form" action="writeGasCylinderDefaults.py" method="post">

				<!-- Leergewicht -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-leer">Leergewicht Gasflasche(in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="leer" name="gewicht-leer" value="<?php echo $GS_empty; ?>" >
					</div>
				</div>

				<!-- Vollgewicht -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-voll">Gesamtgewicht volle Gasflasche (in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="voll" name="gewicht-voll" value="<?php echo $GS_full; ?>" >
					</div>
				</div>

					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Gewichte Gasflasche speichern">
				</div>
			</form>
		</div>
		
		<div class="container">
			<form class="caravanpi-form" action="writeScaleCalibration.py" method="post">

				<!-- Button autom. Kalibrierung-->
				<div class="row submit-button">
					<div>
						<p>
							<b>Autom. Kalibrierung der Gasflaschen Waage</b><br/>
							Bitte nehmen Sie die Gasflasche von der Waage. 
							Warten Sie dann ca. 2 Minuten bis die Waage ruhig steht. 
							Kalibrieren Sie die Waage dann durch Drücken auf den nachfolgenden Button.
						</p>
					</div>
					<input type="submit" id="submit" name="submit" value="Kalibrierung der leeren Gasflaschen-Waage starten">
				</div>

			</form>
		</div>
		
		<div class="container">
			<form class="caravanpi-form" action="writeGasScaleDefaults.py" method="post">

				<!-- Tara -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-leer">Tara der leeren Gasflaschen-Waage (in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="tara" name="tara" value="<?php echo $GS_tare; ?>" >
					</div>
				</div>

				<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Tara Gasflaschen-Waage speichern">
				</div>
			</form>
		</div>
	
		<div id="power-button" class="menu-element hidden button main-menu">
			<a class="text" href="index.html">zurück zum Konfigurationsmenü</a>
		</div>

	</body>
</html>