#!/usr/bin/env python3
########################################
# is_ieee_open.py
# jbokor@uci.edu, April 2022
#
#  "Small", "quick" python program written for
#  UCI IEEE to show whether the room is open or not
#  in the club's Discord server.
########################################

import RPi.GPIO as GPIO
import time
import os
import requests     # for webhook requests
import json         # used for checking discord status page
import logging      # gotta keep them logs

# companion files
import messenger
import _creds_ # creds is a separate file used to store secrets

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

    # setup logging
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='/var/log/room_alert_bot/room_bot.log', level=logging.INFO)


    # script initialization block
    logging.info("Script initilized, waiting for switch input")
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

        LEDs_blink()
        LEDs_blink()

        # this will run until the "powering up" message is sent successfully
        while not message_success:
            a,b = messenger.send_room_alert("poweron")
            error_desc = b
            if a:
                logging.info("sent initial message to discord, starting primary loop")
                message_success = True
                fail_count = 0
            else:
                logging.info("Sending initial message failed")
                logging.info("Initial message sending error: " + str(b))
                fail_count += 1
                time.sleep(1)

            if fail_count > 5:
                logging.info("failed again, blinking LEDs. Fail_count: " + str(fail_count))
                LEDs_blink()
                time.sleep(2)

            # things aren't going well. lets slow our roll
            if fail_count > 30:
                logging.info("Failures over 30, slowing down retries. Blinking LEDs. Fail_count: " + str(fail_count))
                LEDs_blink()
                time.sleep(20)

        # reset message success value and start the main loop
        message_success = False
        while True:

            # switch is now "ON". it's backwards, I know. 
            if (GPIO.input(switch_pin) == GPIO.LOW):

                if prev_input != 1:
                    message_success = False
                    prev_input = 1
                    logging.info("Switch Position ON!")

                if not message_success:        # if message was already successfully sent, don't sent another
                    # if function returns false, sending was unsuccessful
                    a,b = messenger.send_room_alert("open")
                    error_desc = b
                    if a:
                        logging.info("message sending success, turning LEDs to OCCUPIED state now")
                        LEDs_state_occupied()
                        message_success = True
                        fail_count = 0
                    else:
                        logging.info("UHOH, sending message failed")
                        logging.info("Error: " + str(b))
                        fail_count += 1
                        time.sleep(2)

                time.sleep(0.05)

            else:
            # switch now low
                if prev_input != 0:
                    message_success = False
                    prev_input = 0
                    logging.info("Switch Position OFF!")

                if not message_success:        # if message was already successfully sent, don't sent another
                    # if function returns false, sending was unsuccessful
                    a,b = messenger.send_room_alert("closed")
                    error_desc = b
                    if a:
                        logging.info("message sending success, turning LEDs to VACANT state now")
                        LEDs_state_vacant()
                        message_success = True
                        fail_count = 0
                    else:
                        logging.info("UHOH, sending message failed")
                        logging.info("Error: " + str(b))
                        fail_count += 1
                        time.sleep(2)

                time.sleep(0.05)

            # if 5 failures occur and email hasn't been sent for 4 hours, send another
            
            # things aren't going well. lets slow our roll
            if fail_count > 30:
                logging.info("Failures over 30, slowing down retries. Blinking LEDs. Fail_count: " + str(fail_count))
                LEDs_blink()
                time.sleep(20)

            elif fail_count > 4:
                logging.info("Failures over 5, blinking LEDs. " + str(fail_count))

                LEDs_blink()

            if fail_count > 4:
                if is_discord_broke():
                    error_desc = "Discord status page reporting issues"

                LEDs_blink()

                if (time.time() - last_email_time > 14400):
                    logging.info("sending error email message")
                    messenger.send_email(fail_count, error_desc)
                    last_email_time = time.time()

                LEDs_blink()

                time.sleep(0.5)

    except Exception as err:
        logging.info("Caught a big exception in the wild! Generic Exception: " + str(err))

    except KeyboardInterrupt as err:
        messenger.send_room_alert("poweroff")
        quit()


    finally:
        logging.info("clean up")
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
        logging.info("ConnectionError: " + str(err))
        time.sleep(1)
        return False, err
    except Exception as err:
        logging.info("Generic Exception: " + str(err))
        time.sleep(1)
        return False, err

    d_dict = json.loads(d_json.content)
    d_status = d_dict['status']['description']
    if not d_status == "All Systems Operational":
        logging.info("Discord status page reporting issues")
        logging.info("Discord status: " + d_status)
        return True

    return False

if __name__=="__main__":
    main()

