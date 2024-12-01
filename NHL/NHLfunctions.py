import json
import requests
import datetime
import RPi.GPIO as GPIO
from adafruit_ht16k33 import segments
import time
import board
import busio

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
endpoint = "/v1/club-schedule-season/MIN/20242025"  
response1 = requests.get(url + endpoint)
def refresh():
    endpoint="/v1/scoreboard/now"
    response = requests.get(url+endpoint)  
    endpoint = "/v1/club-schedule-season/MIN/20242025"  
    response1 = requests.get(url + endpoint)
def handshake():
    if response.status_code == 200:
        data = response.json()
        return "success" 
    else:
        return "fail"
def gameNum():
    x=len(response.json()["gamesByDate"][getDate()]["games"])
    for i in range(0,x):
        if response.json()["gamesByDate"][getDate()]["games"][i]["id"] == ID():
            return i
    
def getDate():
    for i in range(0,6):
        if str(date1)== response.json()["gamesByDate"][i]["date"]:
            return i
def ID():
    for i in range(0,86):
        if date1 == response1.json()["games"][i]["gameDate"]:
            return response1.json()["games"][i]["id"]
            break
def game():
    x=getDate()
    for i in range(0,x+1):
        if response.json()["gamesByDate"][getDate()]["games"][i]["id"]==ID():
            return i
def homeAway():
    x=game()
    if response.json()["gamesByDate"][getDate()]["games"][x]["homeTeam"]["id"]==30:
        return 1
    elif response.json()["gamesByDate"][getDate()]["games"][x]["awayTeam"]["id"]==30:
        return 2
def source():  
    return response.json()["gamesByDate"][getDate()]["games"][gameNum()]
def MINScore():
    if source()["gameState"]!="FUT":
        if homeAway()==1:
            return source()["homeTeam"]["score"]
        elif homeAway()==2:
            return source()["awayTeam"]["score"]
        else:
            return error
def otherScore():
     if source()["gameState"]!="FUT":
        if homeAway()==2:
            return source()["homeTeam"]["score"]
        elif homeAway()==1:
            return source()["awayTeam"]["score"]
def clock():
    response=requests.get(url+"/"+str(ID())+"/landing")
    if source()["gameState"]== "LIVE":
        return source()["clock"]["timeRemaining"]
    elif source()["gameState"]== "FUT" or "OFF":
         return "NA"
def period():
    if source()["gameState"]!="FUT":
        return source()["periodDescriptor"]["number"]
def periodCont():
    if period() is not None:
        if period()==1:
            GPIO.output(14,GPIO.HIGH)
            GPIO.output(15,GPIO.LOW)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)
        elif period()==2:
            GPIO.output(14,GPIO.LOW)
            GPIO.output(15,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)
        elif period()==3:
            GPIO.output(14,GPIO.LOW)
            GPIO.output(15,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(23,GPIO.LOW)
        elif period()==4 or period()==5:
            GPIO.output(14,GPIO.LOW)
            GPIO.output(15,GPIO.LOW)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(23,GPIO.HIGH)
def allOff():
    GPIO.output(14,GPIO.LOW)  
    GPIO.output(15,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
def gameOver():
    if source()["gameState"]=="FINAL" or "OFF":
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
        if x<datetime.timedelta(hours=12) and x>datetime.timedelta(seconds=-1):
            return True
    
