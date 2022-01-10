# csv-to-calendar

Upload CSV timetable to Google Calendar. Pretty much the same as
the [Importing Calendar Events from CSV to Google Calendar](https://support.google.com/calendar/answer/37118), but automatically.

## Setup and Usage

### Setup

1. Get an api key. See: [oauth](https://developers.google.com/calendar/api/guides/auth)
2. Download it to `.client_secret.json`

### Usage

1. Modify the `timetable.csv` template using an editor.
    - Do not place text outside the allocated time slots
2. Run `pip install -r requirements.txt` to install all the dependencies.
3. Run `python upload.py`
    - Will open webpage to get token
    - Token saved in `~/.credentials/calendar-python-quickstart.json`
    - Will parse the csv and upload events accordingly

## Features

### Auth

- Opens browser to get Google OAuth token
- Saves token to `~/.credentials/calendar-python-quickstart.json` for future use (might want to delete this file after
  use)

### CSV

- Parse from CSV template. See `timetable.csv` for an example. See
  also: [Importing Calendar Events from CSV to Google Calendar](https://it.stonybrook.edu/help/kb/importing-calendar-events-from-csv-to-google-calendar)

### Calendar

- ~~Will operate on the calendar named 'csv-to-calendar'~~
- ~~Everytime `upload.py` is run it will be cleared or created if it does not exist~~
- Will operate on the calendar of your choice
- The csv will have an ID, that will be appended to the description of each event and will be used for syncing
- Events will be synchronized with the CSV template, using the following rules:
    - If the event already exists, it will be updated
    - If the event does not exist, it will be created
    - If the event is not in the CSV template, it will be deleted

### Events

- ~~Recur weekly until `2017-11-02~~
- Notification 15 minutes before each event

## Warning

This script requests Read/Write access to your calendar. If used incorrectly it may delete all the calendars/events on
your account.
