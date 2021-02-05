"""
Tests for electives module. As I did not understand how to mock sqlalchemy db,
all tests should clean after themselves
"""
import unittest
from datetime import datetime

from telebot.types import Message

from modules.core.source import bot
from modules.electives import controller, parser
from modules.electives.classes import User, Elective, ElectiveLesson
from modules.electives.controller import DBException


class DBTests(unittest.TestCase):

    def test_save_elective(self):
        new_elective = Elective("Doing Nothing", "Gandi", "DN", "Main")
        try:
            controller.add_elective(new_elective)
            # Inserted
            self.assertTrue(controller.get_elective(new_elective.id) is not None)
            # Can not be inserted second time
            self.assertRaises(DBException, controller.add_elective, new_elective)
        finally:
            controller.delete_elective(new_elective.id)

    def test_enroll(self):
        new_elective = Elective("Doing Nothing", "Gandi", "DN", "Main")
        new_user = User(chat_id=999999)

        try:
            controller.register_user(new_user)
            controller.add_elective(new_elective)

            controller.enroll(new_elective.id, new_user.chat_id)
            self.assertEqual(controller.get_electives_of_user(new_user), [new_elective])

        finally:
            controller.delete_user(new_user.chat_id)
            controller.delete_elective(new_elective.id)

    def test_lessons_auto_deleted(self):
        """Tests that when elective is deleted, its lessons are removed as well"""
        new_elective = Elective("Doing Nothing", "Gandi", "DN", "Main")
        lessons = [ElectiveLesson(104, datetime(2021, 1, 28, 14, 00))]
        try:
            controller.add_elective(new_elective)
            controller.add_elective_lesson(elective_id=new_elective.id, lesson=lessons[0])

            amount_of_lessons = len(controller.get_lessons())
            lessons_to_remove = controller.get_lessons_of_elective(new_elective.id)
            controller.delete_elective(elective_id=new_elective.id)

            self.assertEqual(amount_of_lessons - len(lessons_to_remove),
                             len(controller.get_lessons()))
        except DBException:
            try:
                for lesson in lessons:
                    controller.delete_lesson(lesson)
                controller.delete_elective(new_elective.id)
            except DBException:
                pass


def load_schedule():
    parser.parse_new_electives_timetable()


def run_tests(message: Message):
    elective_suite = unittest.TestSuite()
    elective_suite.addTest(unittest.makeSuite(DBTests))
    print("count of tests: " + str(elective_suite.countTestCases()) + "\n")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(elective_suite)
    if result.wasSuccessful():
        bot.send_message(message.chat.id,
                         f"Successfully ran all tests ({result.testsRun} tests were run)")
    else:
        bot.send_message(message.chat.id, f"Some tests failed: \n {result.failures}")
