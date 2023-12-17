import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BCM)

led_pin = 18
GPIO.setup(led_pin, GPIO.OUT) 
cognibot = subprocess.check_output("systemctl is-active cognibot", shell=True)

if cognibot == "active":
   GPIO.output(led_pin, GPIO.HIGH) # Turn on 
else:
   GPIO.output(led_pin, GPIO.LOW) # Turn off

time.sleep(5)


