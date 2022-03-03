# room_alert_bot
Discord bot to alert people in the IEEE UCI Discord when the room is open

### Usage
Flip switch "On" to send a discord message alerting people the room is open. Flip switch "Off" to send a message alerting people that the room is closed. 

### Installation & Configuration
* Extract & Install on pi. Install `requests` library through pip.
* You need to rename `creds_CHANGEME.py` to `_creds_.py` and add your discord webhook to the `WEBHOOK_URL` field in the file. 



### Indicator Light Behavior
* When operating correctly, only one light should be on at a time. The lights will ONLY change once a message has successfully been posted to discord.
* On errors, they blink. There should be a single blink on startup to indicate that the program is running. 

