import json
import requests
import datetime
import RPi.GPIO as GPIO
from adafruit_ht16k33 import segments
import time
import board
import busio
from NHLfunctions import *

i2c= busio.I2C(board.SCL, board.SDA)
display=segments.Seg7x4(i2c, address=0x72)
display2=segments.Seg7x4(i2c,address=0x74)
display.fill(0)
allOff()
while 1<2:
	display.fill(0)
	display2.fill(0)
	display2.print(str(MINScore())+"  "+str(otherScore()))
	if gameOver()== True:
		if source()["gameState"]=="FINAL" or "OFF":
			if period()==3:
				display.fill()
				display.print("F")
			elif period()==4:
				isplay.fill()
				display.print("F-OT")
			elif period()==5:
				isplay.fill()
				display.print("F-SO")
			if timeTilNxt()==True:
				while timeTilNxt()== True:
					print("Waiting")
					allOff()
					time.sleep(360)
			
	else:
		display.fill(0)
		display2.fill(0)
		display.print(clock())
		periodCont()
		display2.print(MINScore()+"  "+otherScore())
		
