from datetime import timedelta, datetime

from modules.remind.classes import User
from modules.schedule.classes import Lesson
from modules.core import source as core
from modules.remind import permanent
from modules.schedule import controller as schedule_controller


@core.db_write
def register_user(session, user_id):
    """
    Register user to send him reminders

    :param session: sqlalchmey session from decorator
    :param user_id: int
    """
    session.add(User(user_id))


@core.db_write
def delete_user(session, user_id):
    """
    Delete user so no reminders will be send

    :param session: sqlalchmey session from decorator
    :param user_id: int
    """
    session.query(User).filter_by(id=user_id).delete()


@core.db_read
def get_relevant_reminders(session):
    """
    Function is called in fixed amount of minutes before each lesson (e.g. 10 minutes)
    Returns list of tuples with user ids and lessons.
    Each user in tuple must be reminded about his lesson

    :param session: sqlalchmey session from decorator
    :return: [(int, Lesson)]
    """
    users = session.query(User).all()
    need_remind = []
    for user in users:
        next_lesson = schedule_controller.get_next_lesson(user.id)
        if next_lesson and abs(next_lesson.minutes_until_start - permanent.REMIND_WHEN_LEFT_MINUTES) <= 1:
            need_remind.append((user.id, next_lesson))
    return need_remind


@core.db_read
def get_reminder_times(session):
    """
    Function is called once when remind module is attached
    Return list of times in 'hh:mm' format, when reminders should be sent every day

    :param session: sqlalchmey session from decorator
    :return: [String]
    """
    start_times = session.query(Lesson.start).distinct().all()
    # subtract needed time from lesson start time for reminding in time
    start_times = [datetime.strptime(start_time[0], "%H:%M") - timedelta(minutes=permanent.REMIND_WHEN_LEFT_MINUTES)
                   for start_time in start_times]
    # convert datetime back to string
    return [remind_time.strftime("%H:%M") for remind_time in start_times]
