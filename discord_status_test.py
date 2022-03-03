#!/usr/bin/env python3

import json
import requests

# check if discord is showing issues on their status page
d_json = requests.get("https://discordstatus.com/api/v2/status.json")
d_dict = json.loads(d_json.content)
d_status = d_dict['status']['description']
if not d_status == "All Systems Operational":
    print("uhoh, discord having issues")

print("discord status: " + d_status)

