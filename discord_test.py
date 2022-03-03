#!/usr/bin/env python3
########################################
# is_ieee_open.py
# UCI IEEE, Nov 2021
#
# Python program written for UCI IEEE 
#  to show whether the room is open or not 
#  in the club's Discord server. 
########################################

import discord
import _creds_ # creds is separate file used to store api secrets

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(_creds_.TOKEN)
