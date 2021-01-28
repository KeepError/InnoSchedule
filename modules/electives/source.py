from telebot.types import Message

from modules.core.source import bot
from modules.electives import controller
from modules.electives.classes import Elective
from modules.schedule.controller import get_user

"""
This module allows user to configure their electives, which will be included
in regular schedule

Author: @AAHTOXA
"""


def attach_electives_module():
    @bot.message_handler(commands=['configure_electives'])
    def elective_command_handler(message: Message):
        if '/configure_electives' in message.text:
            controller.delete_electives()
            controller.save_electives([Elective("123", "teacher1", 1, 123, "AAA"),
                                       Elective("1234", "teacher2", 1, 1234, "AAA")])

            user = get_user(message.chat.id)

            bot.send_message(chat_id=message.chat.id, text=user)
            electives = controller.get_all_electives()
            bot.send_message(chat_id=message.chat.id, text=electives)
