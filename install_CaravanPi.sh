#!/bin/bash
# 
# Installieren des CaravanPi
#

# Titelbild ausgeben
echo -e "\e[0m"
echo '                                                                                                        '                                                                                                          
echo '  ,ad8888ba,                                                                             88888888ba   88'
echo ' d8""    `"8b                                                                            88      "8b  ""'
echo 'd8"                                                                                      88      ,8P    '
echo '88             ,adPPYYba,  8b,dPPYba,  ,adPPYYba,  8b       d8  ,adPPYYba,  8b,dPPYba,   88aaaaaa8P"  88'
echo '88             ""     `Y8  88P"   "Y8  ""     `Y8  `8b     d8"  ""     `Y8  88P"   `"8a  88"""""""    88'
echo 'Y8,            ,adPPPPP88  88          ,adPPPPP88   `8b   d8"   ,adPPPPP88  88       88  88           88'
echo ' Y8a.    .a8P  88,    ,88  88          88,    ,88    `8b,d8"    88,    ,88  88       88  88           88'
echo '  `"Y8888Y""   `"8bbdP"Y8  88          `"8bbdP"Y8      "8"      `"8bbdP"Y8  88       88  88           88'
echo '                                                                                                        '                                                                                                          
echo -e "\e[0m"


# Überprüfen, ob das Skript mit dem Parameter -force aufgerufen wird
# Nur dann werden die Installations Kommandos tatsächlich ausgeführt

SIMULATE=true
for arg in "$@"; do
	if [ "$arg" == "-force" ]; then
		SIMULATE=false
		break
	fi
done

BOOT_CONFIG_FILE_OLD="/boot/config.txt"
BOOT_CONFIG_FILE_NEW="/boot/firmware/config.txt"

STD_HOSTNAME="CaravanPi"

WIFI_CONFIG_FILE="/etc/wpa_supplicant/wpa_supplicant.conf"
WIFI_BASIC_CONFIG="ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE"

CARAVANPI_DIR="$HOME/CaravanPi"
CARAVANPI_LOCAL_BACKUP="$HOME/CaravanPilocalBackup"
CARAVANPI_MARIADB_CREATE_TABLES="$CARAVANPI_DIR/installation/CaravanPiValues.sql"

MAGICMIRROR_DIR="$HOME/MagicMirror"

GRAFANA_INI="/etc/grafana/grafana.ini"

red='\033[0;31m'
nc='\033[0m' # No Color

note() {
	# Paramter $1 enthält die Beschreibung des nächsten Schrittes
	local description=$1

	# Paramter $2 enthält den Switch für rote Schrift
	local color=$2

	# Prüfen, ob die Ausgabe in Rot erfolgen soll
	if [ "$color" == "red" ]; then
		echo -e "${red}"
	else
		echo -e "${nc}"
	fi

	# Ausgabe einer Trennlinie mit Sternen zur visuellen Trennung
	echo ""
	echo "********************************************************************************"
	echo "   $description"
	echo "********************************************************************************"

	# Farbe zurücksetzen
	echo -e "${nc}"
}


# Funktion, um Kommandos basierend auf der SIMULATE-Variable auszuführen oder anzuzeigen
run_cmd() {
	if [ "$SIMULATE" = true ]; then
		echo -e "${red}Simuliere:${nc} $@"
	else
		echo -e "${red}Führe aus:${nc} $@"
		eval "$@"
	fi
}

# Funktion zur Überprüfung der Installation
check_installed() {
	dpkg -s $1 &> /dev/null

	if [ $? -eq 0 ]; then
		return 0 # Installiert
	else
		return 1 # Nicht installiert
	fi
}

# Backup-Funktion, die das Skript localBackup.sh aufruft
backup_caravanpi() {
	echo "Starte Backup für CaravanPi..."
	# Pfad zum Backup-Skript (angepasst an Ihre Struktur)
	local backup_script="$CARAVANPI_DIR/localBackup.sh"
	if [ -f "$backup_script" ]; then
		run_cmd "bash \"$backup_script\""
	else
		echo "Backup-Skript nicht gefunden: $backup_script"
	fi
}

