
import random
from datetime import datetime, timedelta

def erstelle_wetterdaten_testdatei():
    start_zeitpunkt = datetime(2022, 1, 1, 0, 0, 8)
    zeilen = []
    
    for tag in range(8):
        temperatur_start = random.uniform(18.0, 22.0)
        luftfeuchtigkeit_start = random.uniform(80.0, 90.0)
        luftdruck_start = random.uniform(1010.0, 1020.0)
        
        temperatur_hoechst = random.uniform(28.0, 32.0)
        luftfeuchtigkeit_hoechst = random.uniform(60.0, 70.0)
        luftdruck_hoechst = random.uniform(1008.0, 1018.0)
        hoechst_zeitpunkt = start_zeitpunkt + timedelta(hours=random.randint(12, 15), minutes=random.randint(0, 59))
        
        tag_ende = datetime(start_zeitpunkt.year, start_zeitpunkt.month, start_zeitpunkt.day, 23, 59, 0)
        dauer_bis_hoechst = (hoechst_zeitpunkt - start_zeitpunkt).total_seconds()
        dauer_nach_hoechst = (tag_ende - hoechst_zeitpunkt).total_seconds()
        
        aktueller_zeitpunkt = start_zeitpunkt
        while aktueller_zeitpunkt <= tag_ende:
            if aktueller_zeitpunkt <= hoechst_zeitpunkt:
                faktor = (aktueller_zeitpunkt - start_zeitpunkt).total_seconds() / dauer_bis_hoechst
            else:
                faktor = 1 - (aktueller_zeitpunkt - hoechst_zeitpunkt).total_seconds() / dauer_nach_hoechst
            
            temperatur = temperatur_start + (temperatur_hoechst - temperatur_start) * faktor
            luftfeuchtigkeit = luftfeuchtigkeit_start + (luftfeuchtigkeit_hoechst - luftfeuchtigkeit_start) * faktor
            luftdruck = luftdruck_start + (luftdruck_hoechst - luftdruck_start) * faktor
            
            zeilen.append(f"BME280-96-119 {aktueller_zeitpunkt.strftime('%Y%m%d%H%M%S')} {temperatur:.1f} {luftdruck:.1f} {luftfeuchtigkeit:.1f}\n")
            
            aktueller_zeitpunkt += timedelta(minutes=1)
        
        start_zeitpunkt += timedelta(days=1)
    
    return zeilen

# Erstellen und Schreiben der Wetterdaten in eine Datei
wetterdaten_zeilen = erstelle_wetterdaten_testdatei()
with open('wetterdaten_testdatei.py', 'w') as datei:
    datei.writelines(wetterdaten_zeilen)
