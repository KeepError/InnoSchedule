MODULE_NAME = "core"
DATABASE_FOLDER = "modules/admin/db"
DATABASE_NAME = "db.sqlite3"

LOG_FILE_NAME = 'log'
LOG_MAX_SIZE_BYTES = 1024 * 1024 * 10  # 10 MB
LOG_NAME = 'logger'
LOG_BACKUP_COUNT = 1
LOG_MESSAGE_FORMAT = "%(asctime)s :: %(message)s"
LOG_DATE_FORMAT = "%d.%m.%Y :: %H:%M:%S"

PROXY_PROTOCOL = 'https'
PROXY_SOCKS = 'socks5'
PROXY_LOGIN = '356819408'
PROXY_PASSWORD = 'nya8e4Es'
PROXY_ADDRESS = 'deimos.public.opennetwork.cc'
PROXY_PORT = '1090'

MESSAGE_HI = "Hi there!✋"
MESSAGE_HELP = "Schedule open platform for Innopolis students.\n\n" \
               "Some commands, that might be useful for you:\n" \
               "/configure_schedule - change group settings\n" \
               "/configure_remind - change reminders settings\n" \
               "/friend - show current and next friend's lessons\n" \
               "   or you can just send his alias directly\n" \
               "/ics - download schedule as an ics file\n" \
               "/help\n\n" \
               "Anyone could easily add his own functionality:\n" \
               "https://gitlab.com/Louie_ru/InnoSchedule\n" \
               "Original creators: @Nmikriukov @thedownhill\n" \
               "Now maintained by @artembakhanov"
MESSAGE_ERROR = "Sorry, I did not understand you"
MESSAGE_UNKNOWN = "Unknown message from"