list_configured_ssids() {
	# Überprüfen, ob die Konfigurationsdatei existiert
	if [ ! -f "$WIFI_CONFIG_FILE" ]; then
		echo "keine Wifi SSIDs konfiguriert"
		return 1
	fi
	
	echo "aktuell konfigurierte SSIDs:"
	# Extrahieren und auflisten aller SSIDs
	sudo grep 'ssid=' "$WIFI_CONFIG_FILE" | sed -e 's/.*ssid="\([^"]*\)".*/\1/'
}

#m Funktion zum Updaten des Raspberry OS
update_raspberry_os() {
	echo "Aktualisiere Paketquellen..."
	run_cmd "sudo apt-get update -y"
	
	echo "Führe ein Upgrade aller installierten Pakete durch..."
	run_cmd "sudo apt-get upgrade -y"
	
	echo "Führe ein dist-upgrade durch, um sicherzustellen, dass auch Kernel und Firmware aktualisiert werden..."
	run_cmd "sudo apt-get dist-upgrade -y"
	
	echo "Bereinige nicht mehr benötigte Pakete..."
	run_cmd "sudo apt-get autoremove -y"
	
}

# Funktion zum Konfigurieren des Raspberry OS
config_raspberry_os() {
	echo "Land, Sprache und Zeitzone einstellen"
	run_cmd "sudo raspi-config nonint do_change_locale de_DE.UTF-8"
	run_cmd "sudo raspi-config nonint do_change_timezone Europe/Berlin"

	echo "Booten zum Desktop einstellen"	
	run_cmd "sudo raspi-config nonint do_boot_behaviour B4"
	
	echo "Overscan (schwarzer Bildschirmrand) deaktivieren"
	run_cmd "sudo raspi-config nonint do_overscan 1"

	echo "Hostnamen setzen"
	read -p "Geben Sie den neuen Hostnamen ein (Default: $STD_HOSTNAME): " answer
	if [[ -z $answer ]]; then
		answer=$STD_HOSTNAME
	fi
	run_cmd "sudo raspi-config nonint do_hostname $answer"
	
	echo "SSH aktivieren"
	run_cmd "sudo raspi-config nonint do_ssh 0"

	# Reboot anfordern
	# es ist noch zu prüfen, ob das immer gemacht werden muss
	#
	sudo touch /var/run/reboot-required
}

# Funktion zum Konfigurieren des WLAN
config_wifi() {
	# Überprüfen, ob die Konfigurationsdatei existiert
	if [ ! -f "$WIFI_CONFIG_FILE" ]; then
		echo "Konfigurationsdatei nicht gefunden. Erstelle eine neue mit Grundkonfiguration."
		run_cmd "echo \"$WIFI_BASIC_CONFIG\" | sudo tee \"$WIFI_CONFIG_FILE\" > /dev/null"
	fi

	# Eingabe der WIFI Daten
	echo
	echo "Geben Sie die notwendigen Daten ein"
	read -p "SSID: " ssid
	read -p "Passwort: " password
	echo

	# Überprüfen, ob SSID bereits konfiguriert ist
	if sudo grep -q "ssid=\"$ssid\"" "$WIFI_CONFIG_FILE"; then
		echo "Eine Konfiguration für SSID $ssid existiert bereits. Nichts zu tun!"
	else
		# Wenn die SSID noch nicht konfiguriert ist, hinzufügen
		run_cmd "wpa_passphrase \"$ssid\" \"$password\" | sudo tee -a \"$WIFI_CONFIG_FILE\" > /dev/null"
		echo "Neue Konfiguration für $ssid hinzugefügt."
		
		# WLAN-Dienst neu starten, um die neue Konfiguration zu übernehmen
		run_cmd "sudo systemctl restart wpa_supplicant"
		
		echo "WLAN-Konfiguration aktualisiert."
	fi
}


