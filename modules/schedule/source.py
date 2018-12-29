from datetime import datetime

import telebot

from modules.schedule import controller, permanent
from modules.core import source as core

"""
Module allows to set user's groups and get information about current and next lesson,
lessons at some day of week or get link to official google doc
Also may provide information about friend's current and next lessons by his alias

Authors: @Nmikriukov @thedownhill
"""


def attach_schedule_module():

    @core.bot.message_handler(commands=['friend', 'configure_schedule'])
    def schedule_command_handler(message):
        """
        Register module's commands
        """
        core.log(permanent.MODULE_NAME, message)
        if message.text == '/friend':
            msg = core.bot.send_message(message.chat.id, permanent.REQUEST_ALIAS)
            core.bot.register_next_step_handler(msg, process_friend_request_step)
        elif message.text == '/configure_schedule':
            # Register user if he is not registered
            if not controller.get_user(message.from_user.id):
                controller.register_user(message.from_user.id, message.from_user.username)
            # set configured to false and remove his groups
            controller.set_user_configured(message.from_user.id, False)
            options = telebot.types.ReplyKeyboardMarkup(True, False)
            # add buttons to choose course
            options.add(*list(permanent.REGISTERED_COURSES.keys()))
            msg = core.bot.send_message(message.chat.id, permanent.REQUEST_COURSE, reply_markup=options)
            core.bot.register_next_step_handler(msg, process_course_step)

    def process_course_step(message):
        """
        Get user's course and request course group
        """
        core.log(permanent.MODULE_NAME, message)
        course = message.text
        if course not in permanent.REGISTERED_COURSES.keys():
            core.bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=core.main_markup)
            return
        controller.append_user_group(message.from_user.id, course)

        options = telebot.types.ReplyKeyboardMarkup(True, False)
        # add buttons of groups in selected course
        options.add(*list(permanent.REGISTERED_COURSES[course]))
        msg = core.bot.send_message(message.chat.id, permanent.REQUEST_GROUP, reply_markup=options)
        core.bot.register_next_step_handler(msg, process_group_step)

    def process_group_step(message):
        """
        Save user`s group choice to database
        """
        core.log(permanent.MODULE_NAME, message)
        user_course = message.text[:3]
        if message.text not in permanent.REGISTERED_COURSES[user_course]:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=core.main_markup)
            return
        controller.append_user_group(message.from_user.id, message.text)
        if user_course == 'B18':
            # B18 need special configuration of english group
            options = telebot.types.ReplyKeyboardMarkup(True, False)
            # add buttons for english group select
            options.add(*list(permanent.B18_ENGLISH_GROUPS))
            msg = core.bot.send_message(message.chat.id, permanent.REQUEST_ENGLISH, reply_markup=options)
            core.bot.register_next_step_handler(msg, process_english_step)
        else:
            controller.set_user_configured(message.from_user.id, True)
            core.bot.send_message(message.chat.id, permanent.MESSAGE_SETTINGS_SAVED, reply_markup=core.main_markup)

    def process_english_step(message):
        """
        Save user`s english group to database
        """
        core.log(permanent.MODULE_NAME, message)
        if message.text not in permanent.B18_ENGLISH_GROUPS:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=core.main_markup)
            return
        controller.append_user_group(message.from_user.id, message.text)
        controller.set_user_configured(message.from_user.id, True)
        core.bot.send_message(message.chat.id, permanent.MESSAGE_SETTINGS_SAVED, reply_markup=core.main_markup)

    @core.bot.message_handler(
        regexp=f"^({permanent.TEXT_BUTTON_NOW}|{permanent.TEXT_BUTTON_DAY}|{permanent.TEXT_BUTTON_WEEK})$")
    def main_buttons_handler(message):
        """
        Handler for processing three main buttons requests
        """
        core.log(permanent.MODULE_NAME, message)
        # check user if configured
        user = controller.get_user(message.chat.id)
        if not user or not user.is_configured:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_USER_NOT_CONFIGURED, reply_markup=core.main_markup)
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
            core.bot.send_message(message.chat.id, permanent.REQUEST_WEEKDAY, reply_markup=markup)
        elif message.text == permanent.TEXT_BUTTON_WEEK:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_FULL_WEEK, reply_markup=core.main_markup)

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
        core.bot.send_message(to_chat_id, reply, reply_markup=core.main_markup)

    @core.bot.message_handler(regexp=f"^({'|'.join(permanent.TEXT_DAYS_OF_WEEK)})⭐?$")
    def weekday_select_handler(message):
        """
        Handler for schedule request of specific weekday
        """
        core.log(permanent.MODULE_NAME, message)
        # check user is configured
        if not controller.get_user(message.chat.id).is_configured:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_USER_NOT_CONFIGURED, reply_markup=core.main_markup)
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
        core.bot.send_message(message.chat.id, reply, reply_markup=core.main_markup)

    def process_friend_request_step(message):
        """
        Send current schedule of user with given alias to requesting user
        """
        core.log(permanent.MODULE_NAME, message)
        # check alias was sent
        if message.text is None:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=core.main_markup)
            return
        # remove tabs, spaces and new line symbols
        alias = message.text.strip()
        # remove '@' at beginning
        if alias[0] == '@':
            alias = alias[1:]
        friend = controller.get_user_by_alias(alias)
        # check such friend exists
        if not friend or not friend.is_configured:
            core.bot.send_message(message.chat.id, permanent.MESSAGE_FRIEND_NOT_FOUND, reply_markup=core.main_markup)
            return
        send_current_schedule(message.chat.id, friend.id)
