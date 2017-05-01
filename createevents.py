
# Project:Reminders and Calender
# Purpose Details: Read json file from the given directory and then decide whehter to set/cancel/reschedule event based on the file found
# Course: IST 440_002
# Author: Jahura Ferdous
# Date Developed: 03/15/2017
# Last Date Changed: 04/26/2017

from __future__ import print_function
#from apiclient.discovery import build
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from jsonreader import *
from datetime import datetime
import sys
import logging as lg

#Date time format
fmt="%Y-%m-%dT%H:%M:%S"
#Check if the user is testing
isTest=False

#Compare date between target event and saved event
def matchEvent(newEv,oldEv):
    global fmt
    return (newEv['summary']==oldEv['summary']) and\
           (newEv['start']['dateTime']==oldEv['start']['dateTime'])

#Fetch and return events list from calendar
def getEvents(calendarId,calendar):
    #Maximum number of events get
    MAX_EVENTS=100
    global fmt
    #Minimum time to fetch event
    now = datetime.utcnow().isoformat() + 'Z'
    lg.debug('Fetching events from calendar...')
    try:
        eventsResult= calendar.events().list(calendarId=calendarId, 
                timeMin=now, 
                maxResults=MAX_EVENTS, 
                singleEvents=True,
                timeZone='America/New_York',
                orderBy='startTime').execute()
        events=eventsResult.get('items',[])
    except:
        lg.error('Error fetching events from calendar...')
        exit(1)
    lg.debug('Sucessfully fetching events')
    for ev in events:
        print(ev['summary'],ev['end']['dateTime'])
        lg.debug('{0} {1} {2}'.format(ev["summary"],ev["start"]["dateTime"],ev["end"]["dateTime"]))
    return events

#Add new event to calendar
def setEvent(event,calendarId,calendar):
    lg.debug('Adding events to calendar...')
    try:
        e = calendar.events().insert(calendarId=calendarId,
            sendNotifications=True, body=event).execute()
    except:
        lg.error('Error adding event to calendar...')
        exit(1)
    lg.debug('Successfully add event to calendar...')
    lg.debug('{0} {1} {2}'.format(e["summary"],e["start"]["dateTime"],e["end"]["dateTime"]))
    print(tc.toString('add',event))
    print('''*** %r event added:
    Start: %s
    End:   %s''' % (e['summary'].encode('utf-8'),
        e['start']['dateTime'], e['end']['dateTime']))

#Cancel event on calendar
def cancelEvent(event,calendarId,calendar,matchNameOnly):
    print("Fetching event...")
    events=getEvents(calendarId,calendar)
    matched=None
    lg.debug('Find matching events...')
    for i in events:
        if matchEvent(event,i) or \
                (matchNameOnly and event['summary']==i['summary']):
            matched=i
            lg.debug('Event match found')
            lg.debug('Canceling event...')
            print("Event found")
            print("Canceling event...")
            try:
                calendar.events().delete(calendarId=calendarId, 
                        eventId=matched['id']).execute()
            except:
                lg.error('Error canceling event on calendar...')
                exit(1)
            print("Successfully canceling event...")
            print("Event successfully canceled")
            print(tc.toString('cancel',event))
    if matched==None:
        lg.debug('No event matched')
        print("No event matched")
        return False
    return True

#Reschedule event on calendar
def updateEvent(event,calendarId,calendar):
    if not cancelEvent(event,calendarId,calendar,True):
        return
    print("Updating event")
    setEvent(event,calendarId,calendar)
    print(tc.toString('update',event))

#Get google api calendar service
def getService():
    try:
        global isTest
        import argparse
        if not isTest:
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        else:
            flags=None
    except ImportError:
        flags = None
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
    srvc = build('calendar', 'v3', http=creds.authorize(Http()))
    return srvc

#Print service type --> For testing
def printService():
    service=getService()
    print(type(service).__name__)

#For testing
def testEventManipulation():
    lg.basicConfig(filename='calendarapi.log',level=lg.DEBUG)
    service=getService()
    if sys.argv[2]=='add':
        setEvent(tc.ADD_EVENTS[int(sys.argv[3])],'primary',service)
    elif sys.argv[2]=='cancel':
        cancelEvent(tc.CANCEL_EVENTS[int(sys.argv[3])],'primary',service,False)
    elif sys.argv[2]=='update':
        updateEvent(tc.UPDATE_EVENTS[int(sys.argv[3])],'primary',service)

#Main function
def main():
    lg.basicConfig(filename='calendarapi.log',level=lg.DEBUG)
    try:
        lg.debug('Fetching service...')
        service=getService()
    except:
        lg.error('Error fetching service')
        exit(1)
    lg.debug('Successfully fetch service')
    '''


    This program is desgined to fetch data of only one json file at a specific
    directory and then delete it. To test each command below, comment out the
    other two.


    '''
    lg.debug('Finding json files...')
    try:    
        EVENT,calendarId,command= readJson('json/set') #set
        #EVENT,calendarId,command= readJson('json/cancel') #cancle
        #EVENT,calendarId,command= readJson('json/rescdule') #reschedule
    except:
        lg.error('error fetching json file')
        exit(1)
    lg.debug('Json file found')
    lg.debug('Command id get: %s' % command)
    lg.debug('Eventget: %s' % EVENT)
    if command==Command.Set:
        setEvent(EVENT,calendarId,service)
    elif command==Command.Cancel:
        cancelEvent(EVENT,calendarId,service,False)
    else:
        updateEvent(EVENT,calendarId,service)

#Run this only when 'python createevents.py' command is
if __name__=="__main__":
    numArgs=len(sys.argv)
    if numArgs==1:
        main()
    elif numArgs==2 and sys.argv[1]=='test':
        isTest=True
        printService()
    elif sys.argv[1]=='test' and numArgs==4:
        isTest=True
        testEventManipulation()
