import json
import requests
import datetime
import RPi.GPIO as GPIO
from adafruit_ht16k33 import segments
import time
import board
import busio
from configparser import ConfigParser

#config setup

config=ConfigParser()
config.read('config.ini')
today = datetime.date.today()
date1=today.strftime("%Y-%m-%d")
x=config.get('team','teamABV')
num=config.get('team','teamID')
num=int(num)
tzoffset=config.get('time','zone')
timeFormat=config.get('time','24hr')
timeFormat=int(timeFormat) 
#api setup

url='https://api-web.nhle.com'
endpoint="/v1/scoreboard/now"
response = requests.get(url+endpoint) 
endpoint = "/v1/club-schedule-season/"+x+"/20242025"  
response1 = requests.get(url + endpoint)

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
def gameOver():
    if response.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"]=="FINAL" or "OFF" or "OVER" and not "LIVE" or "CRIT":
        if period()==3:
            display2.print("F")
        elif period()==4:
            display2.print("F/OT")
            return True
        elif period()==5:
            display2.print("F/SO")
            return True
    else:
        return False
def timeTilNxt():
    for i in range(0,88):
        date2=response1.json()["games"][i]["gameDate"]
        test=response1.json()["games"][i]["startTimeUTC"]
        testsub1=test[:10]
        testsub2=test[11:19]
        test=testsub1+" "+testsub2
        ttime=datetime.datetime.strptime(test,"%Y-%m-%d %H:%M:%S")
        cenTest=ttime-datetime.timedelta(hours=6)
        x=cenTest-datetime.datetime.now()
        if x<datetime.timedelta(hours=1) and x>datetime.timedelta(seconds=-1):
            return True
    return False
    

def oneCall():
    gameDate=-1
    gameNum=-1
    gameID=-1
    
    for i in range(0,86):
        if date1 == response1.json()["games"][i]["gameDate"]:
            gameID= response1.json()["games"][i]["id"]
    for i in range(0,6):
        if str(date1)== response.json()["gamesByDate"][i]["date"]:
            gameDate=i
    for i in range(0,len(response.json()["gamesByDate"][gameDate]["games"])):
        if response.json()["gamesByDate"][gameDate]["games"][i]["id"]==gameID:
             gameNum=i
             
    print(str(gameID)+" "+str(gameDate)+" "+str(gameNum));
    if gameDate != -1 or gameNum !=-1 or gameID !=-1:
        try:
            period=response.json()["gamesByDate"][gameDate]["games"][gameNum]["period"] 
            if response.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"] !="LIVE" or "CRIT":
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
            response3 = requests.get("https://api-web.nhle.com/v1/scoreboard/now")
            if response3.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"] == "LIVE" or "CRIT":
                display2.print(response3.json()["gamesByDate"][gameDate]["games"][gameNum]["clock"]["timeRemaining"])
        except KeyError:
            print("clock key error, no api time")
   
        if response3.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"]!="FUT":
            if response3.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["id"]==num:
                display.print(str(response3.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["score"])+"  "+str(response.json()["gamesByDate"][gameDate]["games"][gameNum]["awayTeam"]["score"]))
            else:
                display.print(str(response3.json()["gamesByDate"][gameDate]["games"][gameNum]["awayTeam"]["score"])+"  "+str(response.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["score"]))
def noGameControl():
    i=gameConDate()
    if response1.json()['games'][i]['homeTeam']['id']==num:
        site="Vs"
        other=response1.json()['games'][i]['awayTeam']['abbrev']
    else:
        site="At"
        other=response1.json()['games'][i]['homeTeam']['abbrev']
    if response1.json()['games'][i-1]['homeTeam']['id']==num:
        other2=response1.json()['games'][i-1]['awayTeam']['abbrev']
        OtherScore=response1.json()['games'][i-1]['awayTeam']['score']
        MNScore=response1.json()['games'][i-1]['homeTeam']['score']
    else:
        OtherScore=response1.json()['games'][i-1]['homeTeam']['score']
        other2=response1.json()['games'][i-1]['homeTeam']['abbrev']
        MNScore=response1.json()['games'][i-1]['awayTeam']['score']
    clock()
    display.marquee("Next Game ",0.5,False)
    string=response1.json()["games"][i]["gameDate"]
    p1=string[5:7]
    p2=string[8:10]
    display.marquee(p1+"."+p2+" At "+gameConTime()+" "+site+" "+other,0.5,False)
    display.marquee("Last Game MIN "+str(MNScore)+" "+other2+" "+str(OtherScore), 0.5,False)
def gameConDate():
    date1=datetime.date.today()
    for y in range(0,7):
        change=datetime.timedelta(days=y)
        date2=date1+change
        for i in range(0,88):
            x=response1.json()["games"][i]["gameDate"]
            if x == datetime.datetime.strftime(date2,"%Y-%m-%d")[:11]:
                return i
def gameConTime():
    i=gameConDate()
    test=response1.json()["games"][i]["startTimeUTC"]
    testsub1=test[:10]
    testsub2=test[11:19]
    test=testsub1+" "+testsub2
    ttime=datetime.datetime.strptime(test,"%Y-%m-%d %H:%M:%S")
    cenTest=ttime-datetime.timedelta(hours=int(tzoffset))
    cenTest=datetime.datetime.strftime(cenTest,"%Y-%m-%d %H:%M:%S")
    fig2=cenTest[14:16]
    print(cenTest[11:16])
    if timeFormat != 1:
        if int(cenTest[11:13]) >12:
            fig1=int(cenTest[11:13])-12
            return str(fig1)+"."+str(fig2)+" PM"
        else:        
            return cenTest[11:13]+"."+fig2+" AM"
    else:  
            return cenTest[11:13]+"."+fig2
def clock():
    x=datetime.datetime.now()
    y=datetime.datetime.strftime(x,"%H:%M")
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
        

#def totwelve(t)
 #   time 
