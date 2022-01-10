from __future__ import print_function

import os

import httplib2
import tzlocal
from apiclient import discovery

from core import calendar_api, parsing, utils

TIMEZONE = tzlocal.get_localzone_name()
CALENDAR_NAME = "csv-to-calendar"
TIMETABLE_CSV_PATH = "csv_2_google.csv"
EXCEL_FILE_NAME = "csv_2_google.xlsx"
CLEAN_AFTER = True


def main():
    credentials = calendar_api.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    calendar_id = calendar_api.init_calendar(service, CALENDAR_NAME)

    temp_excel_file = "_" + EXCEL_FILE_NAME
    assert EXCEL_FILE_NAME in os.listdir(".")
    utils.copy_file(EXCEL_FILE_NAME, temp_excel_file)
    utils.remove_all_pages_but_first(temp_excel_file)
    utils.xlsx_to_csv(temp_excel_file, TIMETABLE_CSV_PATH)

    items = parsing.get_items_from_csv(TIMETABLE_CSV_PATH)
    if CLEAN_AFTER:
        utils.remove_file(temp_excel_file)
        utils.remove_file(TIMETABLE_CSV_PATH)
    events = parsing.parse_items_into_events(items)

    for event in events:
        calendar_api.upload_event(service, event, calendar_id)
