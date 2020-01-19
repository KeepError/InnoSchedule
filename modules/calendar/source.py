from datetime import datetime, timedelta
from random import random, seed
from os.path import exists
from os import mkdir
import shutil

from icalendar import Calendar, Event, Timezone, TimezoneStandard, vRecur, vDatetime

from modules.core.source import bot, log
from modules.calendar import controller, permanent
import modules.schedule.permanent as schedule_constants
from modules.schedule.source import main_markup
from modules.admin.permanent import ADMIN_LIST

"""
Module translates the schedule to an ics file. Can be used as an alternative to Schedule Assistant

Author's telegram @Winner_OK
Author's github: @WinnerOK
"""

day_abbreviation = {
    0: "MO",
    1: "TU",
    2: "WE",
    3: "TH",
    4: "FR",
    5: "SA",
    6: "SU",
}


def generate_calendar(group: str):
    """
    Generates an ics for a group.
    """
    if not group:
        raise ValueError("group must be non-null value")
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
        current_day = permanent.SEMESTER_START + timedelta(days=day)
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
                                          interval=1, count=permanent.SEMESTER_LENGTH))
                event.add("uid", f"{vDatetime(datetime.now()).to_ical().decode()}-{random()}")
                event.add("location", f"room #{lesson.room}")
                c.add_component(event)
    with open(f"{permanent.ICS_STORAGE}/{group}.ics", "wb") as f:
        f.write(c.to_ical())


def attach_calendar_module():
    def create_storage():
        if not exists(permanent.ICS_STORAGE):
            mkdir(permanent.ICS_STORAGE)

    def send_calendar(user_id: int):
        groups = controller.get_groups(user_id)
        if groups is None:
            bot.send_message(user_id, schedule_constants.MESSAGE_USER_NOT_CONFIGURED)
            return
        for group in groups:
            calendar = f"{permanent.ICS_STORAGE}/{group}.ics"
            if not exists(calendar):
                generate_calendar(group)

            with open(calendar, 'rb') as f:
                bot.send_document(user_id, f, reply_markup=main_markup)

    @bot.message_handler(commands=['ics'])
    def get_ics(message):
        log(permanent.MODULE_NAME, message)
        user_id = message.from_user.id
        send_calendar(user_id)

    @bot.message_handler(commands=['ics_clear'])
    def clear_ics(message):
        """
        Clear all created ics
        """
        if message.from_user.id in ADMIN_LIST:
            log(permanent.MODULE_NAME, message)
            shutil.rmtree(permanent.ICS_STORAGE)
            create_storage()
            bot.send_message(message.from_user.id, permanent.MESSAGE_STORAGE_CLEARED)

    create_storage()