# Funktion zum Kponfigurieren des Raspberry OS
config_protocolls() {
	echo "I2C aktivieren"
	run_cmd "sudo raspi-config nonint do_i2c 0"
	echo "erkannte Devices am I2C:"
	run_cmd "i2cdetect -y 1"

	echo "1-Wire aktivieren"
	run_cmd "sudo raspi-config nonint do_onewire 0"

	echo "1-Wire konfigurieren"
	run_cmd "sudo modprobe wire"
	run_cmd "sudo modprobe w1-gpio"
	run_cmd "sudo modprobe w1-therm"

	echo "1-Wire in /etc/modules aufnehmen ..."
	if ! grep -q '^wire$' /etc/modules; then
		run_cmd "echo \"wire\" | sudo tee -a /etc/modules > /dev/null"
	fi
	if ! grep -q '^w1-gpio$' /etc/modules; then
		run_cmd "echo \"w1-gpio\" | sudo tee -a /etc/modules > /dev/null"
	fi
	if ! grep -q '^w1-therm$' /etc/modules; then
		run_cmd "echo \"w1-therm\" | sudo tee -a /etc/modules > /dev/null"
	fi

	# Konfiguration von 1-Wire auf GPIO Pin 18 in /boot/config.txt bzw. /boot/firmware/config.txt, falls noch nicht vorhanden
	BOOT_CONFIG_FILE="$BOOT_CONFIG_FILE_OLD"
	if [ -f "$BOOT_CONFIG_FILE_NEW" ]; then
		BOOT_CONFIG_FILE="$BOOT_CONFIG_FILE_NEW"
	fi

	echo "Lege 1-Wire auf GPIO Pin 18 (CaravanPi Platine) ..."

	# Prüfen, ob ein Eintrag für dtoverlay=w1-gpio vorhanden ist
	if grep -q '^dtoverlay=w1-gpio' "$BOOT_CONFIG_FILE"; then
		# Prüfen, ob der spezifische Eintrag mit gpiopin=18 existiert
		if ! grep -q '^dtoverlay=w1-gpio,gpiopin=18$' "$BOOT_CONFIG_FILE"; then
			# Wenn dtoverlay=w1-gpio vorhanden, aber nicht mit gpiopin=18, dann vorhandenes auskommentieren und neues ergänzen
			run_cmd "sed -i '/^dtoverlay=w1-gpio/c\# Alten dtoverlay=w1-gpio Eintrag auskommentiert, da nicht gpiopin=18\n# dtoverlay=w1-gpio,gpiopin=18' \"$BOOT_CONFIG_FILE\""
			run_cmd "echo \"# CaravanPi Temperatur Sensoren über 1-Wire auf GPIO Pin 18\" | sudo tee -a \"$BOOT_CONFIG_FILE\" > /dev/null"
			run_cmd "echo \"dtoverlay=w1-gpio,gpiopin=18\" | sudo tee -a \"$BOOT_CONFIG_FILE\" > /dev/null"
		else
			echo "Eintrag für dtoverlay=w1-gpio,gpiopin=18 ist bereits vorhanden. Keine Änderung notwendig."
		fi
	else
		# Wenn kein Eintrag für dtoverlay=w1-gpio vorhanden ist, dann hinzufügen
		run_cmd "echo \"# CaravanPi Temperatur Sensoren über 1-Wire auf GPIO Pin 18\" | sudo tee -a \"$BOOT_CONFIG_FILE\" > /dev/null"
		run_cmd "echo \"dtoverlay=w1-gpio,gpiopin=18\" | sudo tee -a \"$BOOT_CONFIG_FILE\" > /dev/null"
	fi
}

