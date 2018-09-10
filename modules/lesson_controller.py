from datetime import datetime, timedelta
import sqlite3
import threading

from modules import user_controller
from modules.lesson import Lesson
from settings.config import REMIND_WHEN_LEFT_MINUTES


conn = sqlite3.connect('db.sqlite', check_same_thread=False)  # open new sqlite connection
cursor = conn.cursor()  # cursor allows to iterate over database data
lock = threading.RLock()  # at any moment of time only one thread may request db. All others are waiting


def get_day_lessons(user_id, day):
    """
    Function return lessons for user on exact weekday sorted by start time

    :param user_id:  int
    :param day:  int [0-6]
    :return: [Lesson]
    """

    with lock:
        user = user_controller.get(user_id)
        if not user:
            return

        columns = "subject, type, teacher, teacher_gender, start, end, room"

        # Take lessons that are common for whole course
        cursor.execute(f"SELECT {columns} FROM common_lessons "
                       "WHERE course=? AND day=?", (user.course, day,))
        data = cursor.fetchall()

        # Take lessons that are only for user`s course group
        cursor.execute(f"SELECT {columns} FROM group_lessons "
                       "WHERE course=? AND lesson_group=? AND day=?", (user.course, user.course_group, day,))
        data += cursor.fetchall()

        # BS1 have special group for english
        if user.course == 'BS1':
            cursor.execute(f"SELECT {columns} FROM group_lessons "
                           "WHERE subject='English' AND course=? "
                           "AND lesson_group=? AND day=?", (user.course, user.english_group, day,))
            data += cursor.fetchall()

    return sorted([Lesson(x) for x in data])


def get_current_lesson(user_id):
    """
    Function returns Lesson for specified user that is going right now
    or None if there is no such lesson

    :param user_id: int
    :return: Lesson or None
    """
    today_lessons = get_day_lessons(user_id, datetime.today().weekday())
    for lesson in today_lessons:
        if lesson.start < datetime.now() < lesson.end:
            return lesson


def get_next_lesson(user_id):
    """
    Function returns Lesson for specified user that will start next today
    or None if there is no such lesson

    :param user_id: int
    :return: Lesson or None
    """
    today_lessons = get_day_lessons(user_id, datetime.today().weekday())
    for lesson in today_lessons:
        if datetime.now() < lesson.start:
            return lesson


def get_relevant_reminders():
    """
    Function is called in fixed amount of minutes before each lesson (e.g. 10 minutes)
    Returns list of tuples with user ids and lessons.
    Each user in tuple must be reminded about his lesson

    :return: [(int, Lesson)]
    """
    users = user_controller.get_users_with_reminders()
    need_remind = []
    for user in users:
        if not user_controller.is_configured(user.id):
            continue
        next_lesson = get_next_lesson(user.id)
        if next_lesson and abs(next_lesson.minutes_until_start - REMIND_WHEN_LEFT_MINUTES) <= 1:
            need_remind.append((user.id, next_lesson))
    return need_remind


def get_reminder_times():
    """
    Function is called once when reminder module is started
    Return array of times in 'hh:mm' format, when reminders should be sent every day

    :return: [String]
    """
    with lock:
        cursor.execute("SELECT start FROM group_lessons GROUP BY start UNION "
                       "SELECT start FROM common_lessons GROUP BY start")
        data = cursor.fetchall()
    # each row is array with one element - start time
    data = sorted([row[0] for row in data])
    # subtract needed time from lesson start time for making remind in time
    data = [datetime.strptime(start_time, "%H:%M") - timedelta(minutes=REMIND_WHEN_LEFT_MINUTES) for start_time in data]
    # convert datetime back to string
    return [remind_time.strftime("%H:%M") for remind_time in data]
