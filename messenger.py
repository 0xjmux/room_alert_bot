#!/usr/bin/env python3
########################################
# is_ieee_open.py
# UCI IEEE, Nov 2021
#
# This component of the program handles sending 
# alert messages, over discord 
########################################

import requests
import smtplib, ssl # for sending email
import os
import time

import _creds_


port = 465  # For SSL

def main():
    # used for testing alerting systems
    print("the main of messenger.py should NOT be called in normal operation")

    print("testing send_room_open")
    if send_room_alert("open"):
        print("send room open succeeded!")

    print("testing send_room_closed")
    if send_room_alert("closed"):
        print("send room closed succeeded!")
    
    print("testing sending email")
    if send_email(1, "script test; disregard"):
        print("sending email succeeded!")


def send_room_alert(alert_code):
    if alert_code == "open":
        # this line is the one that throws an error when a connection fails
        try:
            result = requests.post(_creds_.WEBHOOK_URL, json = open_data)
        except ConnectionError as err:
            print("ConnectionError: " + err)
            time.sleep(1)       # prevent overloading server with requests
            return False, err


# NOT YET UPDATED
    elif alert_code == "closed":
        result = requests.post(_creds_.WEBHOOK_URL, json = closed_data)
    else:
        reason = "invalid alert_code passed to send_room_alert"
        print(reason)
        return False, reason

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return False, err
    else:
        print("Success, HTTP code {}.".format(result.status_code))
        return True

# send error email
def send_email(fail_count, error_desc):
    message = """\
Subject: IEEE Bot Error


Number of failed send attempts: {}
Error description: {}
Uptime: {}

This message was sent by an automated system.""".format(fail_count, error_desc, os.popen('uptime -p').read()[:-1])

    print(message)
#    context = ssl.create_default_context()
#    with smtplib.SMTP_SSL(_creds_.smtp_server, port, context=context) as server:
#        server.login(_creds_.sender_email, _creds_.password)
#        result = server.sendmail(_creds_.sender_email, _creds_.receiver_email, message)
#        print(result)


# JSON data for the discord webhooks
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

if __name__=="__main__":
    main()
