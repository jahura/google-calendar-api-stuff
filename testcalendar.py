
# Project:Reminders and Calender
# Purpose Details: test some of the methods of the createvents.py, jsonreader.py and namegetter.py 
# Course: IST 440_002
# Author: Jahura Ferdous
# Date Developed: 04/26/2017
# Last Date Changed: 05/02/2017

import unittest
from jsonreader import *
from createevents import *
from namegetter import *
import subprocess as sp

#Get event in string version
def toString(command,event):
    return command+event['summary']+event['start']['dateTime']+event['end']['dateTime']

#Generating fake events for testing
#date MUST be in yyyy-mm-dd format
#time MUST be in hh:mm:ss form
def generateEvent(title,date,time):
    offset='-04:00'
    fullTime=date+'T'+time+offset
    event={
        'summary': '%s' % title,
        'start': {'dateTime': '%s' % fullTime},
        'end': {'dateTime': '%s' % fullTime},
        'reminders': {
            'useDefault': 'false',
            'overrides': [
                {
                    'method': 'email',
                    'minutes': 10
                },    
                {
                    'method': 'sms',
                    'minutes': 10
                }    
            ]
        },
        'attendees': []
    }
    return event

EVENT1=generateEvent('Rush B','2017-07-15','14:00:00')
EVENT2=generateEvent('Rush A','2017-07-16','15:00:00')
EVENT3=generateEvent('Rush B','2017-07-16','15:00:00')
EVENT4=generateEvent('Blame lag','2017-07-16','15:00:00')
EVENT5=generateEvent('Spam gg ez','2017-07-16','15:00:00')

EVENT6=generateEvent('Carry team','2017-07-16','15:00:00')
EVENT7=generateEvent('Farming','2017-07-16','15:00:00')
EVENT8=generateEvent('Farming','2017-07-16','16:00:00')

ADD_EVENTS=[EVENT1,EVENT2,EVENT4,EVENT7]
CANCEL_EVENTS=[EVENT2,EVENT4,EVENT6] #Last one should fail
UPDATE_EVENTS=[EVENT3,EVENT8,EVENT5] #Last one should fail

#All test method
#To test method, run 'python -m unittest testcalendar' on the command line

class TestGoogleCalendarAPI(unittest.TestCase):
    #Test get json file from directory
    def test_namegetter(self):
        self.assertTrue(getFile('json/set')=="json/set/set.json")
        self.assertTrue(getFile('json/cancel')=="json/cancel/cancel.json")
        self.assertTrue(getFile('json/rescdule')=="json/rescdule/rescdule.json")

    #Test get json file from full file name
    def test_namegetter2(self):
        self.assertTrue(getFile('json/set/set.json')=="json/set/set.json")
        self.assertTrue(getFile('json/cancel/cancel.json')=="json/cancel/cancel.json")
        self.assertTrue(getFile('json/rescdule/rescdule.json')=="json/rescdule/rescdule.json")

    #Test fail to get json file from directory
    def test_namegetterF(self):
        try:
            self.assertTrue(getFile('json/')=="")
        except:
            pass
            return
        self.fail('Should throw exception')


    #Test get command from json file path
    def test_get_command(self):
        self.assertTrue(getCommand('/lol/gg/l2p/set.json')==Command.Set)
        self.assertTrue(getCommand('cancel.json')==Command.Cancel)
        self.assertTrue(getCommand('.././rescdule.json')==Command.Update)

    #Test fail to get command from json file path
    def test_get_commandF(self):
        try:
            getCommand('.././setx.json')
        except:
            pass
            return
        self.fail('Should throw exception')

    #Test read data from json for set event command
    def test_read_json_set(self):
        event,calendarId,command=readJson('json/set/set.json')
        self.assertTrue(event!=None)
        self.assertTrue(event['summary']!=None)
        self.assertTrue(event['start']!=None)
        self.assertTrue(calendarId=='primary')
        self.assertTrue(command==Command.Set)


    #Test read data from json for cancel event command
    def test_read_json_cancel(self):
        event,calendarId,command=readJson('json/cancel/cancel.json')
        self.assertTrue(event!=None)
        self.assertTrue(event['summary']!=None)
        self.assertTrue(event['start']!=None)
        self.assertTrue(calendarId=='primary')
        self.assertTrue(command==Command.Cancel)

    #Test read data from json for update event command
    def test_read_json_update(self):
        event,calendarId,command=readJson('json/rescdule/rescdule.json')
        self.assertTrue(event!=None)
        self.assertTrue(event['summary']!=None)
        self.assertTrue(event['start']!=None)
        self.assertTrue(calendarId=='primary')
        self.assertTrue(command==Command.Update)

    #Test get service type name
    def test_get_service(self):
        serviceType=sp.check_output(['python createevents.py test'],shell=True)
        self.assertTrue(serviceType in "Resource\n")

    #Test match 2 events
    def test_match_event(self):
        event1,calendarId,command=readJson('json/set/set.json')
        event2,calendarId,command=readJson('json/set/set.json')
        event3,calendarId,command=readJson('json/cancel/cancel.json')
        event4,calendarId,command=readJson('json/rescdule/rescdule.json')
        self.assertTrue(matchEvent(event1,event2))
        self.assertTrue(matchEvent(event3,event4))
    
    #Test add event 1
    def test_add_events1(self):
        status=sp.check_output(['python createevents.py test add 0'],shell=True)
        self.assertTrue(toString('add',ADD_EVENTS[0]) in status)

    #Test add event 2
    def test_add_events2(self):
        status=sp.check_output(['python createevents.py test add 1'],shell=True)
        self.assertTrue(toString('add',ADD_EVENTS[1]) in status)

    #Test add event 3
    def test_add_events3(self):
        status=sp.check_output(['python createevents.py test add 2'],shell=True)
        self.assertTrue(toString('add',ADD_EVENTS[2]) in status)

    #Test add event 4
    def test_add_events4(self):
        status=sp.check_output(['python createevents.py test add 3'],shell=True)
        self.assertTrue(toString('add',ADD_EVENTS[3]) in status)

    #Test cancel event 1
    def test_cancel_events1(self):
        status=sp.check_output(['python createevents.py test cancel 0'],shell=True)
        self.assertTrue(toString('cancel',CANCEL_EVENTS[0]) in status)

    #Test cancel event 2
    def test_cancel_events2(self):
        status=sp.check_output(['python createevents.py test cancel 1'],shell=True)
        self.assertTrue(toString('cancel',CANCEL_EVENTS[1]) in status)

    #Test cancel event 3
    def test_cancel_events3(self):
        status=sp.check_output(['python createevents.py test cancel 2'],shell=True)
        self.assertTrue('No event matched' in status)

    #Test update event 1
    def test_update_events1(self):
        status=sp.check_output(['python createevents.py test update 0'],shell=True)
        self.assertTrue(toString('update',UPDATE_EVENTS[0]) in status)

    #Test update event 2
    def test_update_events2(self):
        status=sp.check_output(['python createevents.py test update 1'],shell=True)
        self.assertTrue(toString('update',UPDATE_EVENTS[1]) in status)

    #Test update event 3
    def test_update_events3(self):
        status=sp.check_output(['python createevents.py test update 2'],shell=True)
        self.assertTrue('No event matched' in status)

