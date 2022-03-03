#!/usr/bin/env python3
########################################
# is_ieee_open.py
# UCI IEEE, Nov 2021
#
# This component of the program handles sending 
# alert messages, over discord 
########################################

import requests
import _creds_

def main():
    # used for testing alerting systems
    print("the main of messenger.py should NOT be called in normal operation")

    print("testing send_room_open")
    if send_room_alert("open"):
        print("send room open succeeded!")

    print("testing send_room_closed")
    if send_room_alert("closed"):
        print("send room closed succeeded!")
    


def send_room_alert(alert_code):
    if alert_code == "open":
        result = requests.post(_creds_.WEBHOOK_URL, json = open_data)
    elif alert_code == "closed":
        result = requests.post(_creds_.WEBHOOK_URL, json = closed_data)
    else:
        print("invalid alert_code passed to send_room_alert");
        return False

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return False
    else:
        print("Success, HTTP code {}.".format(result.status_code))
        return True


# JSON data for the discord webhooks
open_data = {
    "content" : "Looks like the IEEE Room is open! :sunglasses:",
    "username" : "IEEE Lab Sentinel"
}

closed_data = {
    "content" : "Looks like the IEEE Room is no longer open :disappointed:",
    "username" : "IEEE Lab Sentinel"
}


if __name__=="__main__":
    main()