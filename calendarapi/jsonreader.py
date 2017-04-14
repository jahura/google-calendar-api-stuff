import json
from pprint import pprint 

from namegetter import getFile

#Available commands
class Command:
    Set,Cancel,Update=range(3)

#Get username from calendar ID
def getUser(calendarID):
    for i in range(len(calendarID)):
        if calendarID[i]=='@':
            return calendarID[:i]
    return "praise the sun" #\|T|/

#Get command from file name
def getCommand(filePath):
    command=filePath.split("/")[-1][:-5]
    print(filePath,command)
    if command=="set":
        return Command.Set
    elif command=="cancel":
        return Command.Cancel
    elif command=="rescdule":
        return Command.Update
    else:
        raise Exception("Command unidentitfied")

def readJson(path):
    fileName=getFile(path)
    #Load data from json as dictionary
    with open(fileName) as json_data:
        data=json.load(json_data)
    offset='-05:00'
    #appDate MUST be in yyyy-mm-dd format
    #appTime MUST be in hh:mm:ss form
    #attendees contains a list of emails that the event will be reported to
    title,date,time,attendees=data['message'],data['date'],\
            data['time'],[]
    
    fullTime=date+'T'+time+offset
    username=getUser(data['id'])
    if title==None or title=='':
        title='No title'

    #Event object
    EVENT={
        'summary': '%s' % title,
        'start': {'dateTime': '%s' % fullTime},
        'end': {'dateTime': '%s' % fullTime},
        'attendees': []
    }

    for i in attendees:
        EVENT['attendees'].append({'email': '%s' % i})
    return EVENT,data['id'],getCommand(fileName)

