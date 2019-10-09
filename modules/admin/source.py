from datetime import datetime, timedelta

from file_read_backwards import FileReadBackwards

from modules.core.source import bot, log
from modules.admin import controller, permanent
from modules.schedule.permanent import REGISTERED_COURSES
from modules.schedule.controller import get_user_by_alias
from modules.autoparser.source import attach_autoparser_module


"""
Module allows admins to get statistics, send private or spam (to everybody) messages and control bot

Author: @Nmikriukov
"""


def attach_admin_module():

    personal_msg_user_id = None  # global because register_next_step_handler can not pass parameters
    admin_commands = ['']

    @bot.message_handler(commands=admin_commands)
    def admin(message):
        """
        Register module's commands
        """
        log(permanent.MODULE_NAME, message)
        # only admins from list are allowed to call admin commands
        if message.from_user.id not in permanent.ADMIN_LIST:
            bot.send_message(message.chat.id, permanent.MESSAGE_UNAUTHORIZED)
            return
        elif message.text == '/helpa':
            # send admin commands help
            bot.send_message(message.chat.id, ' '.join(admin_commands))
