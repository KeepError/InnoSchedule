import requests
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from modules.electives import permanent, controller


def parse_new_electives_timetable():
    """
    Downloads new electives timetable from the link, and tries to parse it,
    putting parsed to DB. Use wisely! Users are un-enrolled when
    """
    # Download
    new_schedule = requests.get(permanent.ELECTIVE_SCHEDULE_LINK)
    with open(permanent.ELECTIVE_FILE_PATH, 'wb') as f:
        f.write(new_schedule.content)
    # Delete all electives
    controller.delete_electives()
    wb = load_workbook(permanent.ELECTIVE_FILE_PATH, read_only=True)
    for sheet in wb:
        sheet.title
        parse_sheet()


def parse_sheet():
    # Add electives
    pass
