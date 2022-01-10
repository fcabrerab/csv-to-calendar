from __future__ import print_function

import csv
import datetime


def get_items_from_csv(csv_file):
    headers_mapping = {
        "Subject": "subject",
        "Start Date": "start_date",
        "Start Time": "start_time",
        "End Date": "end_date",
        "End Time": "end_time",
        "All day event": "all_day_event",
        "Description": "description",
        "Location": "location",
    }

    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        items = [[col for col in row] for row in reader if row[0]]
        headers = items.pop(0)
        # Now, we replace the headers with the ones we want
        for i in range(len(headers)):
            if headers[i] in headers_mapping:
                headers[i] = headers_mapping[headers[i]]

        items = [dict(zip(headers, item)) for item in items]
        return items


def parse_items_into_events(items):
    events = []
    for item in items:
        try:
            event = create_event(
                start_datetime=combine_date_and_time(
                    item["start_date"], item["start_time"]
                ),
                end_datetime=combine_date_and_time(item["end_date"], item["end_time"]),
                subject=item["subject"],
                location=item["location"],
            )
            events.append(event)
        except Exception as e:
            print(f"Error parsing item {item}")
            print(e)
    return events


def combine_date_and_time(date, time):
    return (
        datetime.datetime.strptime(f"{date.split(' ')[0]} {time}", "%Y-%m-%d %H:%M:%S")
        .astimezone()
        .isoformat()
    )


def create_event(
    start_datetime,
    end_datetime,
    subject,
    location,
):
    from core.upload import TIMEZONE

    return {
        "summary": subject,
        "location": location,
        "start": {
            "dateTime": start_datetime,
            "timeZone": TIMEZONE,
        },
        "end": {"dateTime": end_datetime, "timeZone": TIMEZONE},
    }
