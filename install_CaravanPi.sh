#!/bin/bash
# 
# Installieren des CaravanPi
#

# Alle Ausgaben zusätzlich in ein Logfile schreiben
LOG_FILE="$HOME/install_CaravanPi.log"
ip_address=$(hostname -I | awk '{print $1}')

# Schreibe die Raspberry Pi Revision und IP-Adresse ins Logfile
{
    echo "------------------------------------------------------------"
    echo "Inhalt von /proc/cpuinfo:"
    echo "------------------------------------------------------------"
	cat /proc/cpuinfo
    echo "------------------------------------------------------------"
    echo "IP-Adresse: $ip_address"
    echo "------------------------------------------------------------"
} > "$LOG_FILE"

# alle weiteren Ausgaben in das Logfile clonen
exec > >(tee -a "$LOG_FILE") 2>&1

echo -e "\e[0m"
echo '                                                                                     '
echo '  $$$$$$\                                                            $$$$$$$\  $$\   '
echo ' $$  __$$\                                                           $$  __$$\ \__|  '
echo ' $$ /  \__| $$$$$$\   $$$$$$\  $$$$$$\ $$\    $$\ $$$$$$\  $$$$$$$\  $$ |  $$ |$$\   '
echo ' $$ |       \____$$\ $$  __$$\ \____$$\\$$\  $$  |\____$$\ $$  __$$\ $$$$$$$  |$$ |  '
echo ' $$ |       $$$$$$$ |$$ |  \__|$$$$$$$ |\$$\$$  / $$$$$$$ |$$ |  $$ |$$  ____/ $$ |  '
echo ' $$ |  $$\ $$  __$$ |$$ |     $$  __$$ | \$$$  / $$  __$$ |$$ |  $$ |$$ |      $$ |  '
echo ' \$$$$$$  |\$$$$$$$ |$$ |     \$$$$$$$ |  \$  /  \$$$$$$$ |$$ |  $$ |$$ |      $$ |  '
echo '  \______/  \_______|\__|      \_______|   \_/    \_______|\__|  \__|\__|      \__|  '
echo '                                                                                     '                                                                                                          
echo -e "\e[0m"
                                                                                 

# ------------------------------------------------------------------
# parameter Verarbeitung
# ------------------------------------------------------------------

# Überprüfen, ob das Skript mit dem Parameter "apply" aufgerufen wird
# Nur dann werden die Installations Kommandos tatsächlich ausgeführt

SIMULATE=true

# Überprüfen, wie das Skript gestartet wurde
# Das Skript kann auf dem Raspberry direkt aufgerufen worden sein (CaravanPi Repository wurde vorher schon geklont) oder
# das Skript wird über "bash -c ... curl ..." aufgerufen, also ohne vorheriges Klonen.
# entprechend muss der Parameter apply anders erkannt werden

p0=$0
# start ohne "bash -c" und es gibt einen Parameter
if [ $0 != 'bash' -a "$1." != "." ]; then
	# wird lokal ausgeführt
	# $1 enthält den Parameter
	p0=$1
fi

# Den Parameter in Kleinbuchstaben umwandeln
p0=$(echo $p0 | awk '{print tolower($0)}')

# Entsprechend dem Parameter handeln
if [ "$p0" == "apply" ]; then
	SIMULATE=false
fi

# ------------------------------------------------------------------
# Variable definieren
# ------------------------------------------------------------------

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

RASPBERRY_PI_BACKUP_CLOUD_DIR="$HOME/Raspberry-Pi-Backup-Cloud"

# ANSI Farbcodes
no_color='\033[0m' # Keine Farbe
nc="$no_color"

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;34m'
magenta='\033[0;35m'
cyan='\033[0;36m'

read_colored() {
	local color_code="$1"
	local prompt="$2"
	local var_name="$3"
	
	# Wähle die Farbe basierend auf dem Parameter
	case "$color_code" in
		red) color=$red ;;
		green) color=$green ;;
		yellow) color=$yellow ;;
		blue) color=$blue ;;
		magenta) color=$magenta ;;
		cyan) color=$cyan ;;
		*) color=$no_color ;; # Standardfarbe, falls keine Übereinstimmung gefunden wurde
	esac

	# Zeige den farbigen Prompt an und lese die Eingabe
	echo -en "${color}${prompt}${no_color}"
	read -r "$var_name"
}

echo_colored() {
	local color_code="$1"
	local output="$2"
	
	# Wähle die Farbe basierend auf dem Parameter
	case "$color_code" in
		red) color=$red ;;
		green) color=$green ;;
		yellow) color=$yellow ;;
		blue) color=$blue ;;
		magenta) color=$magenta ;;
		cyan) color=$cyan ;;
		*) color=$no_color ;; # Standardfarbe, falls keine Übereinstimmung gefunden wurde
	esac

	# Zeige den farbigen Prompt an und lese die Eingabe
	echo -e "${color}${output}${no_color}"
}


