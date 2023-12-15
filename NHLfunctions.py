import json
import requests
from datetime import date
import RPi.GPIO as GPIO
from adafruit_ht16k33 import segments
import time
import board
import busio

response=requests.get("https://api-web.nhle.com/v1/scoreboard/now")
data=json.loads(response.text)
response=requests.get("https://api-web.nhle.com/v1/club-schedule-season/MIN/now")
shedData=json.loads(response.text)
today=date.today().strftime("%Y-%m-%d")    
i2c=busio.I2C(board.SCL,board.SDA)
display1=segments.Seg7x4(i2c,address=0x70)
display2=segments.Seg7x4(i2c,address=0x72)
display3=segments.Seg7x4(i2c,address=0x74)
display2.fill(0)
display3.fill(0)
display1.fill(0)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
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
        if(data['gamesByDate'][gameDateVal]['games'][i]['awayTeam']['abbrev']=="PIT"):
           gameNumVal=i
           homeAway=1
        if(data['gamesByDate'][gameDateVal]['games'][i]['homeTeam']['abbrev']=="PIT"):
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
def pTime():
    gameNumVal=homeAway()[2]
    gameDateVal=homeAway()[1]
   
    if(data['gamesByDate'][gameDateVal]['games'][gameNumVal]['gameState']=="FINAL" or data['gamesByDate'][gameDateVal]['games'][gameNumVal]['gameState']=="OFF"):
        if(period()==4):
            display1.print(" FOT")
        elif(period()==5):
            display1.print(" FSO")
        else:
            display1.print("   F")
    elif(time()=="00:00"):
        if(period()==5):
            display1.print("  SO")
        else:
            display1.print("END"+str(period()))
    if(time()!="00:00"):
        display1.print(time())
def pScore():
    display2.print(str(MNscore())+"  "+str(otherScore()))
def LEDcont():
    if(period()==1):
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(26,GPIO.LOW)
    elif(period()==2):
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.HIGH)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(26,GPIO.LOW)
    elif(period()==3):
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(26,GPIO.LOW)
    elif(period()>=4):
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(26,GPIO.HIGH)
    if(data['gamesByDate'][gameDateVal]['games'][gameNumVal]['gameState']=="FINAL" or data['gamesByDate'][gameDateVal]['games'][gameNumVal]['gameState']=="OFF"):
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(26,GPIO.LOW)
def allOff():
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(26,GPIO.LOW)
    
