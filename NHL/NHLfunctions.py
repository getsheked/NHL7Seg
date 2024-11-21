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
date1="2024-11-19"
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

def handshake():
    endpoint="/v1/score/now"
    response = requests.get(url+endpoint)  
    if response.status_code == 200:
        data = response.json()
        return "success" 
    else:
        return "fail"
def gameNum():
    endpoint= "/v1/scoreboard/now"
    response=requests.get(url+endpoint)
    x=len(response.json()["gamesByDate"][getDate()]["games"])
    for i in range(0,x-1):
        if response.json()["gamesByDate"][getDate()]["games"][i]["id"] == ID():
            return i
def getDate():
    endpoint="/v1/scoreboard/now"
    response=requests.get(url+endpoint)
    for i in range(0,6):
        if date1== response.json()["gamesByDate"][i]["date"]:
            return i
def ID():
    endpoint = "/v1/club-schedule-season/MIN/20242025"
    response = requests.get(url + endpoint)
    for i in range(0,86):
        if date1 == response.json()["games"][i]["gameDate"]:
            return response.json()["games"][i]["id"]
            break
def game():
    x=getDate()
    endpoint = "/v1/scoreboard/now"
    response= requests.get(url+endpoint)
    for i in range(0,x+1):
        if response.json()["gamesByDate"][getDate()]["games"][i]["id"]==ID():
            return i
def homeAway():
    endpoint="/v1/scoreboard/now"
    response=requests.get(url+endpoint)
    x=game()
    if response.json()["gamesByDate"][getDate()]["games"][x]["homeTeam"]["id"]==30:
        return 1
    elif response.json()["gamesByDate"][getDate()]["games"][x]["awayTeam"]["id"]==30:
        return 2
def source():  
    response=requests.get(url+"/v1/scoreboard/now")
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
    elif period()>=4:
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
def timeTilNxt():
    endpoint="/v1/club-schedule-season/MIN/20242025"
    response=requests.get(url+endpoint)
    for i in range(0,88):
        date2=response.json()["games"][i]["gameDate"]
        '''date2=datetime.datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")'''
        test=response.json()["games"][i]["startTimeUTC"]
        testsub1=test[:10]
        testsub2=test[11:19]
        test=testsub1+" "+testsub2
        ttime=datetime.datetime.strptime(test,"%Y-%m-%d %H:%M:%S")
        cenTest=ttime-datetime.timedelta(hours=6)
        x=cenTest-datetime.datetime.now()
        if x<datetime.timedelta(hours=12) and x>datetime.timedelta(seconds=-1):
            return True


print(ID())
print(game())
print(gameNum())
print(getDate())
