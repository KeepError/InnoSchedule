from datetime import datetime

from telebot.types import Message

from modules.core.source import bot
from modules.electives import controller
from modules.electives.classes import User, Elective, ElectiveLesson


def usual_use_case():
    controller.delete_lessons()
    controller.delete_electives()
    # Create some electives
    elective = Elective("Elective1", "Teacher1", "E1")
    controller.save_electives(electives=elective)

    # Add lessons, connect with electives
    elective = controller.get_all_electives()[0]
    lessons = [ElectiveLesson(104, datetime(2021, 1, 28, 14, 00))]
    controller.add_elective_lesson(elective_id=elective.id, lesson=lessons[0])

    # Register user
    user = User(chat_id=999999)
    controller.register_user(user=user)

    # Enroll, check
    controller.enroll(elective.id, user.chat_id)
    is_added = len(controller.get_electives_of_user(user)) == 1

    # Un-enroll, check
    controller.un_enroll(elective.id, user.chat_id)
    is_removed = len(controller.get_electives_of_user(user)) == 0

    # Clean elective, orphan lesson should be deleted automatically
    amount_of_lessons = len(controller.get_lessons())
    lessons_to_remove = controller.get_lessons_of_elective(elective.id)
    controller.delete_elective(elective_id=elective.id)

    is_cleaned = False
    if amount_of_lessons - len(lessons_to_remove) == len(controller.get_lessons()):
        is_cleaned = True

    controller.delete_user(user.chat_id)

    return is_added and is_removed and is_cleaned


def run_tests(message: Message):
    if usual_use_case():
        bot.send_message(message.chat.id, "Test 1: OK")
    else:
        bot.send_message(message.chat.id, "Test 1: FAILED")
