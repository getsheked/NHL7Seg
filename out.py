import time
import board
import busio
from adafruit_ht16k33 import segments
from NHLfunctions import *

x=homeAway()[0]
while 0<10:
	if(x==2 or x==1):
		pTime()
		pScore()
		LEDcont()
	allOff()
		
