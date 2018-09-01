def register_admin_commands(bot):
    """
    Function allows to register special commands for admins
    Receive Telebot object from main module
    Admins could be whitelisted by telegram id and alias

    :param bot: Telebot
    """
    @bot.message_handler(commands=['admin'])
    def admin(message):
        bot.send_message(message.chat.id, u"Hi, admin!")
