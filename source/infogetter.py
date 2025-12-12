from setup import teaminfo
from datetime import datetime
import requests
teaminfo=teaminfo()

def scoreboardCall(x):
    response=requests.get("https://api-web.nhle.com/v1/gamecenter/"+str(x)+"/boxscore")
    data=response.json()
    return data

def gameDayCheck():
    for i in range(len(teaminfo.gameList)):
        if teaminfo.gameList[i][0]==datetime.today().date():
            if scoreboardCall(teaminfo.gameList[i][1])['gameState']=="OFF":
                return 1, teaminfo.gameList[i][1], teaminfo.gameList[i-1][1]  
            return 0,0,teaminfo.gameList[i][1]
        elif teaminfo.gameList[i][0]>datetime.today().date():
                return 1, teaminfo.gameList[i][1], teaminfo.gameList[i-1][1]           
def nextGame(x):
    start=x['startTimeUTC']
    offset=teaminfo.timeInfo
    t=datetime.strptime(start,"%Y-%m-%dT%H:%M:%S%z")
    if offset[1]=='-':
        time=t-offset[0]
    else: time=t+delta
    time=time.strftime("%m-%d %-I:%M %p")
    print(time)
    if x['homeTeam']['abbrev']==teaminfo.teamAbv:
        return "Next Game: "+ time[0:5] + " "+time[6:]+" Vs " + x['awayTeam']['abbrev']
    else:
        return "Next Game: "+ time[0:5] + " "+time[6:]+" At " + x['homeTeam']['abbrev']
def lastGame(x):
    if x['homeTeam']['abbrev']==teaminfo.teamAbv:
        favTeam=x['homeTeam']['abbrev']
        favScore=x['homeTeam']['score']
        otherTeam=x['awayTeam']['abbrev']
        otherScore=x['awayTeam']['score']
    else:
        favTeam=x['awayTeam']['abbrev']
        favScore=x['awayTeam']['score']
        otherTeam=x['homeTeam']['abbrev']
        otherScore=x['homeTeam']['score']
    if int(x['periodDesciptor']['number'])==4:
        return "Last Game: "+"F-OT "+teaminfo.teamAbv+" "+str(favScore)+"  "+otherTeam+" "+str(otherScore)
    elif int(x['periodDesciptor']['number'])==5:
        return "Last Game: "+"F-SO "+teaminfo.teamAbv+" "+str(favScore)+"  "+otherTeam+" "+str(otherScore)
    else: "Last Game: "+teaminfo.teamAbv+" "+str(favScore)+"  "+otherTeam+" "+str(otherScore)
def gameProcessing(x):
    if x['homeTeam']['abbrev']==teaminfo.teamAbv:
        home=True
        favTeam=x['homeTeam']['abbrev']
        favScore=x['homeTeam']['score']
        otherTeam=x['awayTeam']['abbrev']
        otherScore=x['awayTeam']['score']
    else:
        home=False
        favTeam=x['awayTeam']['abbrev']
        favScore=x['awayTeam']['score']
        otherTeam=x['homeTeam']['abbrev']
        otherScore=x['homeTeam']['score']
    
        time=x['clock']['timeRemaining']
        period=x['periodDescriptor']['number']
        gameState=x['gameState']
        intermission=x['clock']['inIntermission']
    return home,favTeam,favScore,otherTeam,otherScore,time,period,gameState,intermission
def control():
    x=gameDayCheck()
    x0=x[0]
    x1=x[1]
    x2=x[2]
    if x0==0:
        return 0,gameProcessing(scoreboardCall(x2))
    else: return lastGame(scoreboardCall(x2)),nextGame(scoreboardCall(x1))