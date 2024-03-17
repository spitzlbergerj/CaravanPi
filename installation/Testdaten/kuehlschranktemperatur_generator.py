
import random
from datetime import datetime, timedelta

def generiere_kuehlschrank_temperatur_verlauf(start_zeitpunkt, tage=8, sensor_id=""):
    außen_temperatur_start = 18.0
    außen_temperatur_hoechst = 32.0
    temperatur_verlauf = []

    for tag in range(tage):
        höchst_temperatur_zeitpunkt = start_zeitpunkt + timedelta(days=tag, hours=12)

        for minute in range(24 * 60):
            aktueller_zeitpunkt = start_zeitpunkt + timedelta(days=tag, minutes=minute)
            if aktueller_zeitpunkt.time() < höchst_temperatur_zeitpunkt.time():
                faktor = (aktueller_zeitpunkt - start_zeitpunkt).seconds / (12 * 60 * 60)
            else:
                faktor = (start_zeitpunkt + timedelta(days=tag+1) - aktueller_zeitpunkt).seconds / (12 * 60 * 60)
            
            aktuelle_temperatur = außen_temperatur_start + (außen_temperatur_hoechst - außen_temperatur_start) * faktor
            # Noch stärkere Schwankungen der Innenraumtemperaturen
            gefrierfach_temp = max(-7, min(-1, -4 + (aktuelle_temperatur - 18) * 0.3))
            kühlfach_temp = max(1, min(9, 5 + (aktuelle_temperatur - 18) * 0.3))
            getränkefach_temp = max(8, min(14, 11 + (aktuelle_temperatur - 18) * 0.3))

            if sensor_id == "gefrierfach":
                temperatur_verlauf.append(f"28-01203392085f {aktueller_zeitpunkt.strftime('%Y%m%d%H%M%S')} {gefrierfach_temp:.2f}\n")
            elif sensor_id == "kühlfach":
                temperatur_verlauf.append(f"28-012033251e15 {aktueller_zeitpunkt.strftime('%Y%m%d%H%M%S')} {kühlfach_temp:.2f}\n")
            elif sensor_id == "getränkefach":
                temperatur_verlauf.append(f"28-012032d4dd5a {aktueller_zeitpunkt.strftime('%Y%m%d%H%M%S')} {getränkefach_temp:.2f}\n")

    return temperatur_verlauf

start_zeitpunkt = datetime(2022, 1, 1, 0, 0, 24)

gefrierfach_temperatur_verlauf = generiere_kuehlschrank_temperatur_verlauf(start_zeitpunkt, 8, "gefrierfach")
kühlfach_temperatur_verlauf = generiere_kuehlschrank_temperatur_verlauf(start_zeitpunkt, 8, "kühlfach")
getränkefach_temperatur_verlauf = generiere_kuehlschrank_temperatur_verlauf(start_zeitpunkt, 8, "getränkefach")

with open('stark_angepasster_gefrierfach_temperatur_verlauf.txt', 'w') as file:
    file.writelines(gefrierfach_temperatur_verlauf)

with open('stark_angepasster_kühlfach_temperatur_verlauf.txt', 'w') as file:
    file.writelines(kühlfach_temperatur_verlauf)

with open('stark_angepasster_getränkefach_temperatur_verlauf.txt', 'w') as file:
    file.writelines(getränkefach_temperatur_verlauf)
