from datetime import datetime
from time import sleep

import telebot

from modules.schedule import controller, permanent
from modules.core.source import bot, log, main_markup

"""
Module allows to set user's groups and get information about current and next lesson,
lessons at some day of week or get link to official google doc
Also may provide information about friend's current and next lessons by his alias

Authors: @Nmikriukov @thedownhill
"""


def attach_schedule_module():
    @bot.message_handler(commands=['friend', 'configure_schedule'])
    def schedule_command_handler(message):
        """
        Register module's commands
        """
        log(permanent.MODULE_NAME, message)
        if '/friend' in message.text:
            # both '/friend' and '/friend @alias' are supported
            if message.text == "/friend":
                msg = bot.send_message(message.chat.id, permanent.REQUEST_ALIAS)
                bot.register_next_step_handler(msg, process_friend_request_step)
            elif len(message.text) > 8:
                alias = message.text[8:].strip()
                send_friend_schedule(message, alias)
        elif message.text == '/configure_schedule':
            # Register user if he is not registered
            if not controller.get_user(message.from_user.id):
                controller.register_user(message.from_user.id, message.from_user.username)

            # set configured to false and remove his groups
            controller.set_user_configured(message.from_user.id, False)
            options = telebot.types.ReplyKeyboardMarkup(True, False)

            # add buttons to choose course
            options.add(*list(permanent.REGISTERED_COURSES.keys()))
            msg = bot.send_message(message.chat.id, permanent.REQUEST_COURSE, reply_markup=options)
            bot.register_next_step_handler(msg, process_course_step)

    def process_course_step(message):
        """
        Get user's course and request course group
        """
        log(permanent.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        course = message.text
        # check course is in registered courses
        if course not in permanent.REGISTERED_COURSES.keys():
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        controller.append_user_group(message.from_user.id, course)

        options = telebot.types.ReplyKeyboardMarkup(True, False)
        # add buttons of groups in selected course
        options.add(*list(permanent.REGISTERED_COURSES[course]))
        msg = bot.send_message(message.chat.id, permanent.REQUEST_GROUP, reply_markup=options)
        bot.register_next_step_handler(msg, process_group_step)

    def process_group_step(message):
        """
        Save user`s group choice to database
        """
        log(permanent.MODULE_NAME, message)
        # check msg has text
        if not message.text:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        if message.text[:3] in permanent.REGISTERED_COURSES.keys():
            user_course = message.text[:3]
        elif message.text[:4] in permanent.REGISTERED_COURSES.keys():
            user_course = message.text[:4]
        else:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        if message.text not in permanent.REGISTERED_COURSES[user_course]:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return

        controller.append_user_group(message.from_user.id, message.text)
        if user_course == 'B20':
            # B19 need special configuration for english group
            options = telebot.types.ReplyKeyboardMarkup(True, False)
            # add buttons for english group select
            options.add(*permanent.B19_ENGLISH_GROUPS)
            msg = bot.send_message(message.chat.id, permanent.REQUEST_ENGLISH, reply_markup=options)
            bot.register_next_step_handler(msg, process_english_step)
        else:
            controller.set_user_configured(message.from_user.id, True)
            bot.send_message(message.chat.id, permanent.MESSAGE_SETTINGS_SAVED, reply_markup=main_markup)

    def process_english_step(message):
        """
        Save user`s english group to database
        """
        log(permanent.MODULE_NAME, message)
        if not message.text or message.text not in permanent.B19_ENGLISH_GROUPS:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        controller.append_user_group(message.from_user.id, message.text)
        controller.set_user_configured(message.from_user.id, True)
        bot.send_message(message.chat.id, permanent.MESSAGE_SETTINGS_SAVED, reply_markup=main_markup)

    @bot.message_handler(regexp=f"^({permanent.TEXT_BUTTON_NOW}|"
                                f"{permanent.TEXT_BUTTON_DAY}|"
                                f"{permanent.TEXT_BUTTON_WEEK})$")
    def main_buttons_handler(message):
        """
        Handler for processing three main buttons requests
        """
        log(permanent.MODULE_NAME, message)
        # check user if configured
        user = controller.get_user(message.chat.id)
        if not user or not user.is_configured:
            bot.send_message(message.chat.id, permanent.MESSAGE_USER_NOT_CONFIGURED, reply_markup=main_markup)
            return

        # update alias if it was changed
        controller.set_user_alias(message.from_user.id, message.from_user.username)

        if message.text == permanent.TEXT_BUTTON_NOW:
            send_current_schedule(message.chat.id, message.from_user.id)
        elif message.text == permanent.TEXT_BUTTON_DAY:
            markup = telebot.types.ReplyKeyboardMarkup(True)
            buttons = list()
            day_of_week = datetime.today().weekday()
            # make list of weekdays and add star for today
            for i, day in enumerate(permanent.TEXT_DAYS_OF_WEEK):
                buttons.append(telebot.types.KeyboardButton(day if day_of_week != i else day + "⭐"))
            markup.add(*buttons)
            bot.send_message(message.chat.id, permanent.REQUEST_WEEKDAY, reply_markup=markup)
        elif message.text == permanent.TEXT_BUTTON_WEEK:
            bot.send_message(message.chat.id, permanent.MESSAGE_FULL_WEEK, reply_markup=main_markup, parse_mode="MarkdownV2")

    def send_current_schedule(to_chat_id, about_user_id):
        """
        Send current and next lesson about specified user to given chat
        Function could be called from /friend command or NOW button press

        :param to_chat_id: int
        :param about_user_id: int
        """
        current_lesson = controller.get_current_lesson(about_user_id)
        next_lesson = controller.get_next_lesson(about_user_id)
        # add headers if needed
        reply = permanent.HEADER_NOW + current_lesson.get_str_current() if current_lesson else ""

        if next_lesson:
            reply += permanent.HEADER_NEXT + next_lesson.get_str_future()
        else:
            reply += permanent.HEADER_NO_NEXT_LESSONS
        bot.send_message(to_chat_id, reply, reply_markup=main_markup)

    @bot.message_handler(regexp=f"^({'|'.join(permanent.TEXT_DAYS_OF_WEEK)})⭐?$")
    def weekday_select_handler(message):
        """
        Handler for schedule request of specific weekday
        """
        log(permanent.MODULE_NAME, message)
        # check user is configured
        if not controller.get_user(message.chat.id).is_configured:
            bot.send_message(message.chat.id, permanent.MESSAGE_USER_NOT_CONFIGURED, reply_markup=main_markup)
            return
        # remove star symbol if needed
        weekday = message.text[:2]
        # force check message is weekday due to some bug
        if weekday not in permanent.TEXT_DAYS_OF_WEEK:
            return
        # get list of lessons for specified user and day
        schedule = controller.get_day_lessons(message.from_user.id,
                                              day=permanent.TEXT_DAYS_OF_WEEK.index(weekday))
        # convert lessons to understandable string output
        reply = permanent.MESSAGE_FREE_DAY if not schedule else \
            permanent.HEADER_SEPARATOR.join(str(lesson) for lesson in schedule)
        bot.send_message(message.chat.id, reply, reply_markup=main_markup)

    def process_friend_request_step(message):
        """
        Get friend's alias after /friend command to show his current schedule
        """
        log(permanent.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        send_friend_schedule(message, message.text)

    @bot.message_handler(regexp="^@?[A-Za-z0-9_]{5,100}$")
    def inline_friend_command_handler(message):
        """
        Show friend's schedule if his alias was sent without /friend command
        """
        log(permanent.MODULE_NAME, message)
        send_friend_schedule(message, message.text)

    def send_friend_schedule(message, alias):
        """
        Send friend schedule by request
        """
        # check alias was sent
        if not message.text:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        # remove tabs, spaces and new line symbols
        alias = alias.strip()
        # remove '@' at beginning
        if alias[0] == '@':
            alias = alias[1:]

        friend = controller.get_user_by_alias(alias)
        # check such friend exists
        if not friend or not friend.is_configured:
            bot.send_message(message.chat.id, permanent.MESSAGE_FRIEND_NOT_FOUND, reply_markup=main_markup)
            return
        send_current_schedule(message.chat.id, friend.id)
