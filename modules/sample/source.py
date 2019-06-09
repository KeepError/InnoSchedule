from modules.core.source import bot, log
from modules.sample import controller, permanent

"""
Module provides simple example of how you may write your own module
Save user's favorite string and send it when requested

Author: @Nmikriukov
"""


def attach_sample_module():

    @bot.message_handler(commands=['set_favorite_string', 'get_favorite_string'])
    def schedule_command_handler(message):
        """
        Register module's commands
        """
        # log message
        log(permanent.MODULE_NAME, message)
        # get user's favorite string from database
        favorite_string = controller.get_string(message.from_user.id)
        # set default string if no such found
        if not favorite_string:
            favorite_string = permanent.TEXT_DEFAULT_STRING
            controller.register_user(message.from_user.id, favorite_string)
        if message.text == '/set_favorite_string':
            # send string request
            msg = bot.send_message(message.chat.id, permanent.REQUEST_FAVORITE_STRING)
            # register new single-use message handler
            bot.register_next_step_handler(msg, process_request_string)
        elif message.text == '/get_favorite_string':
            bot.send_message(message.chat.id, favorite_string)

    def process_request_string(message):
        """
        Get and save new user's favorite string
        """
        # log message
        log(permanent.MODULE_NAME, message)
        # save new string to db
        controller.set_string(message.from_user.id, message.text)
        # notify user of changes
        bot.send_message(message.chat.id, permanent.MESSAGE_STRING_SAVED)
