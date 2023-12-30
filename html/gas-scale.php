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

		<p>ACHTUNG: Eingabefelder für Gasflaschen Waage Flasche 2 derzeit noch experimentell und in Entwicklung!</p>
		<p>&nbsp;</p>
		
		<!-----------------------------------------------------------------------------------
		   Defaults Waage 1
		------------------------------------------------------------------------------------>
	
		<?php
			$gasScale = file("/home/pi/CaravanPi/defaults/gasScaleDefaults1");
			$GS1_empty = intval($gasScale[0]);
			$GS1_full = intval($gasScale[1]);
			$GS1_pin_dout = intval($gasScale[2]);
			$GS1_pin_sck = intval($gasScale[3]);
			$GS1_channel = $gasScale[4];
			$GS1_refUnit = floatval($gasScale[5]);
			
			/*
			echo $GS1_empty; echo ", ";
			echo $GS1_full; echo ", ";
			echo $GS1_pin_dout; echo ", ";
			echo $GS1_pin_sck; echo ", ";
			echo $GS1_channel; echo ", ";
			echo $GS1_refUnit;
			*/
		?>

		<div class="container">
			<form class="caravanpi-form" action="writeGasScaleDefaults.py" method="post">

				<!-- Flaschennummer -->
				<div class="row">
					<div class="col-75">
						<h1>Waage für Gasflasche 1</h1> 
					</div>
					<div class="col-25">
						<input type="hidden" id="flasche" name="flasche-nr" value="1" >
					</div>
				</div>

				<!-- Leergewicht -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-leer">Leergewicht Gasflasche (in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="leer" name="gewicht-leer" value="<?php echo $GS1_empty; ?>" >
					</div>
				</div>

				<!-- Vollgewicht -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-voll">max. Gewicht des Flüssiggases (in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="voll" name="gewicht-voll" value="<?php echo $GS1_full; ?>" >
					</div>
				</div>

				<div class="row">
				<div class="col-75">
						<p><font color=red>Systemwerte - nur mit Bedacht ändern!</font></p>  
					</div>
				</div>

				<!-- GPIO Pin DOUT -->
				<div class="row">
					<div class="col-75">
						<label for="gpio_pin_dout">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GPIO Pin HX711 DOUT (auf CaravanPi Platine: 23)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="dout" name="gpio-pin-dout" value="<?php echo $GS1_pin_dout; ?>" >
					</div>
				</div>

				<!-- GPIO Pin SCK -->
				<div class="row">
					<div class="col-75">
						<label for="gpio_pin_sck">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GPIO Pin HX711 SCK (auf CaravanPi Platine: 24)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="sck" name="gpio-pin-sck" value="<?php echo $GS1_pin_sck; ?>" >
					</div>
				</div>

				<!-- HX711 Channel -->
				<div class="row">
					<div class="col-75">
						<label for="hx711_channel">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Channel HX711 (auf CaravanPi Platine: A)</label>  
					</div>
					<div class="col-25">
						<input type="string" pattern=[A-B] title="nur A oder B" id="channel" name="hx711-channel" value="<?php echo $GS1_channel; ?>" >
					</div>
				</div>

				<!-- HX711 Reference Unit -->
				<div class="row">
					<div class="col-75">
						<label for="hx711_refUnit">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reference Unit HX711 (Wert aus Kalibrierung)</label>  
					</div>
					<div class="col-25">
						<input type="string" id="refUnit" name="hx711-refUnit" value="<?php echo $GS1_refUnit; ?>" >
					</div>
				</div>

					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Defaults für Waage der Gasflasche 1 speichern">
				</div>
			</form>
		</div>

		<!-----------------------------------------------------------------------------------
		   Defaults Waage 2
		------------------------------------------------------------------------------------>
	
		<?php
			$gasScale = file("/home/pi/CaravanPi/defaults/gasScaleDefaults2");
			$GS2_empty = intval($gasScale[0]);
			$GS2_full = intval($gasScale[1]);
			$GS2_pin_dout = intval($gasScale[2]);
			$GS2_pin_sck = intval($gasScale[3]);
			$GS2_channel = $gasScale[4];
			$GS2_refUnit = floatval($gasScale[5]);
			
			/*
			echo $GS2_empty; echo ", ";
			echo $GS2_full; echo ", ";
			echo $GS2_pin_dout; echo ", ";
			echo $GS2_pin_sck; echo ", ";
			echo $GS2_channel; echo ", ";
			echo $GS2_refUnit;
			*/
		?>
	
		<div class="container">
			<form class="caravanpi-form" action="writeGasScaleDefaults.py" method="post">

				<!-- Flaschennummer -->
				<div class="row">
					<div class="col-75">
						<h1>Waage für Gasflasche 2</h1> 
					</div>
					<div class="col-25">
						<input type="hidden" id="flasche" name="flasche-nr" value="2" >
					</div>
				</div>

				<!-- Leergewicht -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-leer">Leergewicht Gasflasche (in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="leer" name="gewicht-leer" value="<?php echo $GS2_empty; ?>" >
					</div>
				</div>

				<!-- Vollgewicht -->
				<div class="row">
					<div class="col-75">
						<label for="gewicht-voll">max. Gewicht des Flüssiggases (in g)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="voll" name="gewicht-voll" value="<?php echo $GS2_full; ?>" >
					</div>
				</div>

				<div class="row">
				<div class="col-75">
						<p><font color=red>Systemwerte - nur mit Bedacht ändern!</font></p>  
					</div>
				</div>

				<!-- GPIO Pin DOUT -->
				<div class="row">
					<div class="col-75">
						<label for="gpio_pin_dout">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GPIO Pin HX711 DOUT (auf CaravanPi Platine: 23)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="dout" name="gpio-pin-dout" value="<?php echo $GS2_pin_dout; ?>" >
					</div>
				</div>

				<!-- GPIO Pin SCK -->
				<div class="row">
					<div class="col-75">
						<label for="gpio_pin_sck">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;GPIO Pin HX711 SCK (auf CaravanPi Platine: 24)</label>  
					</div>
					<div class="col-25">
						<input type="number" id="sck" name="gpio-pin-sck" value="<?php echo $GS2_pin_sck; ?>" >
					</div>
				</div>

				<!-- HX711 Channel -->
				<div class="row">
					<div class="col-75">
						<label for="hx711_channel">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Channel HX711 (auf CaravanPi Platine: A)</label>  
					</div>
					<div class="col-25">
						<input type="string" pattern=[A-B] title="nur A oder B" id="channel" name="hx711-channel" value="<?php echo $GS2_channel; ?>" >
					</div>
				</div>

				<!-- HX711 Reference Unit -->
				<div class="row">
					<div class="col-75">
						<label for="hx711_refUnit">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Reference Unit HX711 (Wert aus Kalibrierung)</label>  
					</div>
					<div class="col-25">
						<input type="string" id="refUnit" name="hx711-refUnit" value="<?php echo $GS2_refUnit; ?>" >
					</div>
				</div>

					<!-- Button -->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Defaults für Waage der Gasflasche 2 speichern">
				</div>
			</form>
		</div>


		<!-----------------------------------------------------------------------------------
		   Kalibrierung Waage 1
		------------------------------------------------------------------------------------>
	
		<div class="container">
			<form class="caravanpi-form" action="writeGasScaleCalibration.py" method="post">

				<!-- Flaschennummer -->
				<div class="row">
					<div class="col-75">
						<h1>Kalibrierung der Waage für Gasflasche 1</h1> 
						<p>
							Bitte nehmen Sie die Gasflasche von der Waage 1. <br/>
							<font color=red>Legen Sie ein Testgewicht auf die Waage.</font> <br/>
							Warten Sie dann ca. 2 Minuten bis die Waage ruhig steht. <br/>
							Kalibrieren Sie die Waage dann durch Drücken auf den nachfolgenden Button.<br/>
							<font color=red>Achtung: die Verarbeitung dauert etwas. Erst danach wird diese Seite aktualisiert.</font> <br/>
						</p>
					</div>
					<div class="col-25">
						<input type="hidden" id="flasche" name="flasche-nr" value="1" >
					</div>
				</div>

				<!-- Testgewicht -->
				<div class="row">
					<div class="col-75">
						<label for="kal-testgewicht">Wie schwer ist das Testgewicht? (in g)</label>  
					</div>
					<div class="col-25">
						<input type="string" id="testgewicht" name="kal-testgewicht" value="1" >
					</div>
				</div>

				<!-- Button autom. Kalibrierung-->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Kalibrierung der leeren Gasflaschen-Waage 1 starten">
				</div>

			</form>
		</div>
		
		<!-----------------------------------------------------------------------------------
		   Kalibrierung Waage 2
		------------------------------------------------------------------------------------>
	
		<div class="container">
			<form class="caravanpi-form" action="writeGasScaleCalibration.py" method="post">

				<!-- Flaschennummer -->
				<div class="row">
					<div class="col-75">
						<h1>Kalibrierung der Waage für Gasflasche 2</h1> 
						<p>
							Bitte nehmen Sie die Gasflasche von der Waage 2. <br/>
							<font color=red>Legen Sie ein Testgewicht auf die Waage.</font> <br/>
							Warten Sie dann ca. 2 Minuten bis die Waage ruhig steht. <br/>
							Kalibrieren Sie die Waage dann durch Drücken auf den nachfolgenden Button.<br/>
							<font color=red>Achtung: die Verarbeitung dauert etwas. Erst danach wird diese Seite aktualisiert.</font> <br/>
						</p>
					</div>
					<div class="col-25">
						<input type="hidden" id="flasche" name="flasche-nr" value="2" >
					</div>
				</div>

				<!-- Testgewicht -->
				<div class="row">
					<div class="col-75">
						<label for="kal-testgewicht">Wie schwer ist das Testgewicht? (in g)</label>  
					</div>
					<div class="col-25">
						<input type="string" id="testgewicht" name="kal-testgewicht" value="1" >
					</div>
				</div>

				<!-- Button autom. Kalibrierung-->
				<div class="row submit-button">
					<input type="submit" id="submit" name="submit" value="Kalibrierung der leeren Gasflaschen-Waage 2 starten">
				</div>

			</form>
		</div>
		
	
		<!-----------------------------------------------------------------------------------
		   zurueck
		------------------------------------------------------------------------------------>
	
		<div id="power-button" class="menu-element hidden button main-menu">
			<a class="text" href="index.html">zurück zum Konfigurationsmenü</a>
		</div>

		<div>
			<p>&nbsp;</p>
			<p>&nbsp;</p>
		</div>

	</body>
</html>
