# Bestellung der Platine bei JLCPCB.com

Hier finden Sie eine Schritt für Schritt Anleitung des Bestellvorgangs. Die benötigten Files holen Sie bitte aus dem jewieligen Versionsverzeichnis (derzeit V3 oder V4)

## Website JLCPCB.com
Rufen Sie die Website https://jlcpcb.com/ auf. Erstellen Sie dort einen Account und klicken Sie anschließend auf "order now"

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-00.png)  

## Gerber File hochladen
Laden Sie anschließend das Gerber File aus dem Versionsverzeichnis als zip-File über den entsprechenden Button hoch. Das Gerber File wird daraufhin verarbeitet und sollte etwa so erkannt werden:

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
**R1,R4,R7,R10,R15,R18,R21 bedienen die Farbe GRÜN**   
**R2,R5,R8,R11,R16,R19,R22 bedienen die Farbe BLAU**   
**R3,R6,R9,R12,R17,R20,R23 bedienen die Farbe ROT**   
Die Bauteile-Datenbank finden Sie [hier](https://jlcpcb.com/parts). Bitte achten Sie darauf, dass Sie bei den Widerständen ein Bauteil des Typs 1206 (Package) wählen, damit die Abmessungen zu den Lötpads passen.

Laden Sie dann die beiden Files BOM und CPL hoch, indem Sie über die beiden Buttons das jeweilige File auswählen und dann den Button "Next" klicken.
![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-021.png)

Nach der Verarbeitung der beiden Files werden Ihnen die gefundenen Bauteile angezeigt.
![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-03.jpg)  

Alle Teile, die abgehackt sind, werden auf die Platine aufgebracht werden. Teile, die nicht lieferbar sind, werden als "Inventory shortage" angezeigt und nicht verlötet werden.

Bestätigen Sie anschließend diese Teileliste.

## Vorschau Bauteilbestückung
Nun sollte eine Vorschau angezeigt werden:
![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-04n.jpg)  

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-05n.jpg)  

![CaravanPi Platine JLCPCB Schritt 1](https://github.com/spitzlbergerj/CaravanPi/raw/master/circuit-board/jlcpcb.com/JLCPCB-Platinenbestellung-06.jpg)  

**Achtung**  
**Bitte achten Sie auf den Kondensator C1. Dieser muss den Pluspol auf der rechten Seite haben. Der rote Strich sollte also rechts sein, wie auf den oberen beiden Bildern.**  
**Das letzte Bild, also die untere Hälfte, zeigt den Kondensator noch falsch herum positioniert!**  

## weitere benötigte Bauteile
JLC bestückt die Platine mit den vorrätigen Teilen. Alle nicht vorrätigen Teile müssen Sie nach dem Empfang der Platine selbst auflöten.

Zudem sind folgende weitere Bauteile pro Platine vonnöten:

- [WAGO Platinen Klemmen](https://www.reichelt.de/klemmleiste-rm-2-54-ffnungshebel-4-polig-wago-233-504-p31675.html?&nbc=1) (können zusammengesteckt werden 3x 4-Port = 1x 12-Port)
  -  2 x 3-Port-Klemmen
  - 11 x 4-Port-Klemmen
  -  2 x 8-Port-Klemmen
  -  1 x 16-Port-Klemme
- Steckleisten 2-reihig oder Wannensteckerbuchsen
  - 1 x [40-Port](https://www.reichelt.de/wannenstecker-40-polig-gerade-wsl-40g-p22834.html?&trstct=pos_2&nbc=1) (Raspberry Pi)
  - 1 x [10-Port](https://www.reichelt.de/wannenstecker-10-polig-gerade-wsl-10g-p22816.html?&trstct=pos_0&nbc=1) (Deckel)
- I2C Extender Baustein P82B715, z.B. [hier](https://www.ebay.de/itm/114730136735)
- HX711 Breakout Platine, z.B. [hier](https://smile.amazon.de/gp/product/B07MY3DCCM)
