# CaravanPi
System for measuring and displaying various values in caravans and motor homes, including climate values, filling levels and levelling data. Magic Mirror is used for presentation.

# defaults

A whole series of sensors must be adjusted before use. It is therefore almost impossible to mount the 3-axis position sensor absolutely horizontally. The compensation values are stored in files in this directory. In addition, values such as the empty weight of the gas cylinder are stored in this directory.

## Correction values position sensor (adjustmentPosition)

- adjustment X
  - X value, if caravan is in horizontal position
- adjustment Y
  - Y value, if caravan is in horizontal position
- adjustment Z
  - Z value, if caravan is in horizontal position
- tolerance X
  - deviation in X direction, which is still considered horizontal 
- tolerance Y
  - deviation in Y direction, which is still considered horizontal
- approximation X
  - at which deviation from the horizontal the LEDs should flash
- approximation Y
  - at which deviation from the horizontal the LEDs should flash
- distance right
  - distance of the sensor from the right side
- distance front
  - distance of the sensor from the front side
- distance axis
  - distance of the sensor from the axis in longitudinal direction

## dimensions of the carvan or motor home (dimensions)

- length over all
  - length of the caravan over all 
- width
  - width of the caravan over all
- lenght body
  - legth of the body of the caravan without drawbar
  
## gas scale and gas cylinder (gasScaleDefaults1)

- tare
  - value from gas scale without a gas cylinder 
- empty weight
  - weight of the empty gas cylinder
- full weight
  - weight of the full gas cylinder
