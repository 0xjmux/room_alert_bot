#!/usr/bin/env python3
########################################
# is_ieee_open.py
# UCI IEEE, Nov 2021
#
#  Small, quick python program written for 
#  UCI IEEE to show whether the room is open or not 
#  in the club's Discord server. 
########################################

import RPi.GPIO as GPIO
import time
import os
import requests

import messenger
import _creds_ # creds is separate file used to store secrets

# variable defs
switch_pin = 17 
R_LED = 27
G_LED = 22

#initialize gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin,GPIO.IN)
GPIO.setup(R_LED,GPIO.OUT)
GPIO.setup(G_LED,GPIO.OUT)

def main():

    # script initialization block
    print("Script initilized, waiting for switch input")
    LEDs_blink()

    # state tracking
    prev_input = 0
    message_success = False
    fail_count = 0              # number of failed attempts


    # zero out status LEDs 
    GPIO.output(R_LED,GPIO.LOW)
    GPIO.output(G_LED,GPIO.LOW)

    try:
        while True:

            # switch is now "ON". it's backwards, I know. 
            if (GPIO.input(switch_pin) == GPIO.LOW):

                if prev_input != 1:
                    message_success = False
                    prev_input = 1
                    print("Switch Position ON!")

                if not message_success:        # if message was already successfully sent, don't sent another
                    # if function returns false, sending was unsuccessful
                    if messenger.send_room_alert("open"):
                        print("message sending success, turning LEDs to OCCUPIED state now")
                        LEDs_state_occupied()
                        message_success = True 
                        fail_count = 0
                    else:
                        print("UHOH, sending message failed")
                        fail_count += 1


                time.sleep(0.05)
            else:
            # switch now low
                if prev_input != 0:
                    message_success = False
                    prev_input = 0
                    print("Switch Position OFF!")

                if not message_success:        # if message was already successfully sent, don't sent another
                    # if function returns false, sending was unsuccessful
                    if messenger.send_room_alert("closed"):
                        print("message sending success, turning LEDs to VACANT state now")
                        LEDs_state_vacant()
                        message_success = True 
                        fail_count = 0
                    else:
                        print("UHOH, sending message failed")
                        fail_count += 1
                time.sleep(0.05)

            # ADD CODE TO CHECK FOR HIGH FAIL COUNT, SEND EMAIL

    except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
        GPIO.cleanup()

    finally:
        print("clean up")
        GPIO.cleanup()

# turns LEDs into position for switch ON, room OCCUPIED
def LEDs_state_occupied():
    GPIO.output(R_LED,GPIO.LOW)
    GPIO.output(G_LED,GPIO.HIGH)
    time.sleep(0.05)

# turns LEDs into position for switch OFF, room VACANT
def LEDs_state_vacant():
    GPIO.output(R_LED,GPIO.HIGH)
    GPIO.output(G_LED,GPIO.LOW)
    time.sleep(0.05)

# blinks both status LEDs once
def LEDs_blink():
    GPIO.output(R_LED,GPIO.HIGH)
    GPIO.output(G_LED,GPIO.HIGH)
    time.sleep(0.25)

    GPIO.output(R_LED,GPIO.LOW)
    GPIO.output(G_LED,GPIO.LOW)
    time.sleep(0.25)

if __name__=="__main__":
    main()
