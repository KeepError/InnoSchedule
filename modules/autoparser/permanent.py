MODULE_NAME = "autoparser"

WEEKDAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

DATABASE_BACKUP_1 = "db.old.sqlite3"
DATABASE_BACKUP_2 = "db.old.old.sqlite3"

SCHEDULE_NAME = "schedule.xlsx"
SCHEDULE_BACKUP_1 = "schedule.old.xlsx"
SCHEDULE_BACKUP_2 = "schedule.old.old.xlsx"
SCHEDULE_DOWNLOAD_LINK = "https://docs.google.com/spreadsheet/ccc?" \
                         "key=1wbfE26tAionZMKUWoMsir_ldC5IocmhG8kE8PrTP0WA&output=xlsx"
SCHEDULE_MIN_SIZE_BYTES = 30 * 1024
SCHEDULE_LAST_COLUMN = 36
SCHEDULE_LAST_ROW = 134

MESSAGE_ERROR_NOTIFY = "Schedule parse error occurred. Please check manually."
MESSAGE_ERROR_PARSE_SYNTAX = "Error during schedule parse with"
MESSAGE_ERROR_UNKNOWN_GROUP = "Unknown group found in schedule"

ADMIN_NOTIFY_TIME = "20:00"
