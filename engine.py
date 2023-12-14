import time
import board
import busio
from adafruit_ht16k33 import segments
from NHLfunctions import *
i2c=busio.I2C(board.SCL,board.SDA)
print(i2c.scan())
display1=segments.Seg7x4(i2c,address=0x70)
display2=segments.Seg7x4(i2c,address=0x72)
display3=segments.Seg7x4(i2c,address=0x74)
display2.fill(0)
display3.fill(0)
display1.fill(0)
def pTime():
	display1.print(time())
def pScore():
	display2.print(str(MNscore())+"  "+str(otherScore()))


