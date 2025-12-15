#!/srv/nhl/nhlvirtual/bin/python
import board
import RPi.GPIO as GPIO
import os
import busio
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import requests
import tzlocal
from configparser import ConfigParser 
from adafruit_ht16k33 import segments

class boardcontrols:
    i2c = busio.I2C(board.SCL, board.SDA)
    display2=segments.Seg7x4(i2c, address=0x74)
    display=segments.Seg14x4(i2c,address =0x73)
class teaminfo:
    config=ConfigParser()
    config.read('config.ini')
    
    teamID=int(config.get('team','teamID'))
    teamAbv=config.get('team', 'teamabv')
    timeFormat=int(config.get('time','24hr'))
    offset=datetime.now().astimezone()
    x=datetime.strftime(offset,"%z")
    z=x[2:3]
    y=x[3:5]
    delta=timedelta(hours=int(z),minutes=int(y))
    timeInfo=delta,x[0]

    response=requests.get("https://api-web.nhle.com/v1/club-schedule-season/"+teamAbv+"/now")
    data=response.json()
    gameList=[]
    for i in range(len(data['games'])):
            y=data['games'][i]['id']
            x=data['games'][i]['gameDate']
            x=datetime.strptime(x,"%Y-%m-%d").date()
            entry=[x,y]
            gameList.append(entry)
