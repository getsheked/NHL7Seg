#main.py
import infogetter
import hardwarecontrol
from datetime import datetime
while 1<2:
    x=infogetter.control()
    #sample control response (0, (False, 'COL', 2, 'NSH', 2, '13:11', 2, 'LIVE', False))
    if int(x[0])==0:
        hardwarecontrol.ledcontroller(x[1][6])
        z=str(x[1][2])+"  "+str(x[1][4])
        hardwarecontrol.inGame(z)
        if x[1][8]==False:
            hardwarecontrol.clock(x[1][5])
    else:
        hardwarecontrol.noGame(x[0],x[1])
        hardwarecontrol.clock(datetime.now().strftime("%H%M"))
        