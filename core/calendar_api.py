from __future__ import print_function

import os

from oauth2client import client, tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at .credentials/calendar-python-quickstart.json
SCOPES = "https://www.googleapis.com/auth/calendar"
# CLIENT_SECRET_FILE = os.path.abspath(os.path.join(os.pardir, '.client_secret.json'))
CLIENT_SECRET_FILE = ".client_secret.json"
APPLICATION_NAME = "CSV to Calendar"


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.curdir
    credential_dir = os.path.join(home_dir, ".credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "calendar-python-quickstart.json")

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print("Storing credentials to " + credential_path)
    return credentials


def get_calendar_id(service, calendar_summary):
    """
    Returns the calendar id of the calendar with the given summary
    """
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            if calendar_list_entry["summary"] == calendar_summary:
                return calendar_list_entry["id"]
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break

    return None


def init_calendar(service, summary):
    from core.upload import TIMEZONE

    # If summary does not start with `csv_`, raise an error, for security reasons
    if not summary.startswith("csv-"):
        raise Exception("Invalid calendar name")

    pre_existing_calender_id = get_calendar_id(service, summary)
    if pre_existing_calender_id is not None:
        service.calendars().delete(calendarId=pre_existing_calender_id).execute()
        print("Calendar " + summary + " has been deleted")
    newly_created_calendar = (
        service.calendars()
        .insert(body={"summary": summary, "timeZone": TIMEZONE})
        .execute()
    )
    print("Calendar " + summary + " has been created")
    return newly_created_calendar["id"]


def upload_event(service, event, calender_id):
    print("Creating event... " + event["summary"] + " @ " + event["start"]["dateTime"])
    service.events().insert(calendarId=calender_id, body=event).execute()
    print("Event created!")
