from datetime import datetime, timedelta
from random import random, seed
from os.path import exists
from os import mkdir, remove
from typing import List

from icalendar import Calendar, Event, Timezone, TimezoneStandard, vRecur, vDatetime

from modules.core.source import bot, log
from modules.calendar import controller, permanent
from modules.electives.classes import Elective
from modules.electives.controller import get_electives_of_user_id, get_lessons_of_elective
import modules.schedule.permanent as schedule_constants
from modules.schedule.source import main_markup

"""
Module translates the schedule to an ics file. Can be used as an alternative to Schedule Assistant

Author's telegram @Winner_OK
Author's github: @WinnerOK
"""


def attach_calendar_module():
    day_abbreviation = {
        0: "MO",
        1: "TU",
        2: "WE",
        3: "TH",
        4: "FR",
        5: "SA",
        6: "SU",
    }

    def create_storage():
        if not exists(permanent.ICS_STORAGE):
            mkdir(permanent.ICS_STORAGE)

    def generate_calendar(groups: List[str], electives: List[Elective]) -> str:
        """
        Generates an ics for a group.
        """
        if not groups:
            raise ValueError("group must be non-empty list of strings")
        path = f"{permanent.ICS_STORAGE}/{'_'.join(groups)}.ics"
        seed()
        c = Calendar()
        c.add('prodid', 'InnoSchedule bot')
        c.add('version', '2.0')

        # reference: https://github.com/collective/icalendar/blob/master/src/icalendar/tests/test_timezoned.py
        tz = Timezone()
        tz.add('tzid', permanent.TIMEZONE)
        tz.add('x-lic-location', permanent.TIMEZONE)

        tzs = TimezoneStandard()
        dt = datetime.now(permanent.TIMEZONE)
        tzs.add('tzname', dt.strftime("%Z"))
        tzs.add('TZOFFSETFROM', permanent.TIMEZONE.utcoffset(datetime.now()))
        tzs.add('TZOFFSETTO', permanent.TIMEZONE.utcoffset(datetime.now()))

        tz.add_component(tzs)
        c.add_component(tz)

        for day in range(permanent.WEEK_LENGTH):
            for group in groups:
                is_module = group not in schedule_constants.REGISTERED_COURSES["B21"] and group not in \
                            schedule_constants.REGISTERED_COURSES["B20"]
                current_day = (permanent.MODULE_SEMESTER_START if is_module else permanent.SEMESTER_START) + timedelta(
                    days=day)
                lessons = controller.get_lessons(group, current_day.weekday())
                if len(lessons) != 0:
                    for lesson in lessons:
                        event = Event()
                        event.add('summary', f"{lesson.subject} with {lesson.teacher}")
                        event.add("dtstart", vDatetime(
                            datetime.combine(current_day, lesson.start_struct.time(), tzinfo=permanent.TIMEZONE)))
                        event.add("dtend", vDatetime(
                            datetime.combine(current_day, lesson.end_struct.time(), tzinfo=permanent.TIMEZONE)))
                        event.add('dtstamp', vDatetime(datetime.now(permanent.TIMEZONE)))
                        event.add("rrule", vRecur(freq="WEEKLY", byday=day_abbreviation[current_day.weekday()],
                                                  interval=1,
                                                  count=permanent.MODULE_SEMESTER_LENGTH if is_module else permanent.SEMESTER_LENGTH))
                        event.add("uid", f"{vDatetime(datetime.now()).to_ical().decode()}-{random()}")
                        event.add("location", f"room #{lesson.room}")
                        c.add_component(event)

        for elective in electives:
            lessons = get_lessons_of_elective(elective.id)
            for lesson in lessons:
                event = Event()
                event.add('summary', f"{elective.name} in room {lesson.room}")
                event.add("dtstart", vDatetime(
                    permanent.TIMEZONE.localize(lesson.date_time)))
                event.add("dtend", vDatetime(
                    permanent.TIMEZONE.localize(lesson.date_time + timedelta(hours=1, minutes=30))))
                event.add('dtstamp', vDatetime(datetime.now(permanent.TIMEZONE)))
                event.add("uid", f"{vDatetime(datetime.now()).to_ical().decode()}-{random()}")
                event.add("location", f"room #{lesson.room}")
                c.add_component(event)
        with open(path, "wb") as f:
            f.write(c.to_ical())
        return path

    @bot.message_handler(commands=['ics'])
    def get_ics(message):
        log(permanent.MODULE_NAME, message)
        user_id = message.from_user.id
        groups = controller.get_groups(user_id)
        electives = get_electives_of_user_id(user_id)
        if groups is None or len(groups) <= 0:
            bot.send_message(user_id, schedule_constants.MESSAGE_USER_NOT_CONFIGURED)
            return
        filepath = generate_calendar(groups, electives)
        with open(filepath, 'rb') as document:
            bot.send_document(user_id, document, reply_markup=main_markup)
        remove(filepath)

    create_storage()
