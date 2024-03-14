#!/bin/bash
# --------------------------------------------------
# Backup Skript fuer Raspberrys mit Config Dateien
# (c) Josef Spitzlberger, 03.12.2022
#
# 2. Skript fuer Sondersituationen in denen es nicht ausreicht, Dateien anzugeben
# --------------------------------------------------

# --------------------------------------------------
# Parameter uebernehmen
# --------------------------------------------------

BACKUP_DIR=$1

# --------------------------------------------------
# als 2. Skript melden
# --------------------------------------------------
echo "----------------------------------------------------"
echo " 2. Skript gestartet"
echo "----------------------------------------------------"

# --------------------------------------------------
# Sonderkommandos zum Sichern
# --------------------------------------------------

# --------------------------------------------------
# MariaDB
# --------------------------------------------------

# Maria DB

#
# Kommandos
MYSQL_CMD=/usr/bin/mysql  
MYSQL_DMP=/usr/bin/mysqldump  

# Backup
#
echo
echo "Starte Datenbanksicherung ..."
mkdir -p "$BACKUP_DIR/MariaDB"
databases=`$MYSQL_CMD -e "SHOW DATABASES;" | grep -Ev "(Database|information_schema|performance_schema)"`
 
for db in $databases; do
  echo "Sichere Datenbank $db ..."
  $MYSQL_DMP --no-data --databases "$db" > "$BACKUP_DIR/MariaDB/$db-schema.sql"
  $MYSQL_DMP --force --opt --databases "$db" | gzip > "$BACKUP_DIR/MariaDB/$db.gz"
done

# --------------------------------------------------
# 2. Skript beenden
# --------------------------------------------------
echo "----------------------------------------------------"
echo " 2. Skript abgeschlossen"
echo "----------------------------------------------------"

exit 0
