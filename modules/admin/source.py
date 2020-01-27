from datetime import datetime, timedelta

from file_read_backwards import FileReadBackwards
import telebot

from modules.core.source import bot, log
from modules.admin import controller, permanent
from modules.schedule.controller import get_user_by_alias
from modules.autoparser.source import attach_autoparser_module
from modules.schedule.permanent import REGISTERED_COURSES


"""
Module allows admins to get statistics, send private or spam (to everybody) messages and control bot

Author: @Nmikriukov
"""


def attach_admin_module():
    # global because register_next_step_handler can not pass parameters
    personal_msg_user_id = None
    spam_course = None
    admin_commands = ['die', 'log', 'spam', 'pm', 'stats', 'parse', 'helpa', 'spam_course']

    @bot.message_handler(commands=admin_commands)
    def admin(message):
        """
        Register module's commands
        """
        global spam_course
        log(permanent.MODULE_NAME, message)
        # only admins from list are allowed to call admin commands
        if message.from_user.id not in permanent.ADMIN_LIST:
            bot.send_message(message.chat.id, permanent.MESSAGE_UNAUTHORIZED)
            return
        if message.text == "/die":
            if message.from_user.id not in permanent.SUPERADMIN_LIST:
                return
            raise Exception
        elif message.text == '/log':
            bot.send_document(message.chat.id, open('log', 'rb'))
        elif message.text == '/spam':
            # send message to everybody
            spam_course = None
            if message.from_user.id not in permanent.SUPERADMIN_LIST:
                return
            msg = bot.send_message(message.chat.id, permanent.REQUEST_SPAM_MESSAGE)
            bot.register_next_step_handler(msg, process_spam_step)
        elif message.text == '/spam_course':
            if message.from_user.id not in permanent.SUPERADMIN_LIST:
                return
            options = telebot.types.ReplyKeyboardMarkup(True, False)
            # add buttons to choose course
            options.add(*list(REGISTERED_COURSES.keys()))
            msg = bot.send_message(message.chat.id, permanent.REQUEST_COURSE, reply_markup=options)
            bot.register_next_step_handler(msg, process_course_step)
        elif message.text == '/pm':
            # private message to specific user
            msg = bot.send_message(message.chat.id, permanent.REQUEST_PERSONAL_ALIAS)
            bot.register_next_step_handler(msg, process_pm_alias_step)
        elif message.text == '/stats':
            # send statistics
            send_statistics_to_admin(message)
        elif message.text == '/parse':
            # parse new schedule
            if message.from_user.id not in permanent.SUPERADMIN_LIST:
                return
            attach_autoparser_module.parse_schedule_func()
            bot.send_message(message.chat.id, permanent.MESSAGE_SCHEDULE_UPDATED)
        elif message.text == '/helpa':
            # send admin commands help
            bot.send_message(message.chat.id, ' '.join(admin_commands))

    def process_course_step(message):
        log(permanent.MODULE_NAME, message)
        if not message.text:
            bot.send_message(message.chat.id, permanent.MESSAGE_ABORTED)
            return
        if message.text == "C":
            bot.send_message(message.chat.id, permanent.MESSAGE_ABORTED)
            return
        # check course is in registered courses
        if message.text not in REGISTERED_COURSES.keys():
            bot.send_message(message.chat.id, permanent.MESSAGE_ABORTED)
            return
        global spam_course
        spam_course = message.text
        msg = bot.send_message(message.chat.id, permanent.REQUEST_SPAM_MESSAGE,
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, process_spam_step)

    def process_spam_step(message):
        """
        Get spam message and send to everyone
        """
        global spam_course
        log(permanent.MODULE_NAME, message)
        # abort operation if needed
        if message.text == "C":
            bot.send_message(message.chat.id, permanent.MESSAGE_ABORTED)
            return
        # iterate over all users and SPAM
        for user, is_reminded in controller.get_all_users():
            try:
                if spam_course is not None and spam_course not in controller.get_user_groups(user.id):
                    continue
                bot.send_message(user.id, message.text)
            except:
                pass
        bot.send_message(message.chat.id, permanent.MESSAGE_SENT_EVERYBODY)

    def process_pm_alias_step(message):
        """
        Get alias of user to send private message
        """
        log(permanent.MODULE_NAME, message)
        # abort operation if needed
        if message.text == "C":
            bot.send_message(message.chat.id, permanent.MESSAGE_ABORTED)
            return
        alias = message.text.strip()
        # remove '@' at beginning
        if alias[0] == '@':
            alias = alias[1:]
        user = get_user_by_alias(alias)
        if user is None:
            bot.send_message(message.chat.id, permanent.MESSAGE_USER_NOT_FOUND)
            return
        # use global, because can not pass parameters using register_next_step_handler
        global personal_msg_user_id
        personal_msg_user_id = user.id
        msg = bot.send_message(message.chat.id, f"{permanent.REQUEST_PERSONAL_MESSAGE}{alias}")
        bot.register_next_step_handler(msg, process_personal_message_step)

    def process_personal_message_step(message):
        """
        Get personal message and send to specific person
        """
        log(permanent.MODULE_NAME, message)
        # abort operation if needed
        if message.text == "C":
            bot.send_message(message.chat.id, permanent.MESSAGE_ABORTED)
            return
        global personal_msg_user_id
        try:
            bot.send_message(personal_msg_user_id, message.text)
        except Exception as e:
            bot.send_message(message.chat.id, permanent.MESSAGE_EXCEPTION + str(e))
            return
        bot.send_message(message.chat.id, permanent.MESSAGE_SENT_PERSONAL)

    def get_course_by_group(group):
        """
        Example: "M18-SE-01" will return "M-SE"
        """
        for course in REGISTERED_COURSES:
            if group in REGISTERED_COURSES[course]:
                return course

    def send_statistics_to_admin(message):
        """
        Send usage statistics from log to admin
        """
        final_msg = "`      |reminded|registered`\n"
        final_msg += "`------+--------+----------`\n"
        # calculate registered and reminded students in each course
        course_stats = {course: {"registered": 0, "reminded": 0} for course in REGISTERED_COURSES}
        for user, is_reminded in controller.get_all_users():
            for group in user.groups:
                course = get_course_by_group(group.name)
                if course in REGISTERED_COURSES:
                    course_stats[course]["registered"] += 1
                    if is_reminded:
                        course_stats[course]["reminded"] += 1

        # generate final message
        for course in course_stats:
            final_msg += f"`{course.rjust(6)}|{str(course_stats[course]['reminded']).rjust(8)}|" \
                f"{str(course_stats[course]['registered']).rjust(10)}`\n"

        # add total info for all courses
        final_msg += f"` Total|{str(sum([course_stats[course]['reminded'] for course in course_stats])).rjust(8)}|"\
            f"{str(sum([course_stats[course]['registered'] for course in course_stats])).rjust(10)}`\n"

        bot.send_message(message.chat.id, final_msg, parse_mode="Markdown")

        # calculate functionality statistics for specified periods
        buttons = {"NOW": 0, "DAY": 0, "WEEK": 0, "friend": 0, "start": 0, "config": 0}
        msg_stats = {period: buttons.copy() for period in ["day", "week", "month", "year"]}
        today = datetime.today()
        day_before = today - timedelta(days=1)
        week_before = today - timedelta(days=7)
        month_before = today - timedelta(days=30)
        year_before = today - timedelta(days=365)

        # read log reversed
        with FileReadBackwards("log", encoding="utf-8") as reversed_log:
            for line in reversed_log:
                spltted_line = line.split()
                if len(spltted_line) < 9:
                    continue
                msg_date, msg_text = spltted_line[0], spltted_line[8]
                # try to convert date to object
                try:
                    msg_date = datetime.strptime(msg_date, "%d.%m.%Y")
                except ValueError as _:
                    continue
                # examine which functionality was used
                if "NOW" in msg_text:
                    msg_type = "NOW"
                elif "DAY" in msg_text:
                    msg_type = "DAY"
                elif "WEEK" in msg_text:
                    msg_type = "WEEK"
                elif "friend" in msg_text or msg_text[0] == "@":
                    msg_type = "friend"
                elif "start" in msg_text:
                    msg_type = "start"
                elif "configure" in msg_text:
                    msg_type = "config"
                else:
                    continue

                if msg_date > day_before:
                    msg_stats["day"][msg_type] += 1
                if msg_date > week_before:
                    msg_stats["week"][msg_type] += 1
                if msg_date > month_before:
                    msg_stats["month"][msg_type] += 1
                if msg_date > year_before:
                    msg_stats["year"][msg_type] += 1

        # generate final message
        final_msg = "`      |day|week|month|year`\n"
        final_msg += "`------+---+----+-----+----`\n"
        for button in buttons:
            final_msg += f"`{button.rjust(6)}|{str(msg_stats['day'][button]).rjust(3)}|" \
                f"{str(msg_stats['week'][button]).rjust(4)}|" \
                f"{str(msg_stats['month'][button]).rjust(5)}|" \
                f"{str(msg_stats['year'][button]).rjust(4)}`\n"

        bot.send_message(message.chat.id, final_msg, parse_mode="Markdown")
