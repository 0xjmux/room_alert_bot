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
import requests     # for webhook requests
import json         # used for checking discord status page

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
    start_time = time.time()

    # script initialization block
    print("Script initilized, waiting for switch input")
    LEDs_blink()

    # state tracking
    prev_input = 0
    message_success = False
    fail_count = 0              # number of failed attempts
    last_email_time = 0


    # zero out status LEDs 
    GPIO.output(R_LED,GPIO.LOW)
    GPIO.output(G_LED,GPIO.LOW)

    error_desc = "high fail count"          # default error desc

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
                    a,b = messenger.send_room_alert("open")
                    error_desc = b
                    if a:
                        print("message sending success, turning LEDs to OCCUPIED state now")
                        LEDs_state_occupied()
                        message_success = True 
                        fail_count = 0
                    else:
                        print("UHOH, sending message failed")
                        print("Error: " + str(b))
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

            # if 5 failures occur and email hasn't been sent for 2 hours, send another
            
            if fail_count > 4:
                print("failed again, fail_count: " + str(fail_count))

                if is_discord_broke():
                    error_desc = "Discord status page reporting issues"


                if (time.time() - last_email_time > 7200):
                    print("sending error email message")
                    messenger.send_email(fail_count, error_desc)
                    last_email_time = time.time()

                print("failures over 5, blinking LEDs")
                LEDs_blink()
                time.sleep(0.5)

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

# check if discord is showing issues on their status page
def is_discord_broke():
    try:
        d_json = requests.get("https://discordstatus.com/api/v2/status.json", timeout=5)
    except ConnectionError as err:
        print("ConnectionError: " + err)
        return False, err

    d_dict = json.loads(d_json.content)
    d_status = d_dict['status']['description']
    if not d_status == "All Systems Operational":
        print("Discord status page reporting issues")
        print("Discord status: " + d_status)
        return True

    return False

if __name__=="__main__":
    main()

