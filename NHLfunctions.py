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
date1=today.strftime("%Y-%m-%d")
abrev=config.get('team','teamABV')
teamID=config.get('team','teamID')
teamID=int(teamID)
tzone=config.get('time','zone')
timeFormat=config.get('time','24hr')
timeFormat=int(timeFormat) 
season=config.get('time','season')
#api setup

url='https://api-web.nhle.com'
endpointBoard="/v1/scoreboard/now"
scoreNow = requests.get(url+endpointBoard) 
endpointSched = "/v1/club-schedule-season/"+abrev+"/"+season  
schedule = requests.get(url + endpointSched)

# hardware setup

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
i2c= busio.I2C(board.SCL, board.SDA)
display2=segments.Seg7x4(i2c, address=0x74)
display=segments.Seg14x4(i2c,address=0x73)
display.fill(0)

def allOff():
    GPIO.output(14,GPIO.LOW)  
    GPIO.output(15,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
def timeTilNxt():
    for i in range(0,88):
        date2=schedule.json()["games"][i]["gameDate"]
        startUTC=schedule.json()["games"][i]["startTimeUTC"]
        adjtime=datetime.datetime.strptime(startUTC[:10]+" "+startUTC[11:19],"%Y-%m-%d %H:%M:%S")
        if(tzone > 0):
              tzoneadj=adjtime+datetime.timedelta(hours=tzone)
              x=tzoneadj+datetime.datetime.now()
        else: 
              tzoneadj=adjtime-datetime.timedelta(hours=abs(tzone))
              x=tzoneadj-datetime.datetime.now()
        if x<datetime.timedelta(hours=1) and x>datetime.timedelta(seconds=-1):
            return True
    return False
    

def oneCall():
    gameDate=-1
    gameNum=-1
    gameID=-1
    
    for i in range(0,86):
        if date1 == schedule.json()["games"][i]["gameDate"]:
            gameID= schedule.json()["games"][i]["id"]
    for i in range(0,6):
        if str(date1)== scoreNow.json()["gamesByDate"][i]["date"]:
            gameDate=i
    for i in range(0,len(scoreNow.json()["gamesByDate"][gameDate]["games"])):
        if scoreNow.json()["gamesByDate"][gameDate]["games"][i]["id"]==gameID:
             gameNum=i
             
    print(str(gameID)+" "+str(gameDate)+" "+str(gameNum));
    if gameDate != -1 or gameNum !=-1 or gameID !=-1:
        try:
            period=scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["period"] 
            if scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"] !="LIVE" or "CRIT":
                if period==3:
                    display2.print("F   ")
                elif period==4:
                    display2.print("F/OT")
                elif period==5:
                    display2.print("F/SO")
            if period==1:
                GPIO.output(14,GPIO.HIGH)
            elif period==2:
                GPIO.output(14,GPIO.LOW)
                GPIO.output(15,GPIO.HIGH)
            elif period==3:
                GPIO.output(15,GPIO.LOW)
                GPIO.output(18,GPIO.HIGH)
            elif period==4 or period==5:
                GPIO.output(18,GPIO.LOW)
                GPIO.output(23,GPIO.HIGH)
        except KeyError:
            print("no period")
            allOff()
        try:
            scoreNow = requests.get(url+endpointBoard) 
            if scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"] == "LIVE" or "CRIT":
                display2.print(scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["clock"]["timeRemaining"])
        except KeyError:
            print("clock key error, no api time")
   
        if scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"]!="FUT":
            if scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["id"]==teamID:
                display.print(str(scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["score"])+"  "+str(scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["awayTeam"]["score"]))
            else:
                display.print(str(scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["awayTeam"]["score"])+"  "+str(scoreNow.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["score"]))
def noGameControl():
    i=gameConDate()
    if schedule.json()['games'][i]['homeTeam']['id']==teamID:
        site="Vs"
        HomeTeam=schedule.json()['games'][i]['awayTeam']['abbrev']
    else:
        site="At"
        HomeTeam=schedule.json()['games'][i]['homeTeam']['abbrev']
    if schedule.json()['games'][i-1]['homeTeam']['id']==teamID:
        otherAbrev=schedule.json()['games'][i-1]['awayTeam']['abbrev']
        OtherScore=schedule.json()['games'][i-1]['awayTeam']['score']
        SelectScore=schedule.json()['games'][i-1]['homeTeam']['score']
    else:
        OtherScore=schedule.json()['games'][i-1]['homeTeam']['score']
        otherAbrev=schedule.json()['games'][i-1]['homeTeam']['abbrev']
        SelectScore=schedule.json()['games'][i-1]['awayTeam']['score']
    clock()
    display.marquee("Next Game ",0.5,False)
    xstring=schedule.json()["games"][i]["gameDate"]
    display.marquee(xstring[5:7]+"."+xstring[8:10]+" At "+gameConTime()+" "+site+" "+HomeTeam,0.5,False)
    display.marquee("Last Game "+abrev+" "+str(SelectScore)+" "+otherAbrev+" "+str(OtherScore), 0.5,False)
def gameConDate():
    date1=datetime.date.today()
    for y in range(0,7):
        change=datetime.timedelta(days=y)
        date2=date1+change
        for i in range(0,88):
            x=schedule.json()["games"][i]["gameDate"]
            if x == datetime.datetime.strftime(date2,"%Y-%m-%d")[:11]:
                return i
def gameConTime():
    i=gameConDate()
    test=schedule.json()["games"][i]["startTimeUTC"]
    adjtime=datetime.datetime.strptime(test[:10]+" "+test[11:19],"%Y-%m-%d %H:%M:%S")
    if(tzone > 0):
         tzoneadj=adjtime+datetime.timedelta(hours=tzone)
         x=tzoneadj+datetime.datetime.now()
    else: 
         tzoneadj=adjtime-datetime.timedelta(hours=abs(tzone))
         x=tzoneadj-datetime.datetime.now()
    fig2=tzoneadj[14:16]
    if timeFormat != 1:
        if int(tzoneadj[11:13]) >12:
            fig1=int(tzoneadj[11:13])-12
            return str(fig1)+"."+str(fig2)+" PM"
        else:        
            return tzoneadj[11:13]+"."+fig2+" AM"
    else:  
            return tzoneadj[11:13]+"."+fig2
def clock():
    y=datetime.datetime.strftime(datetime.datetime.now(),"%H:%M")
    if timeFormat != 1:
        print(y[0:2])
        if int(y[0:2])>12:
            p=int(y[0:2])-12
            y=" "+str(p)+":"+y[3:5]
            display2.print(y)
        else:
            display2.print(y)
    else:
            display2.print(y)
        