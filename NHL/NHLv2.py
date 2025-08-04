import json
import requests
import datetime
#import RPi.GPIO as GPIO
#from adafruit_ht16k33 import segments
import time
#import board
#import busio
from configparser import ConfigParser


#config setup
config=ConfigParser()
config.read('config.ini')
today = datetime.date.today()
date=today.strftime("%Y-%m-%d")
abrev=config.get('team','teamABV')
teamID=int(config.get('team','teamID'))
tzone=config.get('time','zone')
timeFormat=int(config.get('time','24hr'))
season=config.get('time','season')



def retriveSchedule():
  x=requests.get("https://api-web.nhle.com/v1/club-schedule-season/"+abrev+"/"+season)
  return x

print(retriveSchedule.json())