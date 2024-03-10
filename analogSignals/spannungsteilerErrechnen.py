# -----------------------------------------------------------------
# Spannungsteiler berechnen für Standarwiderstände
#
# Code wurde von ChatGPT erzeugt auf einen entsprechenden Prompt hin
#
# -----------------------------------------------------------------

def finde_spannungsteiler(widerstaende, Vin, Vout_ziel):
    beste_differenz = Vin  # Startwert für die kleinste gefundene Differenz, unrealistisch hoch
    beste_kombination = None

    for R1 in widerstaende:
        for R2 in widerstaende:
            Vout = Vin * (R2 / (R1 + R2))
            differenz = Vout_ziel - Vout
            if 0 < differenz < beste_differenz:  # Vout soll knapp unter Vout_ziel sein
                beste_differenz = differenz
                beste_kombination = (R1, R2, Vout)

    return beste_kombination

# Vorhandene Widerstände in Ohm
widerstaende = [10, 20, 47, 82, 100, 150, 220, 470, 560, 1000, 2200, 4700, 10000, 22000, 47000, 100000, 220000, 470000, 1000000]

# Benutzereingaben
Vin = float(input("Bitte geben Sie die Eingangsspannung (Vin) ein: "))
Vout_ziel = float(input("Bitte geben Sie die gewünschte Ausgangsspannung (Vout) ein: "))

# Beste Kombination finden
beste_kombination = finde_spannungsteiler(widerstaende, Vin, Vout_ziel)

if beste_kombination:
    R1, R2, Vout = beste_kombination
    print(f" ")
    print(f" ")
    print(f"an vorhandenen Widerständen wurden dabei angenommen: {widerstaende}")
    print(f" ")
    print(f" ")

    print(f"Beste Kombination: R1 = {R1} Ohm")
    print(f"                   R2 = {R2} Ohm")
    print(f"                   Eingangsspannung      = {Vin:.2f} V")
    print(f"                   erw. Ausgangsspannung = {Vout:.2f} V")
    print(f" ")
    print(f"Schema:            {Vin:.2f} V ----- {R1} Ohm  ----- {Vout:.2f} V ----- {R2} Ohm ----- GND")
else:
    print("Keine geeignete Kombination gefunden.")
