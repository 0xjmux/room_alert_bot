#!/usr/bin/env python3
########################################
# hardware_test.py
# UCI IEEE, Nov 2021
#
# Basic program to test hardware operation for 
#  the IEEE room alert bot. 
########################################

import RPi.GPIO as GPIO
import time
import os

# variable defs
switch_pin = 17 
R_LED = 27
G_LED = 22

#initialize gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin,GPIO.IN)
GPIO.setup(R_LED,GPIO.OUT)
GPIO.setup(G_LED,GPIO.OUT)

print("Script initilized, waiting for switch input")
prev_input = 0

try:
    while True:
        input = GPIO.input(17)

        # triggers on switch going high
        if (GPIO.input(switch_pin) == GPIO.HIGH):

            if prev_input != 1:
                prev_input = 1
                print("Switch ON!")

            GPIO.output(R_LED,GPIO.HIGH)
            GPIO.output(G_LED,GPIO.HIGH)
            time.sleep(0.05)
        else:
            if prev_input != 0:
                prev_input = 0
                print("Switch OFF!")
            GPIO.output(R_LED,GPIO.LOW)
            GPIO.output(G_LED,GPIO.LOW)
            time.sleep(0.05)


except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()

finally:
    print("clean up")
    GPIO.cleanup()
