import telebot
import schedule

from modules.remind import controller, permanent
from modules.core.source import bot, log, main_markup

"""
Module send users notifications about coming lesson
Timetable information is taken from schedule module

Author: @Nmikriukov
"""


def attach_remind_module():

    @bot.message_handler(commands=['configure_remind'])
    def remind_command_handler(message):
        """
        Register commands to change module settings
        """
        log(permanent.MODULE_NAME, message)
        if message.text == '/configure_remind':
            markup = telebot.types.ReplyKeyboardMarkup(True, False)
            markup.add(permanent.MESSAGE_YES, permanent.MESSAGE_NO)
            msg = bot.send_message(message.chat.id, permanent.REQUEST_REMINDERS, reply_markup=markup)
            bot.register_next_step_handler(msg, process_reminders_step)

    def process_reminders_step(message):
        """
        Save user if he wants reminders or delete him from db otherwise
        """
        log(permanent.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        user_id = message.from_user.id
        if message.text == permanent.MESSAGE_YES:
            controller.register_user(user_id)
        elif message.text == permanent.MESSAGE_NO:
            controller.delete_user(user_id)
        else:
            bot.send_message(message.chat.id, permanent.MESSAGE_ERROR, reply_markup=main_markup)
            return
        bot.send_message(message.chat.id, permanent.MESSAGE_SETTINGS_SAVED, reply_markup=main_markup)

    def remind_time():
        """
        Function is called by reminder module in certain amount of minutes before each lesson
        Iterates over users and sends reminders if needed
        """
        # get relevant reminders for current moment
        for remind in controller.get_relevant_reminders():
            user_id, lesson = remind[0], remind[1]
            try:
                bot.send_message(user_id, permanent.HEADER_REMIND + str(lesson), reply_markup=main_markup)
            except Exception as exception:
                # 403 Forbidden means user blocked the bot (what a silly!)
                if hasattr(exception, 'result') and exception.result.status_code == 403:
                    controller.delete_user(user_id)
                continue

    # calculate time when to call remind_time
    for time_start in controller.get_reminder_times():
        schedule.every().day.at(time_start).do(remind_time)
