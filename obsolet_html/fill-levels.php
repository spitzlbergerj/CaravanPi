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
		
		<!-- Anweisgung für Darstellung auf mobilen Devices (SmartPhone, Tablet) -->
		<meta name="viewport" content="width=device-width, initial-scale=1">
		
		<!-- Anweisung für Google: Seite nicht übersetzen -->
		<meta name="google" content="notranslate" />
	</head>

	<body>
		<header class="header">CaravanPi Konfiguration - Einstellungen Füllstände Tanks</header>
		
		<?php
			$fwTank = file("/home/pi/CaravanPi/defaults/tankDefaults1");
			$FW_tankNumber = 1;
			$FW_level1 = intval($fwTank[0]);
			$FW_level2 = intval($fwTank[1]);
			$FW_level3 = intval($fwTank[2]);
			$FW_level4 = intval($fwTank[3]);
			
			$wwTank = file("/home/pi/CaravanPi/defaults/tankDefaults2");
			$WW_tankNumber = 2;
			$level1 = intval($wwTank[0]);
			$level2 = intval($wwTank[1]);
			$level3 = intval($wwTank[2]);
			$level4 = intval($wwTank[3]);
			
		?>
	
		<div class="container">
			<form class="caravanpi-form" action="writeTankDefaults.py" method="post">

				<!-- Tank Nummer -->
				<div class="row">
					<div class="col-75">
						<h1>Frischwassertank</h1>  
					</div>
					<div class="col-25">
						<input type="hidden" id="tankNumber" name="tankNumber" value="<?php echo $FW_tankNumber; ?>" >
					</div>
				</div>

				<!-- Fülllevel 1 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 1 Füllmenge (in l) - geringste Menge</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level1" name="level1" value="<?php echo $FW_level1; ?>" >
					</div>
				</div>

				<!-- Fülllevel 2 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 2 Füllmenge (in l)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level2" name="level2" value="<?php echo $FW_level2; ?>" >
					</div>
				</div>

				<!-- Fülllevel 3 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 3 Füllmenge (in l)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level3" name="level3" value="<?php echo $FW_level3; ?>" >
					</div>
				</div>

				<!-- Fülllevel 4 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 4 Füllmenge (in l)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level4" name="level4" value="<?php echo $FW_level4; ?>" >
					</div>
				</div>


					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Füllmengen Frischwassertank speichern">
				</div>
			</form>
		</div>
			
		<div class="container">
			<form class="caravanpi-form" action="writeTankDefaults.py" method="post">

				<!-- Tank Nummer -->
				<div class="row">
					<div class="col-75">
						<h1>Fäkalientank</h1>  
					</div>
					<div class="col-25">
						<input type="hidden" id="tankNumber" name="tankNumber" value="<?php echo $WW_tankNumber; ?>" >
					</div>
				</div>

				<!-- Fülllevel 1 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 1 Füllmenge (in l) - geringste Menge</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level1" name="level1" value="<?php echo $level1; ?>" >
					</div>
				</div>

				<!-- Fülllevel 2 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 2 Füllmenge (in l)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level2" name="level2" value="<?php echo $level2; ?>" >
					</div>
				</div>

				<!-- Fülllevel 3 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 3 Füllmenge (in l)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level3" name="level3" value="<?php echo $level3; ?>" >
					</div>
				</div>

				<!-- Fülllevel 4 Liter -->
				<div class="row">
					<div class="col-75">
						<label for="level1">Level 4 Füllmenge (in l)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="level4" name="level4" value="<?php echo $level4; ?>" >
					</div>
				</div>


					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Füllmengen Fäkalientank speichern">
				</div>
			</form>
		</div>
	
		<div id="power-button" class="menu-element hidden button main-menu">
			<a class="text" href="index.html">zurück zum Konfigurationsmenü</a>
		</div>

	</body>
</html>