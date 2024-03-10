// ------------------------------------------------------------------
// Funktionen zum EInfügen der menüs in der Flask Installation
// ------------------------------------------------------------------
// 

// Definition von Variablen
var host = window.location.hostname;
var port = window.location.port;

// Definition des Hauptmenüs für das Hamburgermenü und das Hauptmenü auf der Startseite
var links_main = [
	{ text: "Startseite", url: 'http://' + host + ':5000/', isExternal: false, addSeparator: true   },
	{ text: "Status", url: 'http://' + host + ':5000/checks', isExternal: false, addSeparator: false, header: "CaravanPi"  },
	{ text: "Konfiguration", url: 'http://' + host + ':5000/configs', isExternal: false, addSeparator: false  },
	{ text: "Kalibrierung", url: 'http://' + host + ':5000/calibration', isExternal: false, addSeparator: false  },
	{ text: "Tests", url: 'http://' + host + ':5000/tests_home', isExternal: false, addSeparator: true  },
	{ text: "Konfiguration", url: 'http://' + host + ':8080/remote.html#main-menu', isExternal: true, addSeparator: false, header: "MagicMirror"  },
	{ text: "Remote-Anzeige", url: 'http://' + host + ':8080', isExternal: true, addSeparator: true  },
	{ text: "Grafana Website", url: 'http://' + host + ':3000', isExternal: true, addSeparator: false, header: "MariaDB"  },
	{ text: "phpMyAdmin", url: 'http://' + host + '/phpmyadmin/', isExternal: true, addSeparator: true  },
	{ text: "Config anzeigen", url: 'http://' + host + ':5000/show_config', isExternal: true, addSeparator: false, header: "Anzeigen"  },
	{ text: "LOGs anzeigen", url: 'http://' + host + ':5000/list_logs', isExternal: true, addSeparator: false  },
	{ text: "i2c Bus", url: 'http://' + host + ':5000/i2cdetect', isExternal: true, addSeparator: true  },
	{ text: "RPi neu starten", url: 'http://' + host + ':5000/reboot', isExternal: true, addSeparator: false, header: "Raspberry Pi"   },
	{ text: "RPi ausschalten", url: 'http://' + host + ':5000/shutdown', isExternal: false, addSeparator: false  },
];

var links_config = [
	{ text: "Grundeinstellungen", url: 'http://' + host + ':5000/config_caravanpi', isExternal: false, addSeparator: true, header: "CaravanPi" },
	{ text: "Caravan bzw. Wohnmobil", url: 'http://' + host + ':5000/config_dimension_caravan', isExternal: false, addSeparator: false, header: "Dimensionen" },
	{ text: "Lagesensor", url: 'http://' + host + ':5000/config_lagesensor', isExternal: false, addSeparator: true },
	{ text: "Gasflaschen-Waagen", url: 'http://' + host + ':5000/config_gaswaage', isExternal: false, addSeparator: false, header: "Geräte" },
	{ text: "Tanks", url: 'http://' + host + ':5000/config_tanks', isExternal: false, addSeparator: false },
	{ text: "Batterie", url: 'http://' + host + ':5000/config_voltage', isExternal: false, addSeparator: false },
];

var links_calibration = [
	{ text: "Lagesensor", url: 'http://' + host + ':5000/calibration_lage', isExternal: false, addSeparator: false, header: "Kalibrierung" },
	{ text: "Gasflaschen-Waagen", url: 'http://' + host + ':5000/calibration_waage', isExternal: false, addSeparator: false },
];

var links_tests = [
	{ text: "LEDs", url: 'http://' + host + ':5000/test_LEDs', isExternal: false, addSeparator: false, header: "Tests" },
	{ text: "Buzzers", url: 'http://' + host + ':5000/test_buzzer', isExternal: false, addSeparator: false },
	{ text: "Taster", url: 'http://' + host + ':5000/test_switches', isExternal: false, addSeparator: true },
	{ text: "Statusanzeige", url: 'http://' + host + ':5000/checks', isExternal: false, addSeparator: false  },
];

var links_aktoren = [
	{ text: "230V Alarm", url: 'http://' + host + ':5000/aktor/alarm_230v_aus', isExternal: false, addSeparator: false, header: "Alarme aus" },
	{ text: "12V Bord Alarm", url: 'http://' + host + ':5000/aktor/alarm_12v_bord_aus', isExternal: false, addSeparator: false },
	{ text: "12V Car Alarm", url: 'http://' + host + ':5000/aktor/alarm_12v_car_aus', isExternal: false, addSeparator: false },
	{ text: "LED an", url: 'http://' + host + ':5000/actors/LED?LED_status=on', isExternal: false, addSeparator: false, header: "ESP82-1"  },
	{ text: "LED aus", url: 'http://' + host + ':5000/actors/LED?LED_status=off', isExternal: false, addSeparator: false  },
];

