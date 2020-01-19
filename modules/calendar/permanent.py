from datetime import date
from pytz import timezone

MODULE_NAME = "calendar"
TIMEZONE = timezone("Europe/Moscow")

SEMESTER_START = date(year=2020, month=1, day=20)
SEMESTER_LENGTH = 15  # number of weeks
WEEK_LENGTH = 7  # 7 days in a week

ICS_STORAGE = "modules/calendar/ics"

MESSAGE_STORAGE_CLEARED = "Cleared all ics"
