MODULE_NAME = "autoparser"

WEEKDAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

DATABASE_BACKUP_1 = "db.old.sqlite3"
DATABASE_BACKUP_2 = "db.old.old.sqlite3"

SCHEDULE_NAME = "schedule.xlsx"
SCHEDULE_BACKUP_1 = "schedule.old.xlsx"
SCHEDULE_BACKUP_2 = "schedule.old.old.xlsx"
SCHEDULE_DOWNLOAD_LINK = "https://docs.google.com/spreadsheets/d/1IOFD7B4rsJZWrqGBU4LZXOCTzLNc3cVP0fMIcmYkmJ8/export?format=xlsx"
SCHEDULE_MIN_SIZE_BYTES = 10 * 1024
SCHEDULE_LAST_COLUMN = 37
SCHEDULE_LAST_ROW = 134
SCHEDULE_TIMETABLES = [
    (1, 9),
    (1, 9),
    (1, 9),
    (1, 9),
    (1, 9),
    # (10, 16),
    # (17, 23),
    # (24, 30),
    # (31, 36),
    # (37, 37),
]

MESSAGE_ERROR_NOTIFY = "Schedule parse error occurred. Please check manually."
MESSAGE_ERROR_PARSE_SYNTAX = "Error during schedule parse with"
MESSAGE_ERROR_UNKNOWN_GROUP = "Unknown group found in schedule"

ADMIN_NOTIFY_TIME = "20:00"
ADMIN_NOTIFY_TABLE_CHANGES = True
