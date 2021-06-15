# Bestellung der Platine bei JLCPCP.com

Hier finden Sie alle Files zur Bestellung der Platine sowie eine Schritt für Schritt Anleitung des Bestellvorgangs

## Website JLCPCB.com
Rufen Sie die Website https://jlcpcb.com/ auf. Erstellen Sie dort einen Account und klicken Sie anschließend auf "order now"

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-00.png)  

## Gerber File hochladen
Laden Sie anschließend das Gerber File als zip-File über den entsprechenden Button hoch. Das Gerber File wird daraufhin verarbeitet und sollte etwa so erkannt werden:

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-001.png)  

## Platinen Details angeben
Füllen Sie das Formular wie folgt aus

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-02.jpg)  

Im Feld **PCB Qty** geben Sie die Anzahl der Platinen an, die erstellt werden soll. Die Mindestmenge beträgt 5 Stück. In der Regel habe ich Platinen vorrätig, so dass Sie auch einzelne Platinen über mich beziehen können. Dennoch kosten die von JLCPCB gefertigen Platinen im *5-er-Pack inkl. Bestückung* in der Regel noch weniger als *eine* in Europa gefertigte bestückte Platine.

Die meisten anderen Werte können in der Default Einstellung bleiben. Lediglikch **Confirm Production File** und **Remove Order Number** habe ich umgesetzt. letzteres kostet ein geringes Entgelt.

## Bauteil Bestückung (SMT Assembly)
Wählen Sie nun die Bauteilbestückung, also SMT Assembly, aus. Sie werden dann nach der zu bestückende Seite der Platine gefragt. Es ist die Vorderseite (top side).

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-01.jpg)  

Geben Sie auch hier die Anzahl der zu bestückenden Platinen ein. Sie können natürlich max. die Gesamtanzahl eingeben (vorausgewählt). geben Sie heir weniger an, werden Ihnen bestückte und unbestückte Platinen geliefert.

Schließlich drücken Sie den "Confirm" Button.

## BOM und CPL File hochladen
**ACHTUNG**   
**Bitte korrigieren Sie vor dem Hochladen des BOM Files ggf. die Widerstandswerte für die LED Widerstände, falls Sie andere LEDs verwenden als ich.**   
**Es handelt sich um die Widerstände R1 - R12, R15 - R23. Ermitteln Sie aus den Schaltplänen, welche Widerstände welche Werte haben müssen.**   
**R1,R4,R7,R10,R15,R18,R21 bedienen die Farbe x**   
**R2,R5,R8,R11,R16,R19,R22 bedienen die Farbe y**   
**R3,R6,R9,R12,R17,R20,R23 bedienen die Farbe z**   
Die Bauteile-Datenbank finden Sie [hier](https://jlcpcb.com/parts). Bitte achten Sie darauf, dass Sie bei den Widerständen ein Bauteil des Typs 1206 (Package) wählen, damit die Abmessungen zu den Lötpads passen.

Laden Sie dann die beiden Files BOM und CPL hoch, indem Sie über die beiden Buttons das jeweilige File auswählen und dann den Button "Next" klicken.
![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-021.png)

Nach der Verarbeitung der beiden Files werden Ihnen die gefundenen Bauteile angezeigt.
![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-03.jpg)  

Alle Teile, die abgehackt sind, werden auf die Platine aufgebracht werden. Teile, die nicht lieferbar sind, werden als "Inventory shortage" angezeigt und nicht verlötet werden.

Bestätigen Sie anschließend diese Teileliste.

## Vorschau Bauteilbestückung
Nun sollte eine Vorschau angezeigt werden:
![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-04.jpg)  

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-05.jpg)  

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-06.jpg)  

## weitere benötigte Bauteile
JLC bestückt die Platine mit den vorrätigen Teilen. Alle nicht vorrätigen Teile müssen Sie nach dem Empfang der Platine selbst auflöten.

Zudem sind folgende weitere Bauteile pro Platine vonnöten:

- WAGO Platinen Klemmen (können zusammengesteckt werden 3x 4-Port = 1x 12-Port)
  -  2 x 3-Port-Klemmen
  - 11 x 4-Port-Klemmen
  -  2 x 8-Port-Klemmen
  -  1 x 16-Port-Klemme
- Steckleisten 2-reihig oder Wannensteckerbuchsen
  - 1 x 40-Port (Raspberry Pi)
  - 1 x 10-Port (Deckel)
- I2C Extender Baustein
- HX711 Breakout Platine