# Funktion zum Klonen/Aktualisieren des CaravanPi Repositories
install_update_caravanpi() {
	if [ -d "$CARAVANPI_DIR" ]; then
		echo "CaravanPi Repository ist bereits auf diesem Gerät vorhanden."
		read -p "Möchten Sie das Repository aktualisieren? (j/N): " answer
		if [[ "$answer" =~ ^[Jj]$ ]]; then
			cd "$CARAVANPI_DIR"
			echo "Prüfe Änderungen..."
			git fetch
			local changes=$(git diff HEAD..origin/master)
			if [ -n "$changes" ]; then
				echo "Änderungen verfügbar:"
				git diff --stat HEAD..origin/master
				read -p "Möchten Sie diese Änderungen anwenden? (j/n): " apply_changes
				if [[ "$apply_changes" == "j" || "$apply_changes" == "J" ]]; then
					backup_caravanpi
					echo "Aktualisiere CaravanPi Repository..."
					run_cmd "git merge origin/master"
				else
					echo "Aktualisierung abgebrochen."
				fi
			else
				echo "Keine Änderungen verfügbar. Repository ist aktuell."
			fi
		else
			echo "Aktualisierung nicht gewünscht."
		fi
	else
		# Repository herunterladen
		echo "CaravanPi Repository wird heruntergeladen..."
		run_cmd "git clone https://github.com/spitzlbergerj/CaravanPi.git \"$CARAVANPI_DIR\""
	fi

	echo "Ein/Ausschalter Skripte installieren"
	run_cmd "sudo cp /home/pi/CaravanPi/pishutdown/pishutdown.py /usr/local/bin"
	run_cmd "sudo cp /home/pi/CaravanPi/pishutdown/pishutdown.service /etc/systemd/system"
	run_cmd "sudo systemctl enable pishutdown"
	run_cmd "sudo systemctl start pishutdown"
}


# Installation MagicMirror
install_magicmirror() {
	# Pfad zu MagicMirror
	MAGICMIRROR_DIR="$HOME/MagicMirror"

	# Überprüfen, ob MagicMirror bereits geklont wurde
	if [ -d "$MAGICMIRROR_DIR" ]; then
		echo "MagicMirror scheint bereits installiert zu sein. Überspringe das Installieren..."
	else
		echo "MagicMirror Repository wird heruntergeladen..."
		cd $HOME
		run_cmd "bash -c  \"$(curl -sL https://raw.githubusercontent.com/sdetweil/MagicMirror_scripts/master/raspberry.sh)\""
	fi
}

install_apache() {
	echo "Apache installieren ...."
	run_cmd "sudo apt install apache2 -y"

	echo "Starte Apache2 und aktiviere den Autostart..."
	run_cmd "sudo systemctl start apache2"
	run_cmd "sudo systemctl enable apache2"

	# Überprüfe den Status des Apache2-Service
	echo "Überprüfe den Status des Apache2-Dienstes..."
	run_cmd "sudo systemctl status apache2"

	echo "Apache2 wurde erfolgreich installiert und läuft."
}

# Installation MariaDB
install_mariadb() {
	echo "MariaDB Server installieren ...."
	run_cmd "sudo apt-get install -y mariadb-server"

	echo "Installation absichern ... "
	echo "    Bitte folgen Sie den Anweisungen auf dem Bildschirm, um MariaDB und den root-Benutzer abzusichern."
	echo "    Vergeben Sie ein starkes Passwort für den MariaDB root-Benutzer und merken Sie sich dieses."
	echo "    Entfernen Sie anonyme Benutzer und deaktivieren Sie den Root-Login aus der Ferne."
	echo "    Löschen Sie die Testdatenbanken."
	run_cmd "sudo mysql_secure_installation"

	echo "Benutzer CaravanPi anlegen ... "
	read -sp "    Bitte geben Sie ein Passwort für den 'caravanpi' MariaDB Benutzer ein: " caravanpi_password

	echo "    Benutzer wird angelegt ..."
	run_cmd "sudo mysql -e \"CREATE USER 'caravanpi'@'localhost' IDENTIFIED BY '$caravanpi_password';\""

	echo "    Datenbank wird angelegt ..."
	run_cmd "sudo mysql -e \"CREATE DATABASE CaravanPiValues;\""
	run_cmd "sudo mysql -e \"GRANT ALL PRIVILEGES ON CaravanPiValues.* TO 'caravanpi'@'localhost';\""
	run_cmd "sudo mysql -e \"FLUSH PRIVILEGES;\""

	echo "   Datenbanktabellen werden angelegt ..."
	run_cmd "sudo mysql CaravanPiValues < $CARAVANPI_MARIADB_CREATE_TABLES"
}


# Installation phpmyadmin
install_phpmyadmin() {
	echo "phpmyadmin installieren ...."
	run_cmd "sudo apt install phpmyadmin"

	echo "Konfiguriere Apache2 für phpMyAdmin..."
	run_cmd "sudo phpenmod mbstring"
	run_cmd "sudo systemctl restart apache2"
}

