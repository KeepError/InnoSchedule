MODULE_NAME = "autoparser"

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DATABASE_BACKUP_1 = "db.old.sqlite3"
DATABASE_BACKUP_2 = "db.old.old.sqlite3"

SCHEDULE_NAME = "schedule.xlsx"
SCHEDULE_BACKUP_1 = "schedule.old.xlsx"
SCHEDULE_BACKUP_2 = "schedule.old.old.xlsx"
SCHEDULE_DOWNLOAD_LINK = "https://docs.google.com/spreadsheet/ccc?" \
                         "key=1nWzmxw2_OMfGkqfJZIkKBfFpS_gOTPDIEHOrGeYwwOg&output=xlsx"
SCHEDULE_MIN_SIZE_BYTES = 30 * 1024
SCHEDULE_LAST_COLUMN = 27
SCHEDULE_LAST_ROW = 55

MESSAGE_ERROR_NOTIFY = "Schedule parse error occurred. Please check manually."
MESSAGE_ERROR_PARSE_SYNTAX = "Error during schedule parse with"

ADMIN_NOTIFY_TIME = "20:00"
