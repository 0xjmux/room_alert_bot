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
GPIO.setup(buttonPin,GPIO.IN)
GPIO.setup(R_LED,GPIO.OUT)
GPIO.setup(G_LED,GPIO.OUT)

prev_input = 0

client = discord.Client()

#@client.event
#async def on_ready():
#    print('We have logged in as {0.user}'.format(client))


try:
    while True:
        #assuming the script to call is long enough we can ignore bouncing
        if (GPIO.input(buttonPin)):
                #take a reading
                input = GPIO.input(17)
                #if the last reading was low and this one high, print
                print(input)
                if (prev_input != input):
                        print("Switch changed")
                GPIO.output(R_LED,GPIO.HIGH)
                GPIO.output(G_LED,GPIO.HIGH)
                #update previous input
                prev_input = input
                #slight pause to debounce
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
