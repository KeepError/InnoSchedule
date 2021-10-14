from datetime import date
from pytz import timezone

MODULE_NAME = "calendar"
TIMEZONE = timezone("Europe/Moscow")

MODULE_SEMESTER_START = date(year=2021, month=10, day=14) # forth and third year students
MODULE_SEMESTER_LENGTH = 9  # number of weeks

SEMESTER_START = date(year=2021, month=8, day=16) # first and second year students
SEMESTER_LENGTH = 15  # number of weeks

WEEK_LENGTH = 7  # 7 days in a week

ICS_STORAGE = "modules/calendar/ics"

MESSAGE_STORAGE_CLEARED = "Cleared all ics"
