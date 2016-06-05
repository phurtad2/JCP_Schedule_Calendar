from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
from jcpcrawler import week_schedules, string_date
from oauth2client import client
from oauth2client import tools

import datetime

def rf(d, t, GMT):
    return str(d + 'T' + t + ':00' + GMT)

def set_work_cal(n):
    print("Extracting Schedule...")
    sch =week_schedules(int(n))
    print("Extraction Complete!")
    #Example Schedule
    #sch = {'2016-06-07': ('09:45', '15:30'), '2016-06-10': ('12:00', '18:00'), '2016-06-05': ('10:00', '14:00'),
    # '2016-06-03': ('17:00', '22:00'), '2016-06-11': ('11:00', '19:00'),
    # '2016-06-06': ('18:00', '21:45'), '2016-06-08': ('11:00', '17:00')}

    t = datetime.datetime.now()

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
                if flags else tools.run(flow, store)
    CAL = build('calendar', 'v3', http=creds.authorize(Http()))

    GMT_OFF = '-05:00'      # PDT/MST/GMT-7
    workCal = '33tq30updcfnp7j7kr1p274brs@group.calendar.google.com'

    #Deletes all previous work events to make room for new events (to prevent overlapping)

    events = CAL.events().list(calendarId= workCal,
                                   timeMin=rf(string_date(t), '00:00', GMT_OFF),
                                   timeMax=rf(string_date(t + datetime.timedelta(weeks=4)), '00:00', GMT_OFF),
                                   singleEvents=True).execute()
    print("Deleting previous schedules added by program...")
    for event in events['items']:
        if 'description' in event.keys() and 'jcp_weekly' in event['description']:
            CAL.events().delete(calendarId=workCal, eventId=event['id']).execute()
        else:
            pass

    print("Adding newly extracted schedule...")
    for key in sch:
        start = rf(str(key), sch[key][0], GMT_OFF)
        end = rf(str(key), sch[key][1], GMT_OFF)
        EVENT = {
            'summary': 'Work',
            'description' : 'Work at JCPenney\'s (automatically added with jcp_weekly)',
            'start':  {
                       'dateTime': start,
                       'timeZone': 'America/Chicago'
            },
            'end':    {'dateTime': end,
                       'timeZone': 'America/Chicago'
            },
            'background': '#aaaaaa',
            'foreground': "#abcde1",
            'reminders':    {
                'useDefault': False,
                'overrides': [
                  {
                  'method': 'popup', 'minutes': 60}]
            }
        }

        CAL.events().insert(calendarId=workCal,
                sendNotifications=True, body=EVENT).execute()
