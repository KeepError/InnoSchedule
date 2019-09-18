import functools
import logging
from logging.handlers import RotatingFileHandler
import threading
import time

import telebot
import schedule
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from modules.core import permanent
from modules.admin.permanent import SUPERADMIN_LIST, token  # private bot token
from modules.schedule.permanent import TEXT_BUTTON_NOW, TEXT_BUTTON_DAY, TEXT_BUTTON_WEEK

"""
Main core module
All necessary base for other modules is defined here:
    - telegram work
    - logging
    - markups (main buttons)
    - db work
Contains basic commands (e.g. /help) and start listening after all modules are attached

Author: @Nmikriukov
"""

bot = telebot.TeleBot(token)
# Save step handlers in file and load in case of restart; Has some bug
# bot.enable_save_next_step_handlers()
# bot.load_next_step_handlers()

# main three buttons are declared here
main_markup = telebot.types.ReplyKeyboardMarkup(True)
main_markup.add(TEXT_BUTTON_NOW, TEXT_BUTTON_DAY, TEXT_BUTTON_WEEK)

# log configuration
logger = logging.getLogger(permanent.LOG_NAME)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(permanent.LOG_FILE_NAME, maxBytes=permanent.LOG_MAX_SIZE_BYTES,
                              backupCount=permanent.LOG_BACKUP_COUNT)
handler.setFormatter(logging.Formatter(permanent.LOG_MESSAGE_FORMAT, permanent.LOG_DATE_FORMAT))
logger.addHandler(handler)


def log(module, message):
    """
    Write log info about message to file in format:
    date :: time :: module_name :: user_alias :: message_text
    String's length is extended to static length due to visual intelligibility
    """
    # log id of user if no alias exist
    if message.from_user.username:
        user = message.from_user.username
    else:
        user = str(message.from_user.id)
    logger.info(f"{module.rjust(15)} :: {user.rjust(20)} :: "
                f"{message.text if message.text else '--not_text--'}")


# sqlalchemy base for classes declaration and mapping to tables
Base = declarative_base()
# default connection pool size is 5
db_engine = create_engine(f"sqlite:///{permanent.DATABASE_FOLDER}/{permanent.DATABASE_NAME}")
# allows to receive connections from pool
Session = sessionmaker(bind=db_engine)


# decorator to give function session for db read and close connection
def db_read(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        session = Session()
        ret = function(session, *args, **kwargs)
        session.close()
        return ret
    return wrapper


# decorator to give function session for db write, commit and close connection
def db_write(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        session = Session()
        ret = function(session, *args, **kwargs)
        session.commit()
        session.close()
        return ret
    return wrapper


# should be done after all db imports done
from modules.schedule.controller import get_user


def attach_core_module():

    @bot.message_handler(commands=['start', 'help'])
    def core_command_handler(message):
        """
        Basic commands are defined here
        """
        log(permanent.MODULE_NAME, message)
        if message.text == "/start":
            bot.send_message(message.chat.id, permanent.MESSAGE_HI, reply_markup=main_markup)
        elif message.text == "/help":
            bot.send_message(message.chat.id, permanent.MESSAGE_HELP, reply_markup=main_markup)


def compose_attached_modules(set_proxy=False):

    @bot.message_handler()
    def garbage_message_handler(message):
        """
        Handler for any other unknown messages
        Defined when all other modules already defined their handlers
        """
        log(permanent.MODULE_NAME, message)
        # show main buttons if unknown input sent
        bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
        alias = get_user(message.from_user.id).alias
        if ' ' in message.text:
            for admin in SUPERADMIN_LIST:
                bot.send_message(admin, f"{permanent.MESSAGE_UNKNOWN} {str(alias)}:\n{message.text}")

    # set proxy if needed (thx ro roskomnadzor)
    if set_proxy:
        telebot.apihelper.proxy = {
            permanent.PROXY_PROTOCOL: f'{permanent.PROXY_SOCKS}://{permanent.PROXY_LOGIN}:'
                                      f'{permanent.PROXY_PASSWORD}@{permanent.PROXY_ADDRESS}:{permanent.PROXY_PORT}'}

    def pending():
        """
        Function is running in background thread and wake schedule to check if some action should be made
        """
        while 1:
            schedule.run_pending()
            time.sleep(30)

    # start pending to wake up when needed to make some action
    # daemon=True means die if main thread dies
    threading.Thread(target=pending, daemon=True).start()

    # ensure database schema is correct
    Base.metadata.create_all(db_engine)

    # start listening for user`s messages
    bot.polling(none_stop=False, timeout=50)
