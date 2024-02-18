// ------------------------------------------------------------------
// Funktionen zum EInfügen der menüs in der Flask Installation
// ------------------------------------------------------------------
// 
function populateMainLinks(menu, includeHome) {
	var host = window.location.hostname;
	var port = window.location.port;

	var links = [
		{ text: "Startseite", url: 'http://' + host + ':5000/', isExternal: false, addSeparator: true   },
		{ text: "Statusanzeige CaravanPi, Sensoren, Applikationen, ...", url: 'http://' + host + ':5000/checks', isExternal: false, addSeparator: true, header: "Statusanzeige und Konfiguration"  },
		{ text: "Konfiguration der Abmessungen und Sensoren", url: 'http://' + host + ':5000/configs', isExternal: false, addSeparator: false  },
		{ text: "Kalibrierung der Sensoren", url: 'http://' + host + ':5000/calibration', isExternal: false, addSeparator: false  },
		{ text: "Test-Routinen", url: 'http://' + host + ':5000/tests', isExternal: false, addSeparator: true  },
		{ text: "MagicMirror Konfiguration", url: 'http://' + host + ':8080/remote.html#main-menu', isExternal: true, addSeparator: false, header: "MagicMirror"  },
		{ text: "MagicMirror Remote-Anzeige", url: 'http://' + host + ':8080', isExternal: true, addSeparator: true  },
		{ text: "Grafana Website", url: 'http://' + host + ':3000', isExternal: true, addSeparator: false, header: "MariaDB"  },
		{ text: "phpMyAdmin", url: 'http://' + host + '/phpmyadmin/', isExternal: true, addSeparator: true  },
		{ text: "CaravanPi Config anzeigen", url: 'http://' + host + ':5000/show_config', isExternal: true, addSeparator: false, header: "Sonstiges"  },
		{ text: "RPi neu starten", url: 'http://' + host + ':5000/reboot', isExternal: true, addSeparator: false  },
		{ text: "RPi ausschalten", url: 'http://' + host + ':5000/shutdown', isExternal: false, addSeparator: false  },
	];

	if (!includeHome) {
		links.shift(); // Entfernt die Startseite, wenn includeHome false ist
	}

	links.forEach(function(link) {
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

		if (link.addSeparator) {
			var separator = document.createElement('br'); // Erstellt eine Leerzeile als Trennzeichen
			menu.appendChild(separator);
		}
	});
}

function populateConfigLinks(menu) {
	var host = window.location.hostname;
	var port = window.location.port;

	var links = [
		{ text: "Grundeinstellungen CaravanPi", url: 'http://' + host + ':5000/config_caravanpi', isExternal: false, addSeparator: true  },
		{ text: "Dimensionen Caravan bzw. Wohnmobil", url: 'http://' + host + ':5000/config_dimension_caravan', isExternal: false, addSeparator: false  },
		{ text: "Lagesensor", url: 'http://' + host + ':5000/config_lagesensor', isExternal: false, addSeparator: false },
		{ text: "Gasflaschen-Waagen", url: 'http://' + host + ':5000/config_gaswaage', isExternal: false, addSeparator: false },
		{ text: "Tanks", url: 'http://' + host + ':5000/config_tanks', isExternal: false, addSeparator: false },
		{ text: "Batterie", url: 'http://' + host + ':5000/config_voltage', isExternal: false, addSeparator: false },
	];

	links.forEach(function(link) {
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

		if (link.addSeparator) {
			var separator = document.createElement('br'); // Erstellt eine Leerzeile als Trennzeichen
			menu.appendChild(separator);
		}
	});
}

function populateCalibrationLinks(menu) {
	var host = window.location.hostname;
	var port = window.location.port;

	var links = [
		{ text: "Lagesensor", url: 'http://' + host + ':5000/calibration_lage', isExternal: false, addSeparator: false },
		{ text: "Gasflaschen-Waagen", url: 'http://' + host + ':5000/calibration_waage', isExternal: false, addSeparator: false },
	];

	links.forEach(function(link) {
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

		if (link.addSeparator) {
			var separator = document.createElement('br'); // Erstellt eine Leerzeile als Trennzeichen
			menu.appendChild(separator);
		}
	});
}

function populateTestLinks(menu) {
	var host = window.location.hostname;
	var port = window.location.port;

	var links = [
		{ text: "Testen der LEDs", url: 'http://' + host + ':5000/test_LED', isExternal: false, addSeparator: false },
		{ text: "Statusanzeige CaravanPi, Sensoren, Applikationen, ...", url: 'http://' + host + ':5000/checks', isExternal: false, addSeparator: false  },
	];

	links.forEach(function(link) {
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

		if (link.addSeparator) {
			var separator = document.createElement('br'); // Erstellt eine Leerzeile als Trennzeichen
			menu.appendChild(separator);
		}
	});
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
		populateMainLinks(mainMenu, false); // Hauptmenü 
	}

	var hamburgerMenu = document.getElementById("hamburgerMenu");
	if (hamburgerMenu) {
		populateMainLinks(hamburgerMenu, true); // Hamburger-Menü mit Startseite
	}

	// weitere Menüs für Unterseiten, soweit vorhanden
	var configMenu = document.getElementById("configMenu");
	if (configMenu) {
		populateConfigLinks(configMenu); // Hauptmenü der Konfiguration
	}

	var calibrationMenu = document.getElementById("calibrationMenu");
	if (calibrationMenu) {
		populateCalibrationLinks(calibrationMenu); // Hauptmenü der Kalibrierung
	}

	var testsMenu = document.getElementById("testsMenu");
	if (testsMenu) {
		populateTestLinks(testsMenu); // Hauptmenü der Tests
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
