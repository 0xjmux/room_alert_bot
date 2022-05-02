# room_alert_bot
Physical switch connected to a Discord bot to alert people in the IEEE UCI Discord when the room is open. 

<img src="https://raw.githubusercontent.com/0xjmux/room_alert_bot/main/img/final_mounted.JPG" width=80% height=80%>

### Why?
I manage the lab room for the IEEE student chapter at UCI. We run a program called Open Project Space, or OPS, where we teach fellow students the basics of electronics and microcontrollers in a hands on fashion. Part of the program is students coming in to get help on their current projects, and the problem we kept running into was students asking if someone was in the room so that they could get help with their project. 

So, to fix this admittedly minor inconvenience, I built a completely over engineered solution :). 

### Usage
Flip switch "On" to send a discord message alerting people the room is open. Flip switch "Off" to send a message alerting people that the room is closed. 

<img src="https://raw.githubusercontent.com/0xjmux/room_alert_bot/main/img/green.JPG" width=50% height=50%>
<img src="https://raw.githubusercontent.com/0xjmux/room_alert_bot/main/img/red.JPG" width=50% height=50%>

### Indicator Light Behavior
* When operating correctly, only one light should be on at a time. The lights will ONLY change once a message has successfully been posted to discord.
* Blinking:
    * There should be a double blink on startup to indicate that the program has begun execution. 
    * On errors, they blink. If there's a lost network connection, or discord's servers are down, or anything else has caused several errors to rack up, the lights should alert the user that something's not right. 


### FAQ
#### Why was it designed the way it was?
A significant part of the design choices I made kept in mind that this thing isn't going to be touched or maintained for the next few years at least. The hardware, software, and system setup are optimized and consciously designed to run on their own with little to no maintenance required for as long as possible.

In addition, the hardware was designed to make any modifications or maintenance that need to be done as simple as possible. for example, the hardware is exclusively mounted on the lid of the project box; if maintenance needs to be done on the hardware for some reason, you just unscrew the 2 screws, disconnect the 2.1mm jack (which is connected via custom crimped dupont to make that easy) and then the hardware can be taken wherever to be worked on, with the rest of the case still mounted to the wall.


#### How does it work?
The design philosophy behind this was that I wanted it to be able to go on running as long as possible without any maintenance on the actual device. I predict that this is going to sit on the network long after I leave UCI, and nobody's going to really touch it as long as it keeps working. 

It runs on a Raspberry Pi Zero W, connected to Wifi. The electronics are really simple; it's really only a toggle switch, 2 LEDs, and a buck converter for DC step-down. It runs off ~12VDC, which was done for ease of use and because we 
had plenty of 12V power supplies with 2.1mm barrel jacks. 

<img src="https://raw.githubusercontent.com/0xjmux/room_alert_bot/main/img/internals_1.JPG" width=50% height=50%>
<img src="https://raw.githubusercontent.com/0xjmux/room_alert_bot/main/img/internals_2.JPG" width=50% height=50%>


##### What about the code?
It uses discord webhooks to send messages as HTTP POST requests, which means the connection is sort of asynchronous. It only reaches out to the server when it needs to send a message, and is quiet otherwise. In fact, the code *could* have been very simple; just see if the switch has changed position and then send the message. 

However, I was worried about a few edge cases:
* What about when the WiFi drops out and it loses connection?
* What if the internet goes out and it can't send the message?
* What if discord's servers are down, how do I prevent it spamming API requests and getting IP banned?

So, the code is far more complicated than it really needed to be. 
Some features include:
* The LEDs change state on successful posting of a message. If you flip the switch "ON", the LEDs won't switch from green to red until the room open message is posted.
* If we try to send a message and fail after 5 attempts, both LEDs on the case will begin to blink and the bot will check the discord service status page to check if there's some kind of outage reported. If there is, we slow down the checking significantly.
    * If for some reason we're failing a ton of attempts, it's configured to send alert emails with error descriptions to the operator specified email address.
* A decent amount of effort, testing and debugging has been put into handling errors and making sure they don't result in crashes. Alerting is a large part of that, because the system isn't going to be logged into often. 
* Logging to files is implemented with the python `logging` library, and the program generates logs with timestamps during operation, in case they're needed for debugging or root cause analysis. 

What the messages look like posted to discord. 

(the "room closed" followed right by "room open" are caused by people playing with the switch, and not any actual error in the hardware or software)

<img src="https://raw.githubusercontent.com/0xjmux/room_alert_bot/main/img/ieee_discord.png" width=70% height=70%>

##### Why use a physical switch instead of something like a motion/PIR sensor?
I've been asked this a few times, so I figured I'd explain the reasoning here. 
First off, the physical switch was a conscious design choice, for a few reasons 
1. the sensor would be fine for sending the "room open" message, but it would also have to send the "room closed" message. The only way I've seen to do this reliably is to check for motion periodically, and after a certain time frame with no movement send the "closed" alert. This isn't really acceptable from a user trust standpoint, since there will be time when the last message in the channel is wrong, and says that the room is open when it isn't. If someone comes in that 15 minutes or so after the room closed and sees that it's not open, that significantly reduces trust in the system since it, by design, wouldn't always be accurate. 
2. In a similar vein, if someone's coming in to the room just to grab something quick and isn't planning on staying, the PIR will send the "room open" alert but the room won't actually be open by the time anybody shows up
3. One of the main purposes of the project was to make it so people didn't have to message "is the room open" to see if anyone's there. If every time it's used there's a window where the message is wrong, the alert is unreliable, it'll be back to messaging to ask if it's open.
4. Also, some PIR sensors can be buggy and not super reliable. it might just not detect when someone's there; it might detect a bug moving around or something left on that's warm as a person, and think that someone's there when they aren't.
5. In my personal opinion, "smarter" devices aren't always better. Keeping things simple, reliable, and trustworthy is more advantageous over a system that might require less "direct" user interaction, but adds significant complexity and room for error.


## What if I want to build my own?
### Installation & Configuration
* Extract & Install repo on pi. Install `requests` and `logging` library through pip.
* You need to rename `creds_CHANGEME.py` to `_creds_.py` and add your discord webhook to the `WEBHOOK_URL` field in the file. 

### General Info
* Program logs are located at `/var/log/ieee_room_alert/`. Permissions for this directory should be set with GID mask, and you should be running the program as a daemon using a user created just for it. 
* Firewall rules should be configured to only allow inbound SSH.
* Automatic updates should be configured with `unattended-upgrade` to allow for autonomous operation. 
* The service should be daemonized in your init system (I used `systemd`), and set to start up on boot and auto-restart itself in case of issues. 

