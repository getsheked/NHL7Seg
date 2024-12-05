import json
import requests
import datetime
import RPi.GPIO as GPIO
from adafruit_ht16k33 import segments
import time
import board
import busio


x="MIN"
num=30



today = datetime.date.today()
date1=today.strftime("%Y-%m-%d")
url='https://api-web.nhle.com'
i2c= busio.I2C(board.SCL, board.SDA)
display=segments.Seg7x4(i2c, address=0x72)
display2=segments.Seg7x4(i2c,address=0x74)
display.fill(0)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
endpoint="/v1/scoreboard/now"
response = requests.get(url+endpoint) 
endpoint = "/v1/club-schedule-season/"+x+"/20242025"  
response1 = requests.get(url + endpoint)

def handshake():
    if response.status_code == 200:
        data = response.json()
        return "success" 
    else:
        return "fail"
def allOff():
    GPIO.output(14,GPIO.LOW)  
    GPIO.output(15,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
def gameOver():
    if source()["gameState"]=="FINAL" or "OFF" or "OVER" and not "LIVE" or "CRIT":
        print(5)
        if period()==3:
            display.print("F")
            return True
        elif period()==4:
            display.print("F/OT")
            return True
        elif period()==5:
            display.print("F/SO")
            return True
    else:
        return False
def timeTilNxt():
    for i in range(0,88):
        date2=response1.json()["games"][i]["gameDate"]
        '''date2=datetime.datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")'''
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
    gameDate=0
    gameNum=0
    gameID=0
    response = requests.get(url+"/v1/scoreboard/now") 
    response2= requests.get(url+"/v1/club-schedule-season/"+x+"/20242025")
    
    for i in range(0,86):
        if date1 == response2.json()["games"][i]["gameDate"]:
            gameID= response2.json()["games"][i]["id"]
    for i in range(0,6):
        if str(date1)== response.json()["gamesByDate"][i]["date"]:
            gameDate=i
    for i in range(0,len(response.json()["gamesByDate"][gameDate]["games"])):
        if response.json()["gamesByDate"][gameDate]["games"][i]["id"]==gameID:
             gameNum=i
    period=response.json()["gamesByDate"][gameDate]["games"][gameNum]["period"] 
    if response.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"] !="LIVE" or "CRIT":
        if period==3:
            display.print("F")
        elif period==4:
            display.print("F/OT")
        elif period==5:
            display.print("F/SO")
    try:
        if response.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"] == "LIVE" or "CRIT":
            display2.print(response.json()["gamesByDate"][gameDate]["games"][gameNum]["clock"]["timeRemaining"])
    except KeyError:
        print("clock key error, no api time")
    if period==1:
        GPIO.output(14,GPIO.HIGH)
        GPIO.output(15,GPIO.LOW)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
    elif period==2:
        GPIO.output(14,GPIO.LOW)
        GPIO.output(15,GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
    elif period==3:
        GPIO.output(14,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(23,GPIO.LOW)
    elif period==4 or period==5:
        GPIO.output(14,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(23,GPIO.HIGH)
    else:
        allOff()
    if response.json()["gamesByDate"][gameDate]["games"][gameNum]["gameState"]!="FUT":
        if response.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["id"]==num:
            display.print(str(response.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["score"])+"  "+str(response.json()["gamesByDate"][gameDate]["games"][gameNum]["awayTeam"]["score"]))
        else:
            display.print(str(response.json()["gamesByDate"][gameDate]["games"][gameNum]["awayTeam"]["score"])+"  "+str(response.json()["gamesByDate"][gameDate]["games"][gameNum]["homeTeam"]["score"]))
def noGameControl():
    i=gameConDate()
    display2.marquee("Next Game ",0.5,False)
    print(i)
    string=response1.json()["games"][i]["gameDate"]
    print(string)
    p1=string[5:7]
    p2=string[8:10]
    display2.marquee(p1+"."+p2+" At "+gameConTime(),0.5,False)
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
    cenTest=ttime-datetime.timedelta(hours=6)
    cenTest=datetime.datetime.strftime(cenTest,"%Y-%m-%d %H:%M:%S")
    fig2=cenTest[14:16]
    if int(cenTest[11:13]) >12:
        fig1=int(cenTest[11:13])-12
        return str(fig1)+":"+str(fig2)+" PM"
    else:
        return str(cenTest[11:13])+" AM"
