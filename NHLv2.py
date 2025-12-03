
'''

test 
NHLv2.py 

MIT License

Copyright (c) 2024 Getsheked

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice, and the below disclaimer and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''



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
#i dont care if you dont like them. i dont know what im doing! IM CRAZY
gameNumber=0
storedDay=datetime.datetime.now(datetime.timezone.utc)
gamedate=0
def retriveScheduleJSON():
  x=requests.get("https://api-web.nhle.com/v1/club-schedule-season/"+abrev+"/"+season)
  return x.json()
def retriveScoreboardJSON(x):
    y=requests.get("https://api-web.nhle.com/v1/gamecenter/"+str(x)+"/boxscore")
    return y.json()
def InfoFinder():#make better adjust for more games/playoffs
   testtime=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
   global storedDay
   global gameNumber
   if testtime> storedDay.strftime("%Y-%m-%d"): 
        storedDay=testtime
        y=retriveScheduleJSON()
        for i in range(gameNumber,88):
         x=y["games"][i]["startTimeUTC"]
         x=datetime.datetime.strptime(x[:10],"%Y-%m-%d")
         if datetime.datetime.now(datetime.utc).strftime("%Y-%m-%d")== x.strftime("%Y-%m-%d"):
            gameNumber=i
            gameID=y["games"][i]["id"]
            return True, gameID
        else: 
            return False, gameNumber
   else: return False, gameNumber

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
def getGameInformation():
    
   if 1==1:#InfoFinder()[0]==True:
       gameID=InfoFinder()[1]
       y=retriveScoreboardJSON(2023020204)
       period=y["periodDescriptor"]["number"]
       if y["clock"]["InIntermission"]== "True":
            period = "Int"
       elif period <=3:
            period= str(period)
       elif period == 4:
            period="OT"
       elif period == 5:
            period="SO"       
       gameState=y["gameState"]
       if y["homeTeam"]==abrev:
             favScore=y["homeTeam"]["score"]
             favShots= y["homeTeam"]["sog"]
             otherScore=y["awayTeam"]["score"]
             otherShots= y["awayTeam"]["sog"]
             otherID= y["awayTeam"]["abbrev"]
       else: 
           favScore=y["awayTeam"]["score"]
           favShots= y["awayTeam"]["sog"]
           otherScore=y["homeTeam"]["score"]
           otherShots= y["homeTeam"]["sog"]
           otherID=y["homeTeam"]["abbrev"]
       if gameState != "OFF" or "FUT":
              if period != "SO":
                gameTime=y["clock"]["timeRemaining"]
                gameON= True
              else: gameON= False
       else: gameTime= 0
       return gameON, gameState, period, gameTime, favScore, favShots, otherID, otherScore, otherShots
   else: return 0

              




# do this during the game 
#do this right before the game 
#do this right after the game 
#do this between games 

def setup():
   print("Do you need to change settings? (Y/N)")
   if input()=="Y" or "y":
      print("Enter 3 Letter Team Abreveation")
      teamData=config["team"]
      x=input().upper()
      teamData["teamABV"]=x
      timeData=config["time"]
      print("Enter Time Format (12 for AM/PM)(24 for 24hr)")
      timeData["24hr"]=input()
      y=requests.get("https://api-web.nhle.com/v1/season")
      timeData["season"]=str(y.json()[len(y.json())-1])
      print("Enter Date Format (M for Weekday, Month Day)(D for Weekday, Day Month)")
      timeData["SecondDigit"]=input().upper()
      with open('teamAbrevList.json', 'r') as teams:
        teams=json.load(teams)
      teamID=teams[abrev]["ID"]
      teamData=config["team"]
      teamData["teamid"]=str(teamID)
      with open('config.ini', 'w') as conf:
        config.write(conf)         

setup()
print(getGameInformation())
