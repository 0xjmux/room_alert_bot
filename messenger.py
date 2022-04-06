#!/usr/bin/env python3
########################################
# is_ieee_open.py
# jbokor@uci.edu, April 2022
#
# This component of the program handles sending
# alert messages, over discord and email
########################################

import requests
import smtplib, ssl # for sending email
import os
import time
import logging

import _creds_

port = 465  # For SMTP SSL

def main():
    # used for testing all relevant alerting systems
    print("The main of messenger.py should NOT be called in normal operation. ")
    print("Testing messenger functionality: ")

    print("trying to send discord testing message")
    if send_room_alert("test"):
        print("send test message alert succeeded!")

    print("testing send_room_open")
    if send_room_alert("open"):
        print("send room open succeeded!")

    print("testing send_room_closed")
    if send_room_alert("closed"):
        print("send room closed succeeded!")


    print("testing sending email")
    if send_email(1, "SCRIPT TEST; DISREGARD"):
        print("sending email succeeded!")


def send_room_alert(alert_code):
    # set alert_code = whatever json packet we're going to use 
    if alert_code == "open":
        json_data = open_data
    elif alert_code == "closed":
        json_data = closed_data
    elif alert_code == "test":
        json_data = test_message
    elif alert_code == "poweron":
        json_data = poweron_data
    else:
        json_data = interp_error_data

        # this line is the one that throws an error when a connection fails
    try:
        result = requests.post(_creds_.WEBHOOK_URL, json = json_data)
    except ConnectionError as err:
        logging.info("ConnectionError: " + str(err))
        time.sleep(1)       # prevent overloading server with requests
        return False, err
    except Exception as err:
        logging.info("Generic Exception: " + str(err))
        time.sleep(1)       # prevent overloading server with requests
        return False, err


    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.info(err)
        time.sleep(1)       # prevent overloading server with requests
        return False, err
    except Exception as err:
        logging.info("Generic Exception: " + str(err))
        time.sleep(1)       # prevent overloading server with requests
        return False, err
    else:
        logging.info("Success, HTTP code {}.".format(result.status_code))
        return True, "none"

# send error email
def send_email(fail_count, error_desc):
    message = """\
Subject: IEEE Lab Sentinel Bot Error

Number of failed send attempts: {}
Error description: {}
Uptime: {}

This message was sent by an automated system.""".format(fail_count, error_desc, os.popen('uptime -p').read()[:-1])

    try:
        # try sending email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(_creds_.smtp_server, port, context=context) as server:
            server.login(_creds_.sender_email, _creds_.password)
            result = server.sendmail(_creds_.sender_email, _creds_.receiver_email, message)
            logging.info("Server sendmail result: ", end="")
            logging.info(result)
    except Exception as err:
        logging.info("Error sending email! We received: " + str(err))
        return False
    else:
        logging.info("Email sent successfully")
        return True


# JSON data packets for the discord message webhooks
open_data = {
    "content" : "Looks like the IEEE Room is open! :sunglasses:",
    "username" : "IEEE Lab Sentinel"
}

closed_data = {
    "content" : "Looks like the IEEE Room is no longer open :disappointed:",
    "username" : "IEEE Lab Sentinel"
}

poweron_data = {
    "content" : "Powering on!",
    "username" : "IEEE Lab Sentinel"
}

poweroff_data = {
    "content" : "Time for a graceful shutdown :(",
    "username" : "IEEE Lab Sentinel"
}

interp_error_data = {
    "content" : "Looks like we ran into an error and I'm not sure what to send out :(",
    "username" : "IEEE Lab Sentinel"
}

test_message = {
    "content" : "Results of testing the messaging functionality on discord: ",
    "username" : "IEEE Lab Sentinel"
}

if __name__=="__main__":
    main()
