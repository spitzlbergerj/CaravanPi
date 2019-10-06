# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

## position calculation (Technical details see below)

Normally you align a caravan by measuring the position with a spirit level. The spirit level is placed once in the longitudinal direction and once in the transverse direction, e.g. on the floor of the caravan. The accuracy of this usual method depends on the accuracy of the spirit level and the quality of the floor. Everyone knows the situation where a caravan that has been levelled over the floor no longer appears horizontal when the spirit level is placed on the table or kitchen unit.

Therefore the measuring method of the CaravanPi was provided with several adjustable tolerance values. You must determine yourself which tolerance values are the correct ones for your caravan. I give here some recommendations.

A very good to good (= expensive) spirit level normally measures with an accuracy of approx. 1mm / meter. Together with the reading accuracy that can be achieved in the situation of a holiday starting hopefully immediately and the fact that the caravan floor is generally not level, a deviation of approx. 2 - 3 cm between the corners of the caravan and the horizontal appears to be sufficiently accurate.





## Technical details

The ADXL345 3-axis acceleration sensor used is capable of detecting even vibrations of a refrigerator as a change in position. According to technical specification it has an accuracy of approx. 0.0039 g (acceleration due to gravity). This corresponds to a measurable angle of approx. 0.23 degrees. With a caravan of 7 meters long and 2.3 meters wide and a positioning of the sensor at 2/3 of the length and 2/3 of the width respectively, the result is a measurable deviation from the length of approx. 18 mm and in the width of approx. 6 mm. 
 
<img src="https://github.com/spitzlbergerj/CaravanPi/raw/master/images/WindschiefeFlaecheWinkelBerechnung.jpg">
