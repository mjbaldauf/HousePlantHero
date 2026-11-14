from gpiozero import LED
from time import sleep

# GPIO pin assignments
RED_PIN = 26
YELLOW_PIN = 19
GREEN_PIN = 13

# Initialize LEDs
red = LED(RED_PIN)
yellow = LED(YELLOW_PIN)
green = LED(GREEN_PIN)


def all_off():
    red.off()
    yellow.off()
    green.off()


def red_light():
    all_off()
    red.on()


def yellow_light():
    all_off()
    yellow.on()


def green_light():
    all_off()
    green.on()

