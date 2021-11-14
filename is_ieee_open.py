#!/usr/bin/env python3
########################################
# is_ieee_open.py
# UCI IEEE, Nov 2021
#
# Python program written for UCI IEEE 
#  to show whether the room is open or not 
#  in the club's Discord server. 
########################################

import RPi.GPIO as GPIO
import time
import os
import discord
import _creds_ # creds is separate file used to store api secrets

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

client = discord.Client()

#@client.event
#async def on_ready():
#    print('We have logged in as {0.user}'.format(client))

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
   



#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')
#
#client.run(_creds_.TOKEN)
