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

def main():
    # variable defs
    switch_pin = 17 
    message_success = False
    fail_count = 0              # number of failed attempts
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

            # triggers on switch going high
            if (GPIO.input(switch_pin) == GPIO.HIGH):

                if prev_input != 1:
                    message_success = False
                    prev_input = 1
                    print("Switch Position ON!")

                if !message_success:        # if function returns false, sending was unsuccessful
                    if messenger.send_room_open():
                        print("message sending success, changing LEDs now")
                        message_success = True 
                        fail_count = 0
                        GPIO.output(R_LED,GPIO.LOW)
                        GPIO.output(G_LED,GPIO.HIGH)
                    else:
                        print("UHOH, sending message failed")
                        fail_count++

            # ADD CODE TO CHECK FOR HIGH FAIL COUNT, SEND EMAIL

                time.sleep(0.05)
            else:
            # switch now low
                if prev_input != 0:
                    message_success = False
                    prev_input = 0
                    print("Switch Position OFF!")

                messenger.send_room_closed()
                GPIO.output(R_LED,GPIO.HIGH)
                GPIO.output(G_LED,GPIO.LOW)
                time.sleep(0.05)


    except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
        GPIO.cleanup()

    finally:
        print("clean up")
        GPIO.cleanup()
       

