from setup import boardcontrols
boardcontrols=boardcontrols()
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT) 
GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
def ledcontroller(x):
    if x==1:
        GPIO.output(14,GPIO.HIGH)
    elif x==2:
        GPIO.output(14,GPIO.LOW)
        GPIO.output(15,GPIO.HIGH)
    elif x==3:
        GPIO.output(15,GPIO.LOW)
        GPIO.output(18,GPIO.HIGH)
    elif x==4 or period==5:
        GPIO.output(18,GPIO.LOW)
        GPIO.output(23,GPIO.HIGH)
        
    else:
        GPIO.output(18,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
        GPIO.output(14,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)
def clock(x):
    boardcontrols.display2.print(x)
def inGame(x):
    boardcontrols.display.print(x)
def noGame(x,y):
    boardcontrols.display.marquee(x, 0.5,False)
    boardcontrols.display.marquee(y, 0.5,False)