note() {
	# Paramter $1 enthält die Beschreibung des nächsten Schrittes
	local description=$1

	# Paramter $2 enthält den Switch für rote Schrift
	local color=$2

	# Prüfen, ob die Ausgabe in Rot erfolgen soll
	if [ "$color" == "red" ]; then
		echo -e "${red}"
	elif [ "$color" == "green" ]; then
		echo -e "${green}"
	elif [ "$color" == "yellow" ]; then
		echo -e "${yellow}"
	elif [ "$color" == "blue" ]; then
		echo -e "${blue}"
	elif [ "$color" == "magenta" ]; then
		echo -e "${magenta}"
	elif [ "$color" == "cyan" ]; then
		echo -e "${cyan}"
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
	echo -e "${red}Achtung: Das setzen der Sprache wird erst nach eine Rebbot fehlerfrei sein.${nc}"
	echo "Ignorieren Sie daher eventuell auftretende Fehler zur Spracheinstellung."
	echo "Führen Sie jedoch nach diesem Kapitel einen rebbot durch"
	echo
	echo "Land, Sprache und Zeitzone einstellen"
	run_cmd "sudo raspi-config nonint do_change_locale de_DE.UTF-8"
	run_cmd "sudo raspi-config nonint do_change_timezone Europe/Berlin"

	echo "Booten zum Desktop einstellen"	
	run_cmd "sudo raspi-config nonint do_boot_behaviour B4"
	
	echo "Overscan (schwarzer Bildschirmrand) deaktivieren"
	run_cmd "sudo raspi-config nonint do_overscan 1"

	echo "Hostnamen setzen"
	read_colored "cyan" "Geben Sie den neuen Hostnamen ein (Default: $STD_HOSTNAME): " answer
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

	while true; do
		echo
		list_configured_ssids
		echo

		read_colored "cyan" "Möchten Sie die Wifi-Konfiguration ergänzen? (j/N): " answer
		if ! [[ "$answer" =~ ^[Jj]$ ]]; then
			break
   		fi

		# Eingabe der WIFI Daten
		echo
		echo "Geben Sie die notwendigen Daten ein"
		read_colored "cyan" "SSID: " ssid
		read_colored "cyan" "Passwort: " password
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
	done
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
			# Wenn dtoverlay=w1-gpio vorhanden, aber nicht mit gpiopin=18, dann vorhandenes auskommentieren 
			run_cmd "sudo sed -i '/^dtoverlay=w1-gpio/ s/^/# Alten Eintrag von der Installationsroutine CaravanPi auskommentiert\n#&/' \"$BOOT_CONFIG_FILE\""
			# Und neuen Eintrag ergänzen
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
		cd "$CARAVANPI_DIR"
		# Ermittle den aktuellen Branch
		local current_branch=$(git rev-parse --abbrev-ref HEAD)

		echo
		echo "CaravanPi Repository ist bereits auf diesem Gerät vorhanden."
		echo "Lokal wird der Branch - $current_branch - benutzt. Dieser wird mit dem entsprechenden Branch auf github verglichen"
		echo
		read_colored "cyan" "Möchten Sie das Repository aktualisieren? (j/N): " answer
		if [[ "$answer" =~ ^[Jj]$ ]]; then
			cd "$CARAVANPI_DIR"
			echo "Prüfe Änderungen..."
			git fetch

			local target_branch="master"
			if [[ "$current_branch" == "development" ]]; then
				target_branch="development"
			fi

			local changes=$(git diff HEAD..origin/$target_branch)

			if [ -n "$changes" ]; then
				"Änderungen verfügbar auf $target_branch Branch:"
				git diff --stat HEAD..origin/$target_branch
				echo
				read_colored "cyan" "Möchten Sie diese Änderungen anwenden? (j/n): " apply_changes
				if [[ "$apply_changes" =~ ^[Jj]$ ]]; then
					echo "Backup der bisherigen Konfigurationen wird ausgeführt"
					backup_caravanpi
					echo "Aktualisiere CaravanPi Repository von $target_branch..."
					run_cmd "git merge origin/$target_branch"
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
		echo "CaravanPi Repository wird heruntergeladen..."
		# Klonen des Repositories in den spezifizierten Branch
		run_cmd "git clone https://github.com/spitzlbergerj/CaravanPi.git \"$CARAVANPI_DIR\""
		run_cmd "cd \"$CARAVANPI_DIR\""
  		run_cmd "git fetch origin development:development"

		# Ermittle die verfügbaren Branches vom Remote-Repository
		echo "Verfügbare Branches:"
		run_cmd "git branch"

		# nachfolgendes nur falls nicht nur simuliert (zu komplex für run_cmd)
		if [ "$SIMULATE" = false ]; then
			while true; do
				# Frage nach dem gewünschten Branch
				echo "Im Regelfall nutzen Sie bitte den master Branch!"
				read_colored "cyan" "Welchen Branch möchten Sie nutzen? (default: master) " target_branch

				if [[ -z $target_branch ]]; then
					target_branch="master"
				fi

				# Überprüfen, ob der eingegebene Branch existiert
				if git rev-parse --verify "$target_branch" > /dev/null 2>&1; then
					echo "Wechsle zu Branch '$target_branch'..."
					git checkout "$target_branch"
					break
				else
					echo "Der Branch '$target_branch' existiert nicht. Überprüfen Sie die Eingabe und versuchen Sie es erneut."
					echo
				fi
			done
		fi
	fi

	# git hooks aktivieren
	echo "git hooks anlegen"
	cd "$CARAVANPI_DIR"
	run_cmd "cp .git_hooks/*commit .git/hooks"
	run_cmd "chmod +x .git/hooks/*commit"
	run_cmd "mkdir ~/CaravanPi/.git_sensible_backup"

	echo 
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
		echo "Notwendige Updates führen Sie dort bitte selbst durch. Skripte hierzu finden Sie auf https://github.com/sdetweil/MagicMirror_scripts"
	else
		echo "MagicMirror Repository wird heruntergeladen..."
		cd $HOME
		# run_cmd kann hier nicht verwendet werden, weil curl vor der Übergabe an run_cmd ausgeführt wird
		# daher hier direkt abgefragt

		echo "In manchen Fällen wird während der Installaion von MagicMirror nachfolgende Warnung (vielfach) ausgegeben"
		echo " ... MaxListenersExceededWarning: Possible EventEmitter memory leak detected ..."
		echo "Diese Warnungen können Sie ignorieren. Die Installation klappt dennoch. Installation daher nicht abbrechen!!"
		echo
		read_colored "cyan" "Weiter mit Enter" irrelevant


		if [ "$SIMULATE" = true ]; then
			echo -e "${red}Simuliere:${nc} bash -c  \"\$(curl -sL https://raw.githubusercontent.com/sdetweil/MagicMirror_scripts/master/raspberry.sh)\""
		else
			echo -e "${red}Führe aus:${nc} bash -c  \"\$(curl -sL https://raw.githubusercontent.com/sdetweil/MagicMirror_scripts/master/raspberry.sh)\""

			# zunächst wird das Skript heruntergeladen und zwiwchengespeichert
			curl -sL https://raw.githubusercontent.com/sdetweil/MagicMirror_scripts/master/raspberry.sh > /tmp/raspberry.sh
			# dann ausführen
			bash /tmp/raspberry.sh
		fi
	fi
}

