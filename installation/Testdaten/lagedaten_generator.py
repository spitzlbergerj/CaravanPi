
from datetime import datetime, timedelta

def korrigierte_berechnung(differenz_deichsel, differenz_zentral_rechts=0):
    # Berechnet die Positionen basierend auf der Differenz an der Deichsel und zentral rechts
    differenz_hinten_links = -abs(differenz_deichsel) / 2 if differenz_deichsel < 0 else abs(differenz_deichsel) / 2
    differenz_hinten_rechts = differenz_hinten_links
    differenz_vorne_links = differenz_deichsel * 0.75
    differenz_vorne_rechts = differenz_vorne_links
    differenz_zentral_links = -differenz_zentral_rechts
    return [differenz_hinten_links, differenz_hinten_rechts, differenz_vorne_links, differenz_vorne_rechts, differenz_zentral_links, differenz_zentral_rechts, differenz_deichsel]

def erstelle_testdatei(start_deichsel, start_zentral_rechts, datei_pfad):
    testdaten = []
    start_zeit = datetime(2022, 1, 1, 0, 0, 0)
    differenz_deichsel = start_deichsel
    differenz_zentral_rechts = start_zentral_rechts

    for sekunde in range(300):  # Angenommene Dauer für den Test
        zeitstempel = (start_zeit + timedelta(seconds=sekunde)).strftime('%Y%m%d%H%M%S')
        werte = korrigierte_berechnung(differenz_deichsel, differenz_zentral_rechts)
        testdaten.append([zeitstempel] + [round(wert, 2) for wert in werte])

        # Logik zur Anpassung der Differenzen könnte hier hinzugefügt werden, falls nötig

    with open(datei_pfad, 'w') as file:
        for eintrag in testdaten:
            file.write(' '.join(map(str, eintrag)) + '\n')

# Beispielaufruf der Funktion
# erstelle_testdatei(150, 0, 'testdatei_deichsel_150_hoch.txt')
