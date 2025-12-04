import board
import busio
import datetime
import configparser 
from adafruit_ht16k33 import segments
class board:
    i2c = busio.I2C(board.SCL, board.SDA)
    config=configparser()
    config.read('config.ini')
    today = datetime.date.today()
    date1=today.strftime("%Y-%m-%d")
    abrev=config.get('team','teamABV')
    teamID=int(config.get('team','teamID'))
    tzone=config.get('time','zone')
    timeFormat=int(config.get('time','24hr'))
    season=config.get('time','season')
    display2=segments.Seg7x4(i2c, address=0x74)
    display=segments.Seg14x4(i2c,address =0x73)
print(board.today)