from telebot.types import Message

from modules.core.source import bot
from modules.electives import controller, test
from modules.electives.classes import Elective
from modules.schedule.controller import get_user

"""
This module allows user to configure their electives, which will be included
in regular schedule

Author: @AAHTOXA (Telegram)
        @Mexator (GitHub)
"""


def attach_electives_module():
    @bot.message_handler(commands=['configure_electives'])
    def elective_command_handler(message: Message):
        if '/configure_electives' in message.text:
            pass

    @bot.message_handler(commands=['elective_test'])
    def test_command_handler(message: Message):
        bot.register_next_step_handler(message, test.run_tests)
