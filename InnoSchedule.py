#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import telebot

from modules import lesson_controller
from modules import user_controller
from modules import reminder
from modules.admin_module import register_admin_commands
from settings.token import token  # private bot token
from settings import config
from settings import strings

"""
Main InnoSchedule source
All user interaction through telegram is written here
"""

# log configuration
logger = logging.getLogger(config.LOGGER_NAME)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(config.LOG_FILE_NAME, maxBytes=config.LOG_MAX_SIZE_BYTES, backupCount=1)
handler.setFormatter(logging.Formatter("%(asctime)s :: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)

bot = telebot.TeleBot(token)
# set proxy settings (thx ro Roskomnadzor)
telebot.apihelper.proxy = {config.PROXY_PROTOCOL: f'{config.PROXY_SOCKS}://@{config.PROXY_ADDRESS}:{config.PROXY_PORT}'}

# register admin command handlers for sending messages everyone, e.t.c.
register_admin_commands(bot)

# main three buttons are declared here
main_markup = telebot.types.ReplyKeyboardMarkup(True)
main_markup.add(strings.TEXT_BUTTON_NOW, strings.TEXT_BUTTON_DAY, strings.TEXT_BUTTON_WEEK)


@bot.message_handler(commands=['start', 'help', 'configure', 'reminders', 'friend'])
def command_handler(message):
    """
    All commands are processed in this handler
    """
    log(message)
    # Register user if he is not registered
    if not user_controller.is_registered(message.from_user.id):
        user_controller.register(message.from_user.id, message.from_user.username)

    if message.text == "/start":
        bot.send_message(message.chat.id, strings.MESSAGE_HI, reply_markup=main_markup)
    if message.text == '/configure' or not user_controller.is_configured(message.from_user.id):
        options = telebot.types.ReplyKeyboardMarkup(True, False)
        # add buttons to choose course
        options.add(*list(config.REGISTERED_COURSES.keys()))
        msg = bot.send_message(message.chat.id, strings.REQUEST_COURSE, reply_markup=options)
        bot.register_next_step_handler(msg, process_course_step)
    elif message.text == "/help":
        bot.send_message(message.chat.id, strings.MESSAGE_HELP, reply_markup=main_markup)
    elif message.text == '/reminders':
        set_reminders(message)
    elif message.text == '/friend':
        msg = bot.send_message(message.chat.id, strings.REQUEST_ALIAS)
        bot.register_next_step_handler(msg, process_friend_request_step)


@bot.message_handler(regexp=f"^({'|'.join(strings.TEXT_DAYS_OF_WEEK)})⭐?$")
def weekday_select_handler(message):
    """
    Handler for schedule request of specific weekday
    """
    log(message)
    if not is_user_configured(message):
        return
    # remove star symbol if needed
    weekday = message.text[:2]
    # force check message is weekday due to bug
    if weekday not in strings.TEXT_DAYS_OF_WEEK:
        return
    # get list of lessons for specified user and day
    schedule = lesson_controller.get_day_lessons(message.from_user.id, day=strings.TEXT_DAYS_OF_WEEK.index(weekday))
    # convert lessons to understandable string output
    reply = strings.MESSAGE_FREE_DAY if not schedule else \
        strings.HEADER_SEPARATOR.join(str(lesson) for lesson in schedule)
    bot.send_message(message.chat.id, reply, reply_markup=main_markup)


@bot.message_handler(regexp=f"^({strings.TEXT_BUTTON_NOW}|{strings.TEXT_BUTTON_DAY}|{strings.TEXT_BUTTON_WEEK})$")
def main_buttons_handler(message):
    """
    Handler for processing three main buttons requests
    """
    log(message)
    if not is_user_configured(message):
        return
    # update alias if it was changed
    if user_controller.get(message.from_user.id).alias != message.from_user.username:
        user_controller.set_alias(message.from_user.id, message.from_user.username)
    # can not get schedule if not configured
    if message.text == strings.TEXT_BUTTON_NOW:
        send_current_schedule(message.chat.id, message.from_user.id)
    elif message.text == strings.TEXT_BUTTON_DAY:
        markup = telebot.types.ReplyKeyboardMarkup(True)
        buttons = list()
        day_of_week = datetime.today().weekday()
        # make list of weekdays and add star for today
        for i, day in enumerate(strings.TEXT_DAYS_OF_WEEK):
            buttons.append(telebot.types.KeyboardButton(day if day_of_week != i else day + "⭐"))
        markup.add(*buttons)
        bot.send_message(message.chat.id, strings.REQUEST_WEEKDAY, reply_markup=markup)
    elif message.text == strings.TEXT_BUTTON_WEEK:
        bot.send_message(message.chat.id, strings.MESSAGE_FULL_WEEK, reply_markup=main_markup)


@bot.message_handler()
def unknown_input_handler(message):
    """
    Handler for any other unknown messages
    """
    log(message)
    # show main buttons if unknown input sent
    bot.send_message(message.chat.id, strings.MESSAGE_ERROR, reply_markup=main_markup)


def is_user_configured(message):
    if not user_controller.is_configured(message.chat.id):
        bot.send_message(message.chat.id, strings.MESSAGE_USER_NOT_CONFIGURED, reply_markup=main_markup)
        return False
    return True


def process_course_step(message):
    """
    Save user`s course choice to database
    """
    course = message.text
    if course not in config.REGISTERED_COURSES.keys():
        unknown_input_handler(message)
        return
    user_controller.set_course(message.from_user.id, course)

    options = telebot.types.ReplyKeyboardMarkup(True, False)
    # add buttons of groups in selected course
    options.add(*list(config.REGISTERED_COURSES[course]))
    msg = bot.send_message(message.chat.id, strings.REQUEST_GROUP, reply_markup=options)
    bot.register_next_step_handler(msg, process_group_step)


def process_group_step(message):
    """
    Save user`s group choice to database
    """
    course = user_controller.get(message.from_user.id).course
    if message.text not in config.REGISTERED_COURSES[course]:
        unknown_input_handler(message)
        return
    user_controller.set_course_group(message.from_user.id, message.text)
    if course == 'BS1':
        # BS1 need special configuration of english group
        options = telebot.types.ReplyKeyboardMarkup(True, False)
        # add buttons for english group select
        options.add(*list(config.BS1_ENGLISH_GROUPS))
        msg = bot.send_message(message.chat.id, strings.REQUEST_ENGLISH, reply_markup=options)
        bot.register_next_step_handler(msg, process_english_step)
    else:
        set_reminders(message)


def process_english_step(message):
    """
    Save user`s english choice to database
    """
    if message.text not in config.BS1_ENGLISH_GROUPS:
        unknown_input_handler(message)
        return
    user_controller.set_english_group(message.from_user.id, message.text)
    set_reminders(message)


def set_reminders(message):
    """
    Ask user to allow send him reminders
    Function could be called from /reminder command or in configuring process
    """
    # request user to allow reminders
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.add(strings.MESSAGE_YES, strings.MESSAGE_NO)
    msg = bot.send_message(message.chat.id, strings.REQUEST_REMINDERS, reply_markup=markup)
    bot.register_next_step_handler(msg, process_reminders_step)


def process_reminders_step(message):
    """
    Save user`s reminder choice to database
    """
    user_id = message.from_user.id
    if message.text == strings.MESSAGE_YES:
        user_controller.set_reminders(user_id, True)
    elif message.text == strings.MESSAGE_NO:
        user_controller.set_reminders(user_id, False)
    else:
        unknown_input_handler(message)
        return
    bot.send_message(message.chat.id, strings.MESSAGE_SETTINGS_SAVED, reply_markup=main_markup)


def send_current_schedule(to_chat_id, about_user_id):
    """
    Send current and next lesson about specified user to given chat
    Function could be called from /friend command or NOW button press

    :param to_chat_id: int
    :param about_user_id: int
    """
    current_lesson = lesson_controller.get_current_lesson(about_user_id)
    next_lesson = lesson_controller.get_next_lesson(about_user_id)
    # add headers if needed
    reply = strings.HEADER_NOW + current_lesson.get_str_current() if current_lesson else ""
    reply += strings.HEADER_NEXT + next_lesson.get_str_future() if next_lesson else strings.HEADER_NO_NEXT_LESSONS
    bot.send_message(to_chat_id, reply, reply_markup=main_markup)


def process_friend_request_step(message):
    """
    Send current schedule of user with given alias to requesting person
    """
    # remove tabs, spaces and new line symbols
    alias = message.text.strip()
    # remove '@' at beginning
    if alias[0] == '@':
        alias = alias[1:]
    friend_id = user_controller.get_id_by_alias(alias)
    # check such friend exists
    if not friend_id or not user_controller.is_configured(friend_id):
        bot.send_message(message.chat.id, strings.MESSAGE_FRIEND_NOT_FOUND, reply_markup=main_markup)
        return
    send_current_schedule(message.chat.id, friend_id)


def log(message):
    """
    Write log info about message to file
    """
    logger.info(f"{message.from_user.username} :: {message.from_user.id} :: "
                f"{message.text if message.text else '--not_text--'}")


def remind_time():
    """
    Function is called by reminder module in certain amount of minutes before each lesson
    Iterates over users and sends reminders if needed
    """
    # get relevant reminders for current moment
    for remind in lesson_controller.get_relevant_reminders():
        user_id, lesson = remind[0], remind[1]
        try:
            bot.send_message(user_id, strings.HEADER_REMIND + str(lesson), reply_markup=main_markup)
        except Exception as exception:
            # 403 Forbidden means user blocked the bot (what a silly!)
            if hasattr(exception, 'result') and exception.result.status_code == 403:
                # delete user from database
                user_controller.delete(user_id)
            continue


# Tell reminder module which function should be called in remind time
reminder.notify_need_remind(remind_time)

# Save step handlers in file and load in case of restart
bot.enable_save_next_step_handlers()
bot.load_next_step_handlers()

# start listening for user`s messages
# bot.polling(none_stop=True, timeout=50)  # for DEBUG only. Does not restart bot in case of crash
bot.infinity_polling(none_stop=True, timeout=50)