install_apache() {
	echo "Apache installieren ...."
	run_cmd "sudo apt-get install apache2 -y"

	echo "Starte Apache2 und aktiviere den Autostart..."
	run_cmd "sudo systemctl start apache2"
	run_cmd "sudo systemctl enable apache2"

	# Überprüfe den Status des Apache2-Service
	echo "Überprüfe den Status des Apache2-Dienstes..."
	run_cmd "sudo systemctl status apache2"

	# PHP im Apache aktivieren
	echo "Füge PHP Fähigkeit hinzu ..."
	run_cmd "sudo apt-get install php php-mbstring"

	echo "Apache2 wurde erfolgreich installiert und läuft."
}

# Installation MariaDB
install_mariadb() {
	echo "MariaDB Server installieren ...."
	run_cmd "sudo apt-get install -y mariadb-server"

	echo
	echo
	caravanpi_password=""
	while [ -z "$caravanpi_password" ]; do
		read_colored "cyan" "Bitte geben Sie ein Passwort für den Benutzer 'caravanpi' auf der MariaDB ein: " caravanpi_password
		if [ -z "$caravanpi_password" ]; then
			echo "Das Passwort darf nicht leer sein. Bitte versuchen Sie es erneut."
		fi
	done
	
	echo
	echo "    Benutzer CaravanPi wird angelegt ..."
	run_cmd "sudo mysql -e \"CREATE USER 'caravanpi'@'localhost' IDENTIFIED BY '$caravanpi_password';\""

	echo "    Datenbank CaravanPiValues wird angelegt ..."
	run_cmd "sudo mysql -e \"CREATE DATABASE CaravanPiValues;\""
	run_cmd "sudo mysql -e \"GRANT ALL PRIVILEGES ON CaravanPiValues.* TO 'caravanpi'@'localhost';\""
	run_cmd "sudo mysql -e \"FLUSH PRIVILEGES;\""

	echo "   Datenbanktabellen werden angelegt ..."
	run_cmd "sudo mysql CaravanPiValues < $CARAVANPI_MARIADB_CREATE_TABLES"

	echo
	echo "Die Datenbank enthält nun folgende Tabellen:"
	run_cmd "sudo mysql -u'caravanpi' -p'$caravanpi_password' -e \"SHOW TABLES in CaravanPiValues\""
}


# Installation phpmyadmin
install_phpmyadmin() {
	echo "phpmyadmin installieren ...."
	echo
	echo -e "${red}Achtung: Sie bekommen während der nachfolgenden Installation einige Fragen gestellt:${nc}"
	echo " - die Frage nach dem Webserver beantworten Sie mit Apache2"
	echo -e "     ${red}ACHTUNG${nc}, hier unbedingt ${red}Leertaaste im Feld Apache2${nc} drücken, Stern erscheint, dann TAB zu OK"
	echo
	echo " - die Frage 'Konfigurieren der Datenbank für phpmyadmin mit dbconfig-common?' beantworten Sie mit JA! (TAB zu JA)"
	echo
	echo " - die Frage 'Passwort für phpmyadmin Benutzer?' beantworten Sie mit einem Return"
	echo 
	read_colored "cyan" "Weiter mit Enter" irrelevant
	echo 
	run_cmd "sudo apt-get install phpmyadmin"

	echo "Konfiguriere Apache2 für phpMyAdmin..."
	run_cmd "sudo phpenmod mbstring"
	
	run_cmd "echo \"# phpmyadmin aktivieren\" | sudo tee -a /etc/apache2/apache2.conf > /dev/null"
	run_cmd "echo \"Include /etc/phpmyadmin/apache.conf\" | sudo tee -a /etc/apache2/apache2.conf > /dev/null"
	run_cmd "sudo systemctl restart apache2"
}

