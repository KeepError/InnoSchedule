from modules.core import source as core
from modules.admin import permanent

"""
Admin module allows to register special commands for admins (e.g. statistics)
Admins could be whitelisted by telegram_ids or aliases
"""


def attach_admin_module():

    @core.bot.message_handler(commands=['admin'])
    def admin_message_handler(message):
        core.log(permanent.MODULE_NAME, message)
        core.bot.send_message(message.chat.id, permanent.MESSAGE_ADMIN)
