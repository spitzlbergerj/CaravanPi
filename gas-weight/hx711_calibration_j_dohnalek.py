"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

######################################################################
README:

This version runs in python 3.x. It will first prompt the user to 
empty the scale. Then prompt user to place an item with a known weight
on the scale and input weight as INT. 

The offset and scale will be adjusted accordingly and displayed for
convenience.

The user can choose to [0] exit, [1] recalibrate, or [2] display the 
current offset and scale values and weigh a new item to test the accuracy
of the offset and scale values!
#######################################################################
"""

import RPi.GPIO as GPIO
import time
import sys

# -------------------------------------------------------------------------------
# libraries from CaravanPi 
# -------------------------------------------------------------------------------
sys.path.append('/home/pi/CaravanPi/.lib')
from hx711_j_dohnalek import HX711

# Force Python 3 ###########################################################

if sys.version_info[0] != 3:
    raise Exception("Python 3 is required.")

############################################################################

# Make sure you correct these to the correct pins for DOUT and SCK.
# gain is set to 128 as default, change as needed.
hx = HX711(23, 24, gain=128)


def cleanAndExit():
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def setup():
    """
    code run once
    """
    print("Initializing.\n Please ensure that the scale is empty.")
    scale_ready = False
    while not scale_ready:
        if (GPIO.input(hx.DOUT) == 0):
            scale_ready = False
        if (GPIO.input(hx.DOUT) == 1):
            print("Initialization complete!")
            scale_ready = True


def calibrate():
    readyCheck = input("Remove any items from scale. Press any key when ready.")
    offset = hx.read_average()
    print("Value at zero (offset): {}".format(offset))
    hx.set_offset(offset)
    print("Please place an item of known weight on the scale.")

    readyCheck = input("Press any key to continue when ready.")
    measured_weight = (hx.read_average()-hx.get_offset())
    item_weight = input("Please enter the item's weight in grams.\n>")
    scale = int(measured_weight)/int(item_weight)
    hx.set_scale(scale)
    print("Scale adjusted for grams: {}".format(scale))


def loop():
    """
    code run continuously
    """
    try:
        prompt_handled = False
        while not prompt_handled:
            val = hx.get_grams()
            hx.power_down()
            time.sleep(.001)
            hx.power_up()
            print("Item weighs {} grams.\n".format(val))
            choice = input("Please choose:\n"
                           "[1] Recalibrate.\n"
                           "[2] Display offset and scale and weigh an item!\n"
                           "[0] Clean and exit.\n>")
            if choice == "1":
                calibrate()
            elif choice == "2":
                print("\nOffset: {}\nScale: {}".format(hx.get_offset(), hx.get_scale()))
            elif choice == "0":
                prompt_handled = True
                cleanAndExit()
            else:
                print("Invalid selection.\n")
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


##################################

if __name__ == "__main__":

    setup()
    calibrate()
    while True:
        loop()