from gpiozero import Button
from time import sleep

button = Button(6, pull_up=False)

while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")
    sleep(0.5)