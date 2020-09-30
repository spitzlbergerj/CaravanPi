#!/bin/bash

# VARIABLEN - HIER EDITIEREN
BACKUP_PFAD_LOKAL="/home/pi/Backup"
BACKUP_PFAD_CLOUD="/Backup/Geräte/Raspberry/CaravanPi"
BACKUP_ANZAHL="30"
BACKUP_NAME="caravanpi-config-and-scripts"
BACKUP_DIR=${BACKUP_NAME}-$(date +%Y%m%d-%H%M%S)
# echo ${BACKUP_DIR}
# ENDE VARIABLEN

# Directory erstellen
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/backup
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/defaults
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/rclone
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/MM
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/usrlocalbin
mkdir ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/cron

# Sichern Crontabs
crontab -u pi -l > ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/cron/crontab-pi.txt
crontab -u root -l > ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/cron/crontab-root.txt

# Kopieren der relevaten Scripts
echo "Skripts sichern ........"
cp /home/pi/.config/rclone/rclone.conf ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/rclone
cp /home/pi/CaravanPi/defaults/* ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/defaults
cp /home/pi/CaravanPi/backup/backup-scripts.sh ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/backup
cp /home/pi/MagicMirror/css/custom.css ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/MM
cp /home/pi/MagicMirror/config/config.js ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/MM
# cp /usr/local/bin/backup.sh ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/usrlocalbin
cp /usr/local/bin/pishutdown.py ${BACKUP_PFAD_LOKAL}/${BACKUP_DIR}/usrlocalbin

# Alte Sicherungen die nach X neuen Sicherungen entfernen
echo "alte Sicherungen loeschen ....."
pushd ${BACKUP_PFAD_LOKAL}; ls -drt1 ${BACKUP_PFAD_LOKAL}/${BACKUP_NAME}* | head -n -${BACKUP_ANZAHL} | xargs rm -r; popd

#Sync mit Google Drive starten
echo "SYNC starten ............." 
rclone sync CaravanPi:${BACKUP_PFAD_LOKAL} GoogleDriveSJJ:${BACKUP_PFAD_CLOUD}
