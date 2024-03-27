# -----------------------------------------------------------------
# Spannungsteiler berechnen für Standarwiderstände
#
# Code wurde von ChatGPT erzeugt auf einen entsprechenden Prompt hin
#
# -----------------------------------------------------------------

def konvertiere_eingabe(eingabe):
    return float(eingabe.replace(',', '.'))

def finde_top_spannungsteiler(widerstaende, Vin, Vout_ziel, top_n=5):
    kombinationen = []

    for R1 in widerstaende:
        for R2 in widerstaende:
            Vout = Vin * (R2 / (R1 + R2))
            differenz = abs(Vout_ziel - Vout)  # Absolutwert der Differenz, um Nähe zur Zielspannung zu messen
            if Vout <= Vout_ziel:  # Vout darf nicht über Vout_ziel sein
                kombinationen.append((R1, R2, Vout, differenz))

    # Sortiere die Kombinationen basierend auf der Nähe zu Vout_ziel und wähle die top_n Kombinationen
    kombinationen = sorted(kombinationen, key=lambda x: x[3])[:top_n]

    beste_kombinationen = []
    for R1, R2, Vout, _ in kombinationen:
        I = Vin / (R1 + R2)  # Stromstärke in A
        P_R1 = (I ** 2) * R1  # Leistung an R1 in W
        P_R2 = (I ** 2) * R2  # Leistung an R2 in W
        beste_kombinationen.append((R1, R2, Vout, I, P_R1, P_R2))

    return beste_kombinationen

# Vorhandene Widerstände in Ohm
widerstaende = [10, 20, 47, 82, 100, 150, 220, 470, 560, 1000, 2200, 4700, 10000, 22000, 47000, 100000, 220000, 470000, 1000000]

# Benutzereingaben mit Konvertierung
Vin_eingabe = input("Bitte geben Sie die Eingangsspannung (Vin) ein: ")
Vin = konvertiere_eingabe(Vin_eingabe)

Vout_ziel_eingabe = input("Bitte geben Sie die gewünschte Ausgangsspannung (Vout) ein: ")
Vout_ziel = konvertiere_eingabe(Vout_ziel_eingabe)

# Beste Kombinationen finden
beste_kombinationen = finde_top_spannungsteiler(widerstaende, Vin, Vout_ziel, 5)

if beste_kombinationen:
    print("Top 5 Kombinationen (R1, R2, Vout, Stromstärke I):")
    for R1, R2, Vout, I, P_R1, P_R2 in beste_kombinationen:
        print(f"R1 = {R1} Ohm, R2 = {R2} Ohm, Vout = {Vout:.2f} V, I = {(I * 1000):.2f} mA, P_R1 = {(P_R1 * 1000):.4f} mW, P_R2 = {(P_R2 * 1000):.4f} mW")
else:
    print("Keine geeignete Kombination gefunden.")
