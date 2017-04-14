## Files information

- `client_secret.json`: contains client credidentials and allow the createevent.py to authenticate user's gmail account with the application (DON'T EDIT).
- `storage.json`: file made after running the createvents.py (DON'T EDIT)
- `json/event2.json`: sample data containing event and calendar information.
- `jsonreader.py`: python file containing method that can get data such as calendar id, message, date, time from `event2.json` and similar event files. This file is imported by createevents.py to get data from event2.json file.
- `createevents.py`: python file that is used to create an event with the information get from event2.json file (line 25).
