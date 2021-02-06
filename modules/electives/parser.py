"""
This module contains all necessary functions to parse electives schedule.
"""
from typing import List, Union, Dict

import requests
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from modules.electives import permanent, controller
from modules.electives.classes import Elective, ElectiveLesson


def parse_new_electives_timetable():
    """
    Downloads new electives timetable from the link, and tries to parse it,
    putting parsed to DB. Use wisely! Users are un-enrolled when it is called
    """
    # Download
    new_schedule = requests.get(permanent.ELECTIVE_SCHEDULE_LINK)
    with open(permanent.ELECTIVE_FILE_PATH, 'wb') as f:
        f.write(new_schedule.content)
    # Delete all electives
    controller.delete_electives()
    wb = load_workbook(permanent.ELECTIVE_FILE_PATH, read_only=True)
    for sheet in wb:
        electives = find_electives(sheet)


def find_electives(sheet: Worksheet) -> List[Elective]:
    """
    Finds definition of all electives on given sheet
    """

    def strip_none(string: Union[str, None]) -> str:
        """
        Call str.strip(), if string is supplied as argument
        If argument is None, return empty string
        """
        if string is None:
            return ""
        return string.strip()

    def first_nonempty_row() -> int:
        columns = permanent.ELECTIVE_DEFINITION_COLUMNS.values()
        row = 2
        while True:
            values = [sheet.cell(row, col).value for col in columns]
            values = [strip_none(val) for val in values]
            if all(len(part) != 0 for part in values):
                return row
            row += 1

    group = sheet.title
    result = []
    electives_remain = True
    cursor_row = first_nonempty_row()
    while electives_remain:
        name = sheet.cell(cursor_row, permanent.ELECTIVE_DEFINITION_COLUMNS["name"]).value
        teacher = sheet.cell(cursor_row,
                             permanent.ELECTIVE_DEFINITION_COLUMNS["teacher"]).value
        acronym = sheet.cell(cursor_row,
                             permanent.ELECTIVE_DEFINITION_COLUMNS["acronym"]).value
        data = list(map(strip_none, [name, teacher, acronym]))
        if all(len(part) != 0 for part in data):
            result.append(Elective(*data[:3], group))
            cursor_row += 1
        else:
            electives_remain = False
    return result


def find_lessons(sheet: Worksheet) -> Dict[str, List[ElectiveLesson]]:
    pass
