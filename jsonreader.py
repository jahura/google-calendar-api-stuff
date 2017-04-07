import json
from pprint import pprint 

#Get username from calendar ID
def getUser(calendarID):
    for i in range(len(calendarID)):
        if calendarID[i]=='@':
            return calendarID[:i]
    return "praise the sun" #\|T|/

def readJson(path):
    #Load data from json as dictionary
    with open(path) as json_data:
        data=json.load(json_data)
    offset='-05:00'

    #appDate MUST be in yyyy-mm-dd format
    #appTime MUST be in hh:mm:ss form
    #attendees contains a list of emails that the event will be reported to
    title,date,time,attendees=data['message'],data['appDate'],\
            data['appTime'],[]
    
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
    return EVENT,data['id'],username

