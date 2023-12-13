import json
import requests
from datetime import date
import RPi.GPIO as GPIO

response=requests.get("https://api-web.nhle.com/v1/scoreboard/now")
data=json.loads(response.text)
response=requests.get("https://api-web.nhle.com/v1/club-schedule-season/MIN/now")
shedData=json.loads(response.text)
today=date.today().strftime("%Y-%m-%d")

today="2023-12-10"

def gameday():
    game=None
    n=82
    for i in range(0,n):
        print(shedData['games'][i]['gameDate'])
        if(today==shedData['games'][i]['gameDate']):
            return True;
    if(game==False or game==None):
        return False

def homeAway():
    gameDateVal=None
    gameNumVal=None
    homeAway=None
    n=data['focusedDateCount']
    for i in range(0,n):
        if(data['gamesByDate'][i]['date']==today):
            gameDateVal=i;
    x=len(data['gamesByDate'][gameDateVal]['games'])
    for i in range(0,x):
        if(data['gamesByDate'][gameDateVal]['games'][i]['awayTeam']['abbrev']=="MIN"):
           gameNumVal=i
           homeAway=1
        if(data['gamesByDate'][gameDateVal]['games'][i]['homeTeam']['abbrev']=="MIN"):
           gameNumVal=i
           homeAway=2
    return [homeAway,gameDateVal,gameNumVal]

def MNscore():
    gameNumVal=homeAway()[2]
    gameDateVal=homeAway()[1]
    venue=homeAway()[0]
    if(venue==1):
       return data['gamesByDate'][gameDateVal]['games'][gameNumVal]['awayTeam']['score']
    if(venue==2):
        return data['gamesByDate'][gameDateVal]['games'][gameNumVal]['homeTeam']['score']
def otherScore():
    gameNumVal=homeAway()[2]
    gameDateVal=homeAway()[1]
    venue=homeAway()[0]
    if(venue==2):
       return data['gamesByDate'][gameDateVal]['games'][gameNumVal]['awayTeam']['score']
    if(venue==1):
        return data['gamesByDate'][gameDateVal]['games'][gameNumVal]['homeTeam']['score']
def gameID():
    gameNumVal=homeAway()[2]
    gameDateVal=homeAway()[1]
    return data['gamesByDate'][gameDateVal]['games'][gameNumVal]['id']
def time():
    response=requests.get("https://api-web.nhle.com/v1/gamecenter/"+str(gameID())+"/boxscore")
    gameInfo=json.loads(response.text)
    return (gameInfo['clock']['timeRemaining'])
def period():
    response=requests.get("https://api-web.nhle.com/v1/gamecenter/"+str(gameID())+"/boxscore")
    gameInfo=json.loads(response.text)
    return gameInfo['period']

    

    
