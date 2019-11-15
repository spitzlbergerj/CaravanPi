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
		<header class="header">CaravanPi Konfiguration - Einstellungen Lage-Sensor</header>
	
		<?php
			$adjustmentPosition = file("/home/pi/CaravanPi/defaults/adjustmentPosition");
			$AD_adjustX = floatval($adjustmentPosition[0]);
			$AD_adjustY = floatval($adjustmentPosition[1]);
			$AD_adjustZ = floatval($adjustmentPosition[2]);
			$AD_tolX = floatval($adjustmentPosition[3]);
			$AD_tolY = floatval($adjustmentPosition[4]);
			$AD_approxX = floatval($adjustmentPosition[5]);
			$AD_approxY = floatval($adjustmentPosition[6]);
			$AD_distR = intval($adjustmentPosition[7]);
			$AD_distF = intval($adjustmentPosition[8]);
			$AD_distA = intval($adjustmentPosition[9]);
			/* 
			echo $AD_adjustX;
			echo $AD_adjustY;
			echo $AD_adjustZ;
			echo $AD_tolX;
			echo $AD_tolY;
			echo $AD_approxX;
			echo $AD_approxY;
			echo $AD_distR;
			echo $AD_distF;
			echo $AD_distA;	
			*/
		?>
	
	
		<div class="container">
			<form class="caravanpi-form" action="writePositionDefaults.py" method="post">

				<!-- Toleranz X -->
				<div class="row">
					<div class="col-75">
						<label for="tolX">Toleranz Längsrichtung(in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="tolX" name="tolX" value="<?php echo $AD_tolX; ?>" step="0,05" min="-10" max="10">
					</div>
				</div>
				
				<!-- Toleranz Y -->
				<div class="row">
					<div class="col-75">
						<label for="tolY">Toleranz Querrichtung (in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="tolY" name="tolY" value="<?php echo $AD_tolY; ?>" step="0,05" min="-10" max="10">
					</div>
				</div>

				<!-- Approximation X -->
				<div class="row">
					<div class="col-75">
						<label for="approxX">Toleranz Längsrichtung(in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="approxX" name="approxX" value="<?php echo $AD_approxX; ?>" step="0,05" min="-10" max="10">
					</div>
				</div>
				
				<!-- Approximation Y -->
				<div class="row">
					<div class="col-75">
						<label for="approxY">Toleranz Querrichtung (in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="approxY" name="approxY" value="<?php echo $AD_approxY; ?>" step="0,05">
					</div>
				</div>

				<div class="respimglage">
					<img src="img/CaravanPiLagesensor.png" alt="Lagesensor CaravanPi" class="responsive" width="600" height="255">
				</div>

				<!-- Abstände LageSensor -->
				<div class="row">
					<div class="col-75">
						<label for="dist-front">Abstand Lagesensor zur Aufbaufront (in mm)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="distF" name="dist-front" value="<?php echo $AD_distF; ?>" >
					</div>
				</div>
				<div class="row">
					<div class="col-75">
						<label for="dist-right">Abstand Lagesensor zur rechten Aufbauseite (in mm)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="distR" name="dist-right" value="<?php echo $AD_distR; ?>" >
					</div>
				</div>
				<div class="row">
					<div class="col-75">
						<label for="dist-axis">Abstand Lagesensor zur Achse (in mm)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="distA" name="dist-axis" value="<?php echo $AD_distA; ?>" >
					</div>
				</div>

					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Einstellungen Lagesensor speichern">
				</div>
			</form>
		</div>
		
		<div class="container">
			<form class="caravanpi-form" action="writePositionCalibration.py" method="post">

				<!-- Button autom. Kalibrierung-->
				<div class="row submit-button">
					<div>
						<p>
							<b>Autom. Kalibrierung des Lagesensors</b><br/>
							Bitte richten Sie den Caravan bzw. das Wohnmobil möglichst exakt waagrecht aus.
							Im Caravan bzw. im Wohnmobil sollten sich keine Personen aufhalten. Geräte, die Vibrationen verursachen können,
							sollten vollständig ausgeschaltet sein. <br/>
							Lassen Sie den Wagen dann einige Minuten ruhig und unverändert stehen, bis alle Schwingungen abgeklungen sind.
							Starten Sie dann die Kalibrierung. Diese wird weitere zwei Minuten warten, bevor die Sensordaten ausgelesen werden. 
							Ein Summer wird die Kalibrierung signalisieren.
						</p>
					</div>
					<input type="submit" id="submit" name="submit" value="Kalibrierung des Lage-Sensors starten">
				</div>

			</form>
		</div>
		
		<div class="container">
			<form class="caravanpi-form" action="writePositionManuDefaults.py" method="post">

				<!-- X -->
				<div class="row">
					<div class="col-75">
						<label for="adjustX">Ruhewert X Längsrichtung (in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="adjustX" name="adjustX" value="<?php echo $AD_adjustX; ?>" step="0,000001" min="-10" max="10">
					</div>
				</div>
				
				<!-- Y -->
				<div class="row">
					<div class="col-75">
						<label for="adjustY">Ruhewert Y Querrichtung (in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="adjustY" name="adjustY" value="<?php echo $AD_adjustY; ?>" step="0,000001" min="-10" max="10">
					</div>
				</div>

				<!-- Z -->
				<div class="row">
					<div class="col-75">
						<label for="adjustZ">Ruhewert Z senkrecht (in m/s)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="adjustZ" name="adjustZ" value="<?php echo $AD_adjustZ; ?>" step="0,000001" min="-10" max="10">
					</div>
				</div>


				<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Manuelle Ruhewerte speichern">
				</div>
			</form>
		</div>
	
		<div id="power-button" class="menu-element hidden button main-menu">
			<a class="text" href="index.html">zurück zum Konfigurationsmenü</a>
		</div>

	</body>
</html>