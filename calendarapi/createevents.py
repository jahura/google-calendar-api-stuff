
from __future__ import print_function
#from apiclient.discovery import build
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from jsonreader import *
from datetime import datetime
from pytz import timezone

fmt="%Y-%m-%dT%H:%M:%S"

def matchEvent(newEv,oldEv):
    global fmt
    return (newEv['summary']==oldEv['summary']) and\
           (newEv['start']['dateTime']==oldEv['start']['dateTime'])


def getEvents(calendarId,calendar):
    #Maximum number of events get
    MAX_EVENTS=100
    global fmt
    #Minimum time to fetch event
    now=datetime.now(timezone('US/Eastern')).strftime(fmt)+'-05:00'
    eventsResult = calendar.events().list(calendarId=calendarId, 
            timeMin=now, 
            maxResults=MAX_EVENTS, 
            singleEvents=True,
            timeZone='America/Chicago',
            orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

def setEvent(event,calendarId,calendar):
    e = calendar.events().insert(calendarId=calendarId,
        sendNotifications=True, body=event).execute()
    print('''*** %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
        e['start']['dateTime'], e['end']['dateTime']))

def cancelEvent(event,calendarId,calendar):
    print("Fetching event...")
    events=getEvents(calendarId,calendar)
    matched=None
    for i in events:
        if matchEvent(event,i):
            matched=i
            print("Event found")
            print("Canceling event...")
            calendar.events().delete(calendarId=calendarId, 
                    eventId=matched['id']).execute()
            print("Event successfully canceled")
    if matched==None:
        print("No events matched")
        return False
    return True

def updateEvent(event,calendarId,calendar):
    if not cancelEvent(event,calendarId,calendar):
        return
    print("Updating event")
    setEvent(event,calendarId,calendar)
    
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

GMT_OFF = '-07:00'      # PDT/MST/GMT-7

#cases
EVENT,calendarId,command= readJson('json/set') #set
#EVENT,calendarId,command= readJson('json/cancel') #cancle
#EVENT,calendarId,command= readJson('json/rescdule') #reschedule

if command==Command.Set:
    setEvent(EVENT,calendarId,CAL)
elif command==Command.Cancel:
    cancelEvent(EVENT,calendarId,CAL)
else:
    updateEvent(EVENT,calendarId,CAL)