# Absichern MariaDB - erst nsch Installation von myphpadmin!
secure_mariadb() {
	echo "MariaDB Server absichern ...."
	echo
	echo
	root_password=""
	while [ -z "$root_password" ]; do
		read_colored "cyan" "Bitte geben Sie ein Passwort für den Benutzer 'root' auf der MariaDB ein: " root_password
		if [ -z "$root_password" ]; then
			echo "Das Passwort darf nicht leer sein. Bitte versuchen Sie es erneut."
		fi
	done

	echo
	echo "Installation absichern ... "

	# wir ersetzen hier sudo mysql_secure_installation durch eine Reihe von Einzelbefehlen, da 
	# mysql_secure_installation micht gut innerhalb eines Skriptes ausführbar ist

	# SQL-Befehle, um die MariaDB-Sicherheitseinstellungen anzupassen
	sql_commands="
	ALTER USER 'root'@'localhost' IDENTIFIED BY '${root_password}';
	DELETE FROM mysql.user WHERE User='';
	DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
	DROP DATABASE IF EXISTS test;
	DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
	FLUSH PRIVILEGES;
	"
	run_cmd "sudo mysql -u root -e \"$sql_commands\""
}


# Installation Grafana
install_grafana() {
	# Füge APT Keys hinzu
	echo "Füge APT Keys hinzu"
	run_cmd "sudo mkdir -p /etc/apt/keyrings/"
	run_cmd "wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null"

	# Füge das Grafana Repository hinzu
	echo "Füge das Grafana Repository hinzu..."
	run_cmd "echo \"deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main\" | sudo tee -a /etc/apt/sources.list.d/grafana.list"

	# Paketliste nochmal aktualisieren
	echo "Aktualisiere Paketlisten..."
	run_cmd "sudo apt-get update"

	# Installiere Grafana
	echo "Installiere Grafana..."
	run_cmd "sudo apt-get install -y grafana"

	# Starte den Grafana-Service und stelle sicher, dass er beim Booten läuft
	echo "Starte Grafana und aktiviere den Autostart..."
	run_cmd "sudo systemctl enable grafana-server"
	run_cmd "sudo systemctl start grafana-server"

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

# Installation Geräte Librarys
install_libraries() {
	echo "Libraries installieren ...."
	cd "$CARAVANPI_DIR/.lib"

	run_cmd "sudo apt-get install fping"

	run_cmd "sudo apt-get install i2c-tools"

	run_cmd "pip3 install adafruit-circuitpython-ads1x15 --break-system-packages"
	run_cmd "pip3 install adafruit-circuitpython-lis3dh --break-system-packages"
	run_cmd "pip3 install adafruit-circuitpython-busdevice --break-system-packages"
	run_cmd "pip3 install adafruit-circuitpython-adxl34x --break-system-packages"
	run_cmd "pip3 install adafruit-circuitpython-mcp230xx --break-system-packages"

	run_cmd "pip3 install bme680 --break-system-packages"

	run_cmd "pip3 install netaddr --break-system-packages"

	run_cmd "pip3 install board --break-system-packages"
	run_cmd "pip3 install busio --break-system-packages"

	run_cmd "pip3 install digitalio --break-system-packages"

	run_cmd "pip3 install crontab --break-system-packages"

	# outdated
	# run_cmd "sudo apt-get install python-dev python-smbus"
	# run_cmd "sudo apt-get install build-essential git"
}


# Installation Python Module
install_python_modules() {
	echo "Python Module für MariaDB, MQTT und Flask installieren ...."

	echo " ... mysql connector"
	run_cmd "pip3 install mysql-connector-python --break-system-packages"
	echo " ... mqtt connector"
	run_cmd "pip3 install paho-mqtt==1.6.1 --break-system-packages"
	echo " ... Flask Framework"
	run_cmd "pip3 install Flask --break-system-packages"

	# Apache für Flask konfigurieren
	# Apache wird der Proxy, jedoch muss /phpmyadmin weiterhin erreichbar bleiben
	echo " ... Apache für Flask vorbereiten"
	run_cmd "sudo a2enmod proxy"
	run_cmd "sudo a2enmod proxy_http"

	# Füge ProxyPass zu 000-default.conf hinzu, um auf Flask-App zu verweisen
	# und sicherzustellen, dass phpMyAdmin weiterhin funktioniert
	run_cmd "echo \"<VirtualHost *:80>\" | sudo tee /etc/apache2/sites-available/000-default.conf"
	run_cmd "echo \"    ServerAdmin webmaster@localhost\" | sudo tee -a /etc/apache2/sites-available/000-default.conf"
	run_cmd "echo \"    DocumentRoot /var/www/html\" | sudo tee -a /etc/apache2/sites-available/000-default.conf"
	run_cmd "echo \"    ProxyPass /phpmyadmin !\" | sudo tee -a /etc/apache2/sites-available/000-default.conf"
	run_cmd "echo \"    ProxyPass / http://127.0.0.1:5000/\" | sudo tee -a /etc/apache2/sites-available/000-default.conf"
	run_cmd "echo \"    ProxyPassReverse / http://127.0.0.1:5000/\" | sudo tee -a /etc/apache2/sites-available/000-default.conf"
	run_cmd "echo \"</VirtualHost>\" | sudo tee -a /etc/apache2/sites-available/000-default.conf"

	echo "Flask als Systemdienst einrichten"
	run_cmd "sudo cp $CARAVANPI_DIR/.systemd-files/flask.service /etc/systemd/system/"
	run_cmd "sudo systemctl daemon-reload"
	run_cmd "sudo systemctl enable flask.service"
	run_cmd "sudo systemctl start flask.service"

	echo "Apache neu starten"
	run_cmd "sudo service apache2 restart"

}

# Installation Backup Routinr
install_backup() {
	echo "Backup Routine installieren ...."

	if [ -d "$RASPBERRY_PI_BACKUP_CLOUD_DIR" ]; then
		# Routine beretis installiert
		cd "$RASPBERRY_PI_BACKUP_CLOUD_DIR"
		# Ermittle den aktuellen Branch
		local current_branch=$(git rev-parse --abbrev-ref HEAD)

		echo
		echo "Raspberry-Pi-Backup-Cloud Repository ist bereits auf diesem Gerät vorhanden."
		echo "Lokal wird der Branch - $current_branch - benutzt. Dieser wird mit dem entsprechenden Branch auf github verglichen"
		echo
		read_colored "cyan" "Möchten Sie das Repository aktualisieren? (j/N): " answer
		if [[ "$answer" =~ ^[Jj]$ ]]; then
			cd "$RASPBERRY_PI_BACKUP_CLOUD_DIR"
			echo "Prüfe Änderungen..."
			git fetch

			local target_branch="master"
			if [[ "$current_branch" == "development" ]]; then
				target_branch="development"
			fi

			local changes=$(git diff HEAD..origin/$target_branch)

			if [ -n "$changes" ]; then
				"Änderungen verfügbar auf $target_branch Branch:"
				git diff --stat HEAD..origin/$target_branch
				echo
				read_colored "cyan" "Möchten Sie diese Änderungen anwenden? (j/n): " apply_changes
				if [[ "$apply_changes" =~ ^[Jj]$ ]]; then
					echo "Aktualisiere Raspberry-Pi-Backup-Cloud Repository von $target_branch..."
					run_cmd "git merge origin/$target_branch"
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
		echo "Raspberry-Pi-Backup-Cloud Repository wird heruntergeladen..."
		# Klonen des Repositories in den spezifizierten Branch
		run_cmd "git clone https://github.com/spitzlbergerj/Raspberry-Pi-Backup-Cloud.git \"$RASPBERRY_PI_BACKUP_CLOUD_DIR\""
		run_cmd "cd \"$RASPBERRY_PI_BACKUP_CLOUD_DIR\""

		# Ermittle die verfügbaren Branches vom Remote-Repository
		# echo "Verfügbare Branches:"
		# run_cmd "git branch"

		# nachfolgendes nur falls nicht nur simuliert (zu komplex für run_cmd)
		# if [ "$SIMULATE" = false ]; then
		# 	while true; do
		# 		# Frage nach dem gewünschten Branch
		# 		echo "Im Regelfall nutzen Sie bitte den main Branch!"
		#		read_colored "cyan" "Welchen Branch möchten Sie nutzen? (default: main)" target_branch

		#		if [[ -z $target_branch ]]; then
		#			target_branch="main"
		#		fi

		#		# Überprüfen, ob der eingegebene Branch existiert
		#		if git rev-parse --verify "$target_branch" > /dev/null 2>&1; then
		#			echo "Wechsle zu Branch '$target_branch'..."
		#			git checkout "$target_branch"
		#			break
		#		else
		#			echo "Der Branch '$target_branch' existiert nicht. Überprüfen Sie die Eingabe und versuchen Sie es erneut."
		#			echo
		#		fi
		#	done
		# fi
	fi

	run_cmd "ln -s $RASPBERRY_PI_BACKUP_CLOUD_DIR/backup /home/pi/backup"
	run_cmd "cp $CARAVANPI_DIR/.backup-config/backup2ndScript.sh /home/pi/backup/.config/backup2ndScript.sh"
	run_cmd "cp $CARAVANPI_DIR/.backup-config/backup_dirs.txt /home/pi/backup/.config/backup_dirs.txt"
	run_cmd "cp $CARAVANPI_DIR/.backup-config/backup_name.txt /home/pi/backup/.config/backup_name.txt"
	run_cmd "cp $RASPBERRY_PI_BACKUP_CLOUD_DIR/backup/.config/rclone.conf-muster /home/pi/backup/.config/rclone.conf"

	run_cmd "chmod +x /home/pi/backup/backup.sh /home/pi/backup/.config/backup2ndScript.sh"

	# Installation von rclone
	echo "Installation von rclone"
	if [ "$SIMULATE" = false ]; then
		curl https://rclone.org/install.sh | sudo bash
	fi

	echo
	echo_colored "magenta" "rclone muss noch zwingend konfiguriert werden."
	echo_colored "magenta" "Eine Beschreibung hierzu finden Sie unter https://github.com/spitzlbergerj/Raspberry-Pi-Backup-Cloud"
	echo
	echo

}

next_steps() {

	note "Abschluss und nächste Schritte" "cyan"

	echo
	echo
	echo_colored "magenta" "Sie haben es nun beinahe geschafft! Nun folgen noch manuelle Schritte"
	echo
	echo "- reboot durchführen"
	echo "     Sie sollten nach Abschluss der Installation einen reboot durchführen"
	echo "     Sie können sich diesen Text noch einmal ausgeben lassen, "
	echo "     wenn Sie dieses Installations-Skript noch einmal nur mit dem Paramter 'next' starten"
	echo
	echo "- rclone konfigurieren"
	echo "     Damit die Datensicherung klappt, müssen Sie noch rclone entsprechend konfigurieren"
	echo "     Eine gute Beschreibung hierfür finden Sie unter https://github.com/spitzlbergerj/Raspberry-Pi-Backup-Cloud"
	echo
	echo "- CaravanPi Konfiguration durchführen"
	echo "     Vieles am CaravanPi wird über eine Konfigruationsdatei gesteuert. Diese xml Datei können Sie komfortabel"
	echo "     über die CaravanPI Website befüllen. Gehen Sie dazu auf http://$ip_address/configs und führen Sie"
	echo "     nacheinander alle Konfigurationsschritte durch"
	echo
	echo "- Crontabs kontrollieren und anpassen"
	echo "     Dieses Skript hat für die Crontabs meine Muster Crontabs eingesetzt. Spätestens nach dem Booten werden"
	echo "     die CaravanPi Programme beginnen, die Sensoren abzufragen und in Datei, Datenbank zu schreiben"
	echo "     und an den MQTT Broker zu senden."
	echo "     Ändern Sie die Crontab nach Ihren Bedürfnissen. Nehmen Sie z.B. Programme außer Betrieb, falls noch"
	echo "     entsprechenden Sensoren verbaut wurden."
	echo
	echo
	echo "- Sensoren in den Caravan einbauen und mit der CaravanPi Platine verbinden"
	echo "     Der letzte Schritt ist dann natürlich die Hardware Sensoren in den Caravan einzubauen"
	echo "     Auf dem CaravanPi Wiki finden Sie hierzu ausführliche Erläuterungen, wie ich das erledigt habe"
	echo
	echo
}

# ########################################################################################
# ########################################################################################
# ##                                                                                    ##
# ##                                     Skriptanfang                                   ##
# ##                                                                                    ##
# ########################################################################################
# ########################################################################################

# Wenn der Parameter next lautet, dann nur noch den Abschluss Text ausgeben
if [ "$p0" == "next" ]; then
	next_steps
	exit
fi

if [ "$SIMULATE" = true ]; then
	note "Kommandos werden NICHT ausgeführt, lediglich Simulation" "green"
else
	note "ACHTUNG - Kommandos werden ausgeführt !!! " "red"
fi

cd "$HOME"

echo "Die Installation von CaravanPi erfolgt in mehreren Schritten. Für das Funktionieren des CaravanPi sind alle Schritte vonnöten."
echo "Überspringen Sie Schritte nur, wenn Sie wissen was Sie tun bzw. wenn Sie nach einem erforderlichen Reboot alle Schritte "
echo "überspringen, die Sie schon ausgeführt haben."
echo
echo "Die Reihenfolge der einzelnen Schritte ist ebenfalls wichtig und einzuhalten."
echo
echo "Die einzelnen Kommados geben sehr viele Daten aus. Um die Übersicht zu erhöhen folge ich diesen Farb-Codex:"
echo_colored "cyan" "CYAN für Kapitelüberschriften und Abfragen an Sie"
echo_colored "magenta" "MAGENTA für wichtige Informationen"
echo
echo

# --------------------------------------------------------------------------
# Raspberry OS updaten
# --------------------------------------------------------------------------
note "Update Raspberry OS" "cyan"

read_colored "cyan" "Möchten Sie Raspberry OS zunächst updaten? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	update_raspberry_os

	echo "Überprüfe, ob ein Neustart erforderlich ist..."
	if [ -f /var/run/reboot-required ]; then
		echo
		echo
		echo "Ein Neustart ist erforderlich, um die Aktualisierungen zu vervollständigen."
		echo "Bitte führen Sie 'sudo reboot' aus."
		echo "Anschließend starten Sie das Installationsskript erneut und überspringen die Sektionen bis Konfiguration Raspberry OS."
		echo
		echo
		exit
	else
		echo "Kein Neustart erforderlich."
	fi
fi

cd "$HOME"

# --------------------------------------------------------------------------
# Raspberry OS konfigurieren
# --------------------------------------------------------------------------
note "Konfiguration Raspberry OS" "cyan"

echo "Die nachfolgenden Konfigurationen werden in der Regel vom Raspberry Pi Imager bereits vorgenommen."
echo
read_colored "cyan" "Möchten Sie Raspberry OS konfigurieren (Sprache, Zeitzone, Hostname, SSH, ...)? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	config_raspberry_os

	echo "Überprüfe, ob ein Neustart erforderlich ist..."
	if [ -f /var/run/reboot-required ]; then
		echo
		echo
		echo "Ein Neustart ist erforderlich, um die Aktualisierungen zu vervollständigen."
		echo "Bitte führen Sie 'sudo reboot' aus."
		echo "Anschließend starten Sie das Installationsskript erneut und überspringen die Sektionen bis Wifi."
		echo
		echo
		exit
	else
		echo "Kein Neustart erforderlich."
	fi
fi

cd "$HOME"

# --------------------------------------------------------------------------
# WLAN konfigurieren (mehrere WLANs über eine Schleife)
# --------------------------------------------------------------------------
note "Konfiguration Wifi - mehrere Eingaben möglich" "cyan"

config_wifi

cd "$HOME"

# --------------------------------------------------------------------------
# Raspberry OS erweitern
# --------------------------------------------------------------------------
note "Konfiguration benötigter Kommunikationsprotokolle" "cyan"

read_colored "cyan" "Möchten Sie die benötigten Kommunikationsprotokolle aktivieren (i2c, 1-wire, ...)? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	config_protocolls
fi

cd "$HOME"

# --------------------------------------------------------------------------
# CaravanPi Repository installieren
# --------------------------------------------------------------------------
note "Installation CaravanPi Repository" "cyan"

read_colored "cyan" "Möchten Sie das CaravanPi Repository von GitHub klonen? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_update_caravanpi
fi

cd "$HOME"

# --------------------------------------------------------------------------
# MagicMirror installieren
# --------------------------------------------------------------------------
note "Installation MagicMirror"  "cyan"

read_colored "cyan" "Möchten Sie MagicMirror installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_magicmirror

	echo
	echo "Nachinstallieren des async Moduls von npm"
	cd "$HOME/MagicMirror"
	run_cmd "npm install async"

	echo
	echo "Installieren einiger MagicMirror Module ... "
	cd "$HOME/MagicMirror/modules"
	echo " ... MMM-SimpleLogo für das CaravanPi Logo"
	run_cmd "git clone https://github.com/frdteknikelektro/MMM-SimpleLogo.git"
	cd MMM-SimpleLogo
	run_cmd "npm install"
	run_cmd "cp $HOME/CaravanPi/images/CaravanPi-Logo-weiss.png ~/MagicMirror/modules/MMM-SimpleLogo/public/CaravanPi-Logo-weiss.png"

	cd "$HOME/MagicMirror/modules"
	echo " ... MMM-Remote-Control um den MagicMirror per Website konfigurieren zu können"
	run_cmd "git clone https://github.com/Jopyth/MMM-Remote-Control"
	cd MMM-Remote-Control
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo " ... MMM-MarineWeather als Wetteranzeige"
	run_cmd "git clone https://github.com/grenagit/MMM-MarineWeather"
	cd MMM-MarineWeather
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo " ... MMM-Sunrise-Sunset"
	run_cmd "git clone https://github.com/prydonian/MMM-Sunrise-Sunset"
	cd MMM-Sunrise-Sunset
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo " ... MMM-CaravanPi Module"
	echo "     ... MMM-CaravanPiTemperature"
	run_cmd "git clone https://github.com/spitzlbergerj/MMM-CaravanPiTemperature"
	cd MMM-CaravanPiTemperature
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo "     ... MMM-CaravanPiGasWeight"
	run_cmd "git clone https://github.com/spitzlbergerj/MMM-CaravanPiGasWeight"
	cd MMM-CaravanPiGasWeight
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo "     ... MMM-CaravanPiClimate"
	run_cmd "git clone https://github.com/spitzlbergerj/MMM-CaravanPiClimate"
	cd MMM-CaravanPiClimate
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo "     ... MMM-CaravanPiPosition"
	run_cmd "git clone https://github.com/spitzlbergerj/MMM-CaravanPiPosition"
	cd MMM-CaravanPiPosition
	run_cmd "npm install"

	cd "$HOME/MagicMirror/modules"
	echo " ... MMM-GrafanaEmbedded zum Anzeigen der Grafana Grafen"
	run_cmd "git clone https://github.com/eirikaho/MMM-GrafanaEmbedded.git"

	echo "Kopieren der CaravanPi config.js und der custom.css ..."
	run_cmd "cp -f $HOME/CaravanPi/MagicMirror/config/config.js $HOME/MagicMirror/config"
	run_cmd "cp -f $HOME/CaravanPi/MagicMirror/css/custom.css $HOME/MagicMirror/css"


	echo "Starten des MagicMirror"
	run_cmd "pm2 start MagicMirror"

	echo
	echo_colored "magenta" "MagicMirror sollte nun in Kürze auf Ihrem Bildschirm erscheinen"
	echo

fi

cd "$HOME"

# --------------------------------------------------------------------------
# Apache Webserver installieren
# --------------------------------------------------------------------------
note "Installation Apache Webserver"  "cyan"

read_colored "cyan" "Möchten Sie den Apache Webserver installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_apache

	echo
	echo_colored "magenta" "Sie sollten nun auf die Website Ihres CaravanPi zugreifen können."
	echo "Rufen Sie dazu die Website http://$ip_address/ auf."
	echo

fi

cd "$HOME"

# --------------------------------------------------------------------------
# MariaDB installieren
# --------------------------------------------------------------------------
note "Installation MariaDB" "cyan"

read_colored "cyan" "Möchten Sie MariaDB installieren und alle Tabellen anlegen? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_mariadb

	echo
	echo_colored "magenta" "Nach der Installation von phpmyadmin wird die MariaDB noch abgesichert"
	echo
fi

cd "$HOME"


# --------------------------------------------------------------------------
# phpmyadmin installieren
# --------------------------------------------------------------------------
note "Installation phpmyadmin" "cyan"

read_colored "cyan" "Möchten Sie phpmyadmin installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_phpmyadmin

	echo
	echo_colored "magenta" "Sie sollten nun auf phpMyAdmin und damit die Datenbank zugreifen können."
	echo "Rufen Sie dazu die Website http://$ip_address/phpmyadmin auf."
	echo

fi

cd "$HOME"

# --------------------------------------------------------------------------
# MariaDB absichern
# --------------------------------------------------------------------------
note "MariaDB absichern" "cyan"

read_colored "cyan" "Möchten Sie die MariaDB absichern? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	secure_mariadb
fi

cd "$HOME"

# --------------------------------------------------------------------------
# Grafana installieren
# --------------------------------------------------------------------------
note "Installation Grafana" "cyan"

read_colored "cyan" "Möchten Sie Grafana installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_grafana

	echo
	echo_colored "magenta" "Sie sollten nun auf Grafana zugreifen können."
	echo "Rufen Sie dazu die Website http://$ip_address:3000 auf."
	echo

fi

cd "$HOME"

# --------------------------------------------------------------------------
# diverse Libraries installieren
# --------------------------------------------------------------------------
note "Installation diverser Libraries" "cyan"

read_colored "cyan" "Möchten Sie die notwendigen Libraries installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_libraries
fi

cd "$HOME"

# --------------------------------------------------------------------------
# Python Module installieren
# --------------------------------------------------------------------------
note "Installation Python Module für MariaDB, MQTT und Flask" "cyan"

read_colored "cyan" "Möchten Sie die Python Module installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_python_modules
	
	echo
	echo_colored "magenta" "Sie sollten nun auf die CaravanPi Bedienungs-Website zugreifen können."
	echo "Rufen Sie dazu jetzt erneut die Website http://$ip_address auf."
	echo
	echo_colored "magenta" "Sie können dort bereits jetzt den bisherigen Installationsstatus einsehen."
	echo "Klicken Sie dazu auf den Button 'Status'"
	echo "Achtung: Sie werden dabei vermutlich einen Fehler bei der MariaDB bekommen."
	echo "Dies liegt daran, dass Sie in der CaravanPi Konfiguration die User Daten noch nicht gesetzt haben."
	echo "Rufen Sie hierzu folgende Seite auf: http://$ip_address/config_caravanpi"

fi

cd "$HOME"

# --------------------------------------------------------------------------
# Backup Routine clonen und einrichten
# --------------------------------------------------------------------------
note "Backup Routine installieren" "cyan"

read_colored "cyan" "Möchten Sie die Backup Routine installieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	install_backup
fi

cd "$HOME"

# --------------------------------------------------------------------------
# Bewegungsssensor aktivieren
# --------------------------------------------------------------------------
note "Bewegungssernsor aktivieren" "cyan"

read_colored "cyan" "Möchten Sie den Bewegungssensor aktivieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then

	echo "PIR Sensor als Systemdienst einrichten"
	run_cmd "sudo cp $CARAVANPI_DIR/.systemd-files/pir.service /etc/systemd/system/"
	run_cmd "sudo systemctl daemon-reload"
	run_cmd "sudo systemctl enable pir.service"
	run_cmd "sudo systemctl start pir.service"
fi

cd "$HOME"


# --------------------------------------------------------------------------
# logrotate einrichten
# --------------------------------------------------------------------------
note "Logrotate konfigurieren" "cyan"

read_colored "cyan" "Möchten Sie logrotate für CaravanPi aktivieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	run_cmd "echo -e \"\n# CaravanPi\ninclude /home/pi/CaravanPi/logrotate/logrotate-CaravanPi.conf\" | sudo tee -a /etc/logrotate.conf > /dev/null"
	run_cmd "sudo find \"$CARAVANPI_DIR\" -type f -name \"*logrotate*.conf\" -exec chown root:root {} \;"
fi

cd "$HOME"

# --------------------------------------------------------------------------
# Crontabs
# --------------------------------------------------------------------------
note "Crontabs einrichten" "cyan"

read_colored "cyan" "Möchten Sie die Crontabs von pi und root aktivieren? (j/N): " answer
if [[ "$answer" =~ ^[Jj]$ ]]; then
	run_cmd "crontab $CARAVANPI_DIR/.crontabs/crontab-pi"
	run_cmd "sudo crontab $CARAVANPI_DIR/.crontabs/crontab-root"
fi

cd "$HOME"

# --------------------------------------------------------------------------
# CaravanPi Config Lib initialisieren und damit ggf. defaults konvertieren
# --------------------------------------------------------------------------
note "CaravanPi Library initialisieren und ggf. defaults konvertieren" "cyan"

python3 $CARAVANPI_DIR/installation/caravanPiLibInit.py

cd "$HOME"

# --------------------------------------------------------------------------
# nächste Schritte
# --------------------------------------------------------------------------

next_steps
