MODULE_NAME = "autoparser"

WEEKDAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

DATABASE_BACKUP_1 = "db.old.sqlite3"
DATABASE_BACKUP_2 = "db.old.old.sqlite3"

SCHEDULE_NAME = "schedule.xlsx"
SCHEDULE_BACKUP_1 = "schedule.old.xlsx"
SCHEDULE_BACKUP_2 = "schedule.old.old.xlsx"
# SCHEDULE_DOWNLOAD_LINK = "https://docs.google.com/spreadsheet/ccc?" \
# "key=1H3SYKtt1_E_kqJ9REG9hWAJskpSDTrRKHe6tSglv5_0&output=xlsx"
# SCHEDULE_DOWNLOAD_LINK = "https://docs.google.com/spreadsheets/d/18OglpLQk7Jfrta93bLw0gJIttbcDdzZPT5K-avFM0Pc/export?format=xlsx"
SCHEDULE_DOWNLOAD_LINK = "https://docs.google.com/spreadsheets/d/1pWWCBSRzeUvxrgiskFkT0zMuW-urIkZGc7vx1jCmYFQ/export?format=xlsx"
SCHEDULE_MIN_SIZE_BYTES = 10 * 1024
SCHEDULE_LAST_COLUMN = 36
SCHEDULE_LAST_ROW = 134
SCHEDULE_TIMETABLES = [
    (23, 26),
    (15, 22),
    (8, 14),
    (1, 7),
    (23, 26)
]

MESSAGE_ERROR_NOTIFY = "Schedule parse error occurred. Please check manually."
MESSAGE_ERROR_PARSE_SYNTAX = "Error during schedule parse with"
MESSAGE_ERROR_UNKNOWN_GROUP = "Unknown group found in schedule"

ADMIN_NOTIFY_TIME = "20:00"
ADMIN_NOTIFY_TABLE_CHANGES = True