// Funktion zum Erzeugen des Hauptmenü als Buttons aus der gemeinsamen Liste
function populateMenusAsButtons(container, linksData, includeHome) {
	if (!includeHome) {
		linksData.shift(); // Entfernt die Startseite, wenn includeHome false ist
	}

	let rowContainer = null;
	let buttonContainer = null;

	linksData.forEach(function(link, index) {
		// Neuen row-container für den ersten Link oder wenn eine neue Überschrift vorhanden ist
		if (index === 0 || link.header) {
			// Vorherigen row-container abschließen, falls vorhanden
			if (rowContainer) {
				container.appendChild(rowContainer);
			}

			// Neuen row-container erstellen
			rowContainer = document.createElement('div');
			rowContainer.className = 'menu-row-container';

			// header-container erstellen, falls eine Überschrift vorhanden ist
			if (link.header) {
				const headerContainer = document.createElement('div');
				headerContainer.className = 'menu-header-container';
				headerContainer.textContent = link.header;
				rowContainer.appendChild(headerContainer);
			}

			// Neuen button-container für die Buttons erstellen
			buttonContainer = document.createElement('div');
			buttonContainer.className = 'menu-button-container';
			rowContainer.appendChild(buttonContainer);
		}

		// Buttons erstellen und zum button-container hinzufügen
		const button = document.createElement('button');
		button.className = 'menu-button';
		button.textContent = link.text;
		button.onclick = function() {
			if (link.isExternal) {
				window.open(link.url, '_blank');
			} else {
				window.location.href = link.url;
			}
		};
		buttonContainer.appendChild(button);
	});

	// Letzten row-container zum container hinzufügen
	if (rowContainer) {
		container.appendChild(rowContainer);
	}
}


function populateMainAsButtons(menu, includeHome) {
	var localLinks = [...links_main]; // Erstellt eine Kopie des links-Arrays, damit shift nicht dauerhaft wirkt
	populateMenusAsButtons(menu, localLinks, includeHome)
}

// Funktion zum Erzeugen des Hauptmenü als Links (für Hamburgermenü) aus der gemeinsamen Liste
function populateMainAsLinks(menu, includeHome) {
	var localLinks = [...links_main]; // Erstellt eine Kopie des links-Arrays, damit shift nicht dauerhaft wirkt

	if (!includeHome) {
		localLinks.shift(); // Entfernt die Startseite, wenn includeHome false ist
	}

	localLinks.forEach(function(link) {
		// Prüft, ob eine Überschrift eingefügt werden soll
		if (link.header) {
			var header = document.createElement('h3'); // Oder eine andere geeignete Überschriftsebene
			header.textContent = link.header;
			menu.appendChild(header);
		}

		var a = document.createElement('a');
		a.href = link.url;
		a.textContent = link.text;
		if (link.isExternal) {
			a.target = "_blank"; // Öffnet den Link in einem neuen Fenster/Tab
		}
		menu.appendChild(a);

		if(link.addSeparator) {
			menu.appendChild(document.createElement('br'));
		}
	});
}

function populateConfigLinks(menu) {
	var localLinks = [...links_config]; // Erstellt eine Kopie des links-Arrays, damit shift nicht dauerhaft wirkt
	populateMenusAsButtons(menu, localLinks, true)
}

function populateCalibrationLinks(menu) {
	var localLinks = [...links_calibration]; // Erstellt eine Kopie des links-Arrays, damit shift nicht dauerhaft wirkt
	populateMenusAsButtons(menu, localLinks, true)
}

function populateTestLinks(menu) {
	var localLinks = [...links_tests]; // Erstellt eine Kopie des links-Arrays, damit shift nicht dauerhaft wirkt
	populateMenusAsButtons(menu, localLinks, true)
}

function populateAktorLinks(menu) {
	var localLinks = [...links_aktoren]; // Erstellt eine Kopie des links-Arrays, damit shift nicht dauerhaft wirkt
	console.log("Aktoren als Buttons bauen ...");
	populateMenusAsButtons(menu, localLinks, true)
}

function toggleHamburgerMenu() {
	var menu = document.getElementById("hamburgerMenu");
	if (menu.style.display === "block") {
		menu.style.display = "none";
	} else {
		menu.style.display = "block";
	}
}

window.onload = function() {
	// Hauptmenü und Hamburgermenü, soweit vorhanden
	var mainMenu = document.getElementById("mainMenu");
	if (mainMenu) {
		console.log("main bauen ...");
		populateMainAsButtons(mainMenu, false); // Hauptmenü 
	}

	var hamburgerMenu = document.getElementById("hamburgerMenu");
	if (hamburgerMenu) {
		console.log("hamburger bauen ...");
		populateMainAsLinks(hamburgerMenu, true); // Hamburger-Menü mit Startseite
	}

	// weitere Menüs für Unterseiten, soweit vorhanden
	var configMenu = document.getElementById("configMenu");
	if (configMenu) {
		console.log("config bauen ...");
		populateConfigLinks(configMenu); // Hauptmenü der Konfiguration
	}

	var calibrationMenu = document.getElementById("calibrationMenu");
	if (calibrationMenu) {
		console.log("calibration bauen ...");
		populateCalibrationLinks(calibrationMenu); // Hauptmenü der Kalibrierung
	}

	var testsMenu = document.getElementById("testsMenu");
	if (testsMenu) {
		console.log("tests bauen ...");
		populateTestLinks(testsMenu); // Hauptmenü der Tests
	}

	console.log("Aktoren Menü suchen ...");

	var aktorMenu = document.getElementById("aktorMenu");
	console.log("Aktoren gefunden?", aktorMenu);

	if (aktorMenu) {
		console.log("Aktoren Menü bauen ...");
		populateAktorLinks(aktorMenu); // Hauptmenü der Aktoren
	}

};

function hideAndShowMessage() {
	var message = document.querySelector('.flash-message');
	if (message) {
		message.style.display = 'none'; // Versteckt die Nachricht
		setTimeout(function() {
			message.style.display = 'block'; // Zeigt die Nachricht nach einer kurzen Verzögerung wieder an
		}, 500); // 500 Millisekunden Verzögerung
	}
}
