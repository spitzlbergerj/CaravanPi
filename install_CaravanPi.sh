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
		eval "$@"
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
	
	echo "Überprüfe, ob ein Neustart erforderlich ist..."
	if [ -f /var/run/reboot-required ]; then
		echo "Ein Neustart ist erforderlich, um die Aktualisierungen zu vervollständigen."
		echo "Bitte führen Sie 'sudo reboot' aus."
	else
		echo "Kein Neustart erforderlich."
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

	echo "1-Wire installieren"
	run_cmd "sudo modprobe wire"
	run_cmd "sudo modprobe w1-gpio"
	run_cmd "sudo modprobe w1-therm"

    echo "Konfiguriere 1-Wire Module..."
    if ! grep -q '^wire$' /etc/modules; then
        run_cmd "echo \"wire\" | sudo tee -a /etc/modules > /dev/null"
    fi
    if ! grep -q '^w1-gpio$' /etc/modules; then
        run_cmd "echo \"w1-gpio\" | sudo tee -a /etc/modules > /dev/null"
    fi
    if ! grep -q '^w1-therm$' /etc/modules; then
        run_cmd "echo \"w1-therm\" | sudo tee -a /etc/modules > /dev/null"
    fi

    # Konfiguration von 1-Wire auf GPIO Pin 18 in /boot/config.txt, falls noch nicht vorhanden
    echo "Lege 1-Wire auf GPIO Pin 18..."
    if ! grep -q '^dtoverlay=w1-gpio,gpiopin=18$' /boot/config.txt; then
        run_cmd "echo \"# Temperature sensor on 1-Wire\" | sudo tee -a /boot/config.txt > /dev/null"
        run_cmd "echo \"dtoverlay=w1-gpio,gpiopin=18\" | sudo tee -a /boot/config.txt > /dev/null"
    fi

}


# Installation MagicMirror
install_magicmirror() {
	read -p "Möchten Sie MagicMirror installieren? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
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
	else
		echo "Installation von MagicMirror übersprungen."
	fi
}

install_apache() {
	read -p "Möchten Sie den Apache Webserver installieren? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
		echo "Apache installieren ...."
		run_cmd "sudo apt install apache2 -y"

		echo "Starte Apache2 und aktiviere den Autostart..."
		run_cmd "sudo systemctl start apache2"
		run_cmd "sudo systemctl enable apache2"

		# Überprüfe den Status des Apache2-Service
		echo "Überprüfe den Status des Apache2-Dienstes..."
		run_cmd "sudo systemctl status apache2"

		echo "Apache2 wurde erfolgreich installiert und läuft."
	else
		echo "Installation von Apache übersprungen."
	fi
}

# Installation MariaDB
install_mariadb() {
	read -p "Möchten Sie MariaDB installieren und alle Tabellen anlegen? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
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

	else
		echo "Installation von MariaDB übersprungen."
	fi
}


# Installation phpmyadmin
install_phpmyadmin() {
	read -p "Möchten Sie phpmyadmin installieren? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
		echo "phpmyadmin installieren ...."
		run_cmd "sudo apt install phpmyadmin"

		echo "Konfiguriere Apache2 für phpMyAdmin..."
		run_cmd "sudo phpenmod mbstring"
		run_cmd "sudo systemctl restart apache2"
	else
		echo "Installation von phpmyadmin übersprungen."
	fi
}

# Installation Grafana
install_grafana() {
	read -p "Möchten Sie Grafana installieren? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
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
	else
		echo "Installation von Grafana übersprungen."
	fi
}

# Installation Python Module
install_python_modules() {
	read -p "Möchten Sie die Python Module installieren? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
		echo "Python Module installieren ...."

		run_cmd "sudo apt-get install i2c-tools"


		run_cmd "pip install Flask"
		run_cmd "pip install mysql-connector-python"

	else
		echo "Installation von Python Module übersprungen."
	fi
}

# Installation Geräte Librarys
install_libraries() {
	read -p "Möchten Sie die Geräte Libraries installieren? (j/N): " answer
	if [[ "$answer" =~ ^[Jj]$ ]]; then
		echo "Libraries installieren ...."

		run_cmd "sudo apt-get install build-essential python-dev python-smbus git"
		
		run_cmd "git clone https://github.com/adafruit/Adafruit_Python_ADS1x15"
		run_cmd "cd Adafruit_Python_ADS1x15; sudo python3 setup.py install"


		run_cmd "pip3 install adafruit-circuitpython-lis3dh"
		run_cmd "pip3 install adafruit-circuitpython-busdevice"
		run_cmd "pip3 install adafruit-circuitpython-adxl34x"

		run_cmd "sudo pip3 install adafruit-circuitpython-mcp230xx"

	else
		echo "Installation von Libraries übersprungen."
	fi
}

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# 
# Skriptanfang
#
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

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
	if [ -f /var/run/reboot-required ]; then
		echo "Installationsskript wird beendet"
	fi
else
	echo "Update Raspberry OS übersprungen."
fi

# --------------------------------------------------------------------------
# CaravanPi Repository installieren
# --------------------------------------------------------------------------
note "Installation CaravanPi Repository"

install_update_caravanpi

# --------------------------------------------------------------------------
# MagicMirror installieren
# --------------------------------------------------------------------------
note "Installation MagicMirror" 

install_magicmirror

# --------------------------------------------------------------------------
# Apache Webserver installieren
# --------------------------------------------------------------------------
note "Installation Apache Webserver" 

install_apache

# --------------------------------------------------------------------------
# MariaDB installieren
# --------------------------------------------------------------------------
note "Installation MariaDB"

install_mariadb

# --------------------------------------------------------------------------
# phpmyadmin installieren
# --------------------------------------------------------------------------
note "Installation phpmyadmin"

install_phpmyadmin

# --------------------------------------------------------------------------
# Grafana installieren
# --------------------------------------------------------------------------
note "Installation Grafana"

install_grafana

# --------------------------------------------------------------------------
# Python Module installieren
# --------------------------------------------------------------------------
note "Installation Python Module"

install_python_modules

# --------------------------------------------------------------------------
# CaravanPi Config Lib initialisieren und damit ggf. defaults konvertieren
# --------------------------------------------------------------------------
note "CaravanPi Library initialisieren und ggf. defaults konvertieren"

python3 $CARAVANPI_DIR/installation/caravanPiLibInit.py
