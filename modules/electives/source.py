from sqlalchemy.exc import SQLAlchemyError
from telebot.types import Message, ReplyKeyboardMarkup

from modules.core.source import bot, main_markup
from modules.electives import test, permanent, controller, parser
from modules.electives.classes import User
import modules.schedule.permanent as sch_permanent

"""
This module allows user to configure their electives, which will be included
in regular schedule

Author: @AAHTOXA (Telegram)
        @Mexator (GitHub)
"""


def attach_electives_module():
    @bot.message_handler(commands=['configure_electives'])
    def configure_electives_command_handler(message: Message):
        if '/configure_electives' in message.text:
            try:
                controller.delete_user(message.from_user.id)
            except:
                pass
        controller.register_user(User(message.from_user.id))
        choose_category_step(message.chat.id)

    def choose_category_step(chat_id: int):
        categories_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        categories_markup.add(*controller.get_categories(), permanent.BUTTON_DONE)
        msg: Message = bot.send_message(chat_id,
                                        permanent.PROMPT_CHOOSE_CATEGORY,
                                        reply_markup=categories_markup)
        bot.register_next_step_handler(msg, process_category_step)

    def generate_courses_keyboard(chosen_category, user_id):
        electives_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        buttons = [
            f"{'✅ ' if controller.is_enrolled(elective.id, user_id) else ''}{elective.name}, {elective.id}"
            for elective in
            controller.get_electives_by_category(chosen_category)]
        electives_markup.add(*buttons, permanent.BUTTON_BACK, permanent.BUTTON_DONE)

        return electives_markup

    def process_category_step(message: Message):
        if message.text == permanent.BUTTON_DONE:
            bot.send_message(message.chat.id, permanent.VERBOSE_CONFIGURED,
                             reply_markup=main_markup)
            return
        if message.text not in controller.get_categories():
            bot.send_message(message.chat.id, sch_permanent.MESSAGE_ERROR)
            bot.register_next_step_handler(message, process_category_step)
            return

        msg: Message = bot.send_message(message.chat.id, permanent.PROMPT_CHOOSE_ELECTIVE,
                                        reply_markup=generate_courses_keyboard(message.text, message.from_user.id))
        bot.register_next_step_handler(msg, process_elective_step, chosen_category=message.text)

    def process_elective_step(message: Message, chosen_category=""):
        if message.text == permanent.BUTTON_DONE:
            bot.send_message(message.chat.id, permanent.VERBOSE_CONFIGURED,
                             reply_markup=main_markup)
            return
        if message.text == permanent.BUTTON_BACK:
            choose_category_step(message.chat.id)
            return
        try:
            elective_id = int(message.text.split(", ")[1])
            elective = controller.get_elective(elective_id)
            if not controller.is_enrolled(elective_id, message.from_user.id):
                controller.enroll(elective_id, message.from_user.id)
                text = permanent.VERBOSE_YOU_ENROLLED
            else:
                controller.un_enroll(elective_id, message.from_user.id)
                text = permanent.VERBOSE_YOU_UNENROLLED
            bot.send_message(message.chat.id, text + elective.name,
                             reply_markup=generate_courses_keyboard(chosen_category, message.from_user.id))
            bot.register_next_step_handler(message, process_elective_step, chosen_category=chosen_category)
        except:
            bot.send_message(message.chat.id, sch_permanent.MESSAGE_ERROR)
            bot.register_next_step_handler(message, process_elective_step, chosen_category=chosen_category)

    @bot.message_handler(commands=['elective_test'])
    def test_command_handler(message: Message):
        test.run_tests(message)

    attach_electives_module.parse_schedule_func = parser.parse_new_electives_timetable
