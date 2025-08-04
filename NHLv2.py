
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
DateFormat=config.get('time','SecondDigit')


#global variables
gameID=0
storedDay=datetime.datetime.now(datetime.timezone.utc)
gameday= False

def retriveScheduleJSON():
  x=requests.get("https://api-web.nhle.com/v1/club-schedule-season/"+abrev+"/"+season)
  return x.json()

def dayChecker():
   testtime=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
   global storedDay
   global gameID
   global gameday
   if testtime> storedDay.strftime("%Y-%m-%d"): 
        storedDay=testtime
        for i in range(gameID,88):
         x=retriveScheduleJSON()["games"][i]["startTimeUTC"]
         x=datetime.datetime.strptime(x[:10],"%Y-%m-%d")
         if datetime.datetime.now(datetime.utc).strftime("%Y-%m-%d")== x.strftime("%Y-%m-%d"):
            gameid=i
            gameday=True
        else: 
            gameday=False

def DisplayClock():
        if timeFormat == 12:
            FormatCode = "%I:%M %p"
        else: FormatCode= "%H:%M"
        return datetime.datetime.now().strftime(FormatCode)
def DisplayDate():
    if DateFormat== 'M':
       DateCode="%A, %B %e"
    else: DateCode="%A,%e %B"
    return datetime.datetime.now().strftime(DateCode)

dayChecker()