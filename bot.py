import RPi.GPIO as GPIO
import time
import os

#adjust for where your switch is connected
buttonPin = 17 #change this later
R_LED = 27
G_LED = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)
GPIO.setup(R_LED,GPIO.OUT)
GPIO.setup(G_LED,GPIO.OUT)

prev_input = 0

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