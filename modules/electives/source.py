from telebot.types import Message, ReplyKeyboardMarkup

from modules.core.source import bot
from modules.electives import test, permanent, controller, parser

"""
This module allows user to configure their electives, which will be included
in regular schedule

Author: @AAHTOXA (Telegram)
        @Mexator (GitHub)
"""


def attach_electives_module():
    @bot.message_handler(commands=['parse_electives'])
    def parse_handler(message: Message):
        bot.send_message(message.chat.id,
                         permanent.VERBOSE_PARSE_STARTED)
        # TODO: Restrict this command to admins only
        parser.parse_new_electives_timetable()
        bot.send_message(message.chat.id,
                         permanent.VERBOSE_PARSE_DONE)

    @bot.message_handler(commands=['configure_electives'])
    def elective_command_handler(message: Message):
        if '/configure_electives' in message.text:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
            markup.add(*list(controller.get_categories()))
            msg: Message = bot.send_message(message.chat.id,
                                            permanent.PROMPT_CHOOSE_CATEGORY,
                                            reply_markup=markup)

    @bot.message_handler(commands=['elective_test'])
    def test_command_handler(message: Message):
        test.run_tests(message)