# Installation Grafana
install_grafana() {
	# Füge das Grafana GPG Schlüssel hinzu
	echo "Füge Grafana GPG Schlüssel hinzu..."
	run_cmd "curl https://packages.grafana.com/gpg.key | sudo apt-key add -"

	# Füge das Grafana Repository hinzu
	echo "Füge das Grafana Repository hinzu..."
	run_cmd "echo \"deb https://packages.grafana.com/oss/deb stable main\" | sudo tee -a /etc/apt/sources.list.d/grafana.list"

	# Aktualisiere die Paketliste
	echo "Aktualisiere Paketlisten..."
	run_cmd "sudo apt update"

	# Installiere Grafana
	echo "Installiere Grafana..."
	run_cmd "sudo apt install grafana -y"

	# Starte den Grafana-Service und stelle sicher, dass er beim Booten läuft
	echo "Starte Grafana und aktiviere den Autostart..."
	run_cmd "sudo systemctl start grafana-server"
	run_cmd "sudo systemctl enable grafana-server"

	# Sichere die originale grafana.ini Datei
	run_cmd "sudo cp $GRAFANA_INI \"${GRAFANA_INI}.bak\""

	# Aktualisiere die Konfiguration für den anonymen Zugriff
	echo "Aktualisiere Grafana-Konfiguration für anonymen Zugriff..."
	run_cmd "sudo sed -i '/\[auth.anonymous\]/!b;n;c\enabled = true' $GRAFANA_INI"
	run_cmd "sudo sed -i '/\[auth.anonymous\]/!b;n;n;c\org_role = Viewer' $GRAFANA_INI"

	# Aktualisiere Sicherheitseinstellungen zur Einbettung
	echo "Erlaube das Einbetten von Grafana-Dashboards..."
	run_cmd "sudo sed -i '/\[security\]/!b;n;c\allow_embedding = true' $GRAFANA_INI"

	# Starte den Grafana-Dienst neu, um die Konfigurationsänderungen zu übernehmen
	echo "Starte Grafana-Dienst neu..."
	run_cmd "sudo systemctl restart grafana-server"	

	# Überprüfe den Status des Grafana-Dienstes
	echo "Überprüfe den Status des Grafana-Dienstes..."
	run_cmd "sudo systemctl status grafana-server"

	echo "Grafana wurde erfolgreich installiert und läuft."
}

# Installation Python Module
install_python_modules() {
	echo "Python Module installieren ...."

	run_cmd "sudo apt-get install i2c-tools"


	run_cmd "pip install Flask"
	run_cmd "pip install mysql-connector-python"
}

# Installation Geräte Librarys
install_libraries() {
	echo "Libraries installieren ...."

	run_cmd "sudo apt-get install build-essential python-dev python-smbus git"
	
	run_cmd "git clone https://github.com/adafruit/Adafruit_Python_ADS1x15"
	run_cmd "cd Adafruit_Python_ADS1x15; sudo python3 setup.py install"


	run_cmd "pip3 install adafruit-circuitpython-lis3dh"
	run_cmd "pip3 install adafruit-circuitpython-busdevice"
	run_cmd "pip3 install adafruit-circuitpython-adxl34x"

	run_cmd "sudo pip3 install adafruit-circuitpython-mcp230xx"
}

# ########################################################################################
# ########################################################################################
# ##                                                                                    ##
# ##                                     Skriptanfang                                   ##
# ##                                                                                    ##
# ########################################################################################
# ########################################################################################

if [ "$SIMULATE" = true ]; then
	note "Kommandos werden NICHT ausgeführt, lediglich Simulation" "red"
else
	note "ACHTUNG - Kommandos werden ausgeführt, keine Simulation" "red"
fi

# --------------------------------------------------------------------------
# Raspberry OS updaten
# --------------------------------------------------------------------------
note "Update Raspberry OS"

