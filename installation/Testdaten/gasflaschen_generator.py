
import random
from datetime import datetime, timedelta

def erstelle_angepasste_datei_mit_startwert(startwert):
    start_zeitpunkt = datetime(2022, 1, 1, 0, 0, 0)
    gesamtmenge = 6000
    aktueller_inhalt = startwert
    zeilen = []

    for tag in range(8):
        start_reduktion = datetime(start_zeitpunkt.year, start_zeitpunkt.month, start_zeitpunkt.day + tag, 
                                   random.randint(17, 18), random.randint(0, 59), 0)
        dauer_reduktion = timedelta(minutes=random.randint(30, 60))
        ende_reduktion = start_reduktion + dauer_reduktion
        tagesreduktion = random.randint(100, 300)
        reduktion_pro_minute = tagesreduktion / dauer_reduktion.seconds * 60
        
        aktueller_zeitpunkt = start_zeitpunkt + timedelta(days=tag)
        ende_des_tages = datetime(aktueller_zeitpunkt.year, aktueller_zeitpunkt.month, aktueller_zeitpunkt.day, 23, 59, 0)

        while aktueller_zeitpunkt <= ende_des_tages:
            if start_reduktion <= aktueller_zeitpunkt <= ende_reduktion:
                aktueller_inhalt -= reduktion_pro_minute
                if aktueller_inhalt < 15:
                    aktueller_inhalt = 15
            fuellgrad = (aktueller_inhalt / gesamtmenge) * 100
            
            zeitstempel = aktueller_zeitpunkt.strftime("%Y%m%d%H%M%S")
            zeile = f"gasScale1 {zeitstempel} {aktueller_inhalt:.2f} {fuellgrad:.2f}\n"
            zeilen.append(zeile)
            
            aktueller_zeitpunkt += timedelta(minutes=1)

        start_zeitpunkt += timedelta(days=1)
    
    return zeilen

# Anwendung der Funktion mit einem Startwert von 4632 und Speicherung der Ergebnisse in einer Datei
startwert = 4632
angepasste_zeilen_mit_startwert = erstelle_angepasste_datei_mit_startwert(startwert)
with open('gasflaschen_werte_generator.py', 'w') as datei:
    for zeile in angepasste_zeilen_mit_startwert:
        datei.write(zeile)
