import logging
from settings.config import LOGGER_NAME


def register_admin_commands(bot):
    """
    Function allows to register special commands for admins
    Receive Telebot object from main module
    Admins could be whitelisted by telegram id and alias

    :param bot: Telebot
    """
    logger = logging.getLogger(LOGGER_NAME)

    @bot.message_handler(commands=['admin'])
    def admin(message):
        log(message)
        bot.send_message(message.chat.id, u"Hi, admin!")

    def log(message):
        """
        Write log info about admin message to file
        """
        logger.info(f"ADMIN {message.from_user.username} :: {message.from_user.id} :: "
                    f"{message.text if message.text else '--not_text--'}")