read -p "Möchten Sie Raspberry OS zunächst updaten? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	update_raspberry_os

	echo "Überprüfe, ob ein Neustart erforderlich ist..."
	if [ -f /var/run/reboot-required ]; then
		echo "Ein Neustart ist erforderlich, um die Aktualisierungen zu vervollständigen."
		echo "Bitte führen Sie 'sudo reboot' aus."
		exit
	else
		echo "Kein Neustart erforderlich."
	fi
fi

# --------------------------------------------------------------------------
# Raspberry OS konfigurieren
# --------------------------------------------------------------------------
note "Konfiguration Raspberry OS"

echo "Die nachfolgenden Konfigurationen werden in der Regel vom Raspberry Pi Imager bereits vorgenommen."
echo
read -p "Möchten Sie Raspberry OS konfigurieren (Sprache, Zeitzone, Hostname, SSH, ...)? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	config_raspberry_os

	echo "Überprüfe, ob ein Neustart erforderlich ist..."
	if [ -f /var/run/reboot-required ]; then
		echo "Ein Neustart ist erforderlich, um die Aktualisierungen zu vervollständigen."
		echo "Bitte führen Sie 'sudo reboot' aus."
		exit
	else
		echo "Kein Neustart erforderlich."
	fi
fi

# --------------------------------------------------------------------------
# WLAN konfigurieren
# --------------------------------------------------------------------------
note "Konfiguration Wifi"

echo
list_configured_ssids
echo

read -p "Möchten Sie die Wifi-Konfiguration ergänzen? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	config_wifi
	echo
	list_configured_ssids
	echo
fi


# --------------------------------------------------------------------------
# Raspberry OS erweitern
# --------------------------------------------------------------------------
note "Konfiguration benötigter Kommunikationsprotokolle"

read -p "Möchten Sie die benötigten Kommunikationsprotokolle aktivieren (i2c, 1-wire, ...)? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	config_protocolls

	echo "Überprüfe, ob ein Neustart erforderlich ist..."
	if [ -f /var/run/reboot-required ]; then
		echo "Ein Neustart ist erforderlich, um die Aktualisierungen zu vervollständigen."
		echo "Bitte führen Sie 'sudo reboot' aus."
		exit
	else
		echo "Kein Neustart erforderlich."
	fi
fi


# --------------------------------------------------------------------------
# CaravanPi Repository installieren
# --------------------------------------------------------------------------
note "Installation CaravanPi Repository"

read -p "Möchten Sie das CaravanPi Repository von GitHub klonen? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_update_caravanpi
fi

echo "Test Ende !!!"
exit

# --------------------------------------------------------------------------
# MagicMirror installieren
# --------------------------------------------------------------------------
note "Installation MagicMirror" 

read -p "Möchten Sie MagicMirror installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_magicmirror
fi

# --------------------------------------------------------------------------
# Apache Webserver installieren
# --------------------------------------------------------------------------
note "Installation Apache Webserver" 

read -p "Möchten Sie den Apache Webserver installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_apache
fi

# --------------------------------------------------------------------------
# MariaDB installieren
# --------------------------------------------------------------------------
note "Installation MariaDB"

read -p "Möchten Sie MariaDB installieren und alle Tabellen anlegen? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_mariadb
fi

# --------------------------------------------------------------------------
# phpmyadmin installieren
# --------------------------------------------------------------------------
note "Installation phpmyadmin"

read -p "Möchten Sie phpmyadmin installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_phpmyadmin
fi

# --------------------------------------------------------------------------
# Grafana installieren
# --------------------------------------------------------------------------
note "Installation Grafana"

read -p "Möchten Sie Grafana installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_grafana
fi

# --------------------------------------------------------------------------
# Python Module installieren
# --------------------------------------------------------------------------
note "Installation Python Module"

read -p "Möchten Sie die Python Module installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_python_modules
fi

# --------------------------------------------------------------------------
# Python Module installieren
# --------------------------------------------------------------------------
note "Installation Python Module"

read -p "Möchten Sie die Geräte Libraries installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_libraries
fi

# --------------------------------------------------------------------------
# CaravanPi Config Lib initialisieren und damit ggf. defaults konvertieren
# --------------------------------------------------------------------------
note "CaravanPi Library initialisieren und ggf. defaults konvertieren"

python3 $CARAVANPI_DIR/installation/caravanPiLibInit.py
