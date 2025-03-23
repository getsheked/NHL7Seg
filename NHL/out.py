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
display2=segments.Seg7x4(i2c, address=0x74)
display=segments.Seg14x4(i2c,address =0x73)
display.fill(0)
display2.fill(0)
allOff()
print(x)
print(num)

while 1<2:
	print("RUNNING")
	oneCall()
	
	
		
  

