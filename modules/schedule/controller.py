from datetime import datetime

from modules.schedule.classes import User, Group
from modules.core.source import db_read, db_write


@db_read
def get_day_lessons(session, user_id, day):
    """
    Function return lessons for user on exact weekday sorted by start time

    :param session: sqlalchemy session from decorator
    :param user_id:  int
    :param day:  int [0-6]
    :return: [Lesson]
    """
    user = session.query(User).filter_by(id=user_id).first()
    lessons = []
    for group in user.groups:
        # filter lessons from user`s groups by given day
        lessons += list(filter(lambda lesson: lesson.day == day, group.lessons))
    return sorted(lessons)


def get_current_lesson(user_id):
    """
    Function returns Lesson for specified user that is going right now
    or None if there is no such lesson

    :param user_id: int
    :return: Lesson or None
    """
    today_lessons = get_day_lessons(user_id, datetime.today().weekday())
    for lesson in today_lessons:
        if lesson.start_struct < datetime.now() < lesson.end_struct:
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
        if datetime.now() < lesson.start_struct:
            return lesson


@db_write
def append_user_group(session, user_id, group):
    """
    Add user to group

    :param session: sqlalchemy session from decorator
    :param user_id: int
    :param group: string
    """
    user = session.query(User).filter_by(id=user_id).first()
    group = session.query(Group).filter_by(name=group).first()
    if not user or not group:
        return
    user.groups.append(group)


@db_read
def get_user(session, user_id):
    """
    Get instance of concrete module user
    Note that session will be closed and any changes to this instance will be ignored

    :param session: sqlalchemy session from decorator
    :param user_id: int
    :return: User
    """
    return session.query(User).filter_by(id=user_id).first()


@db_write
def register_user(session, user_id, alias):
    """
    Register new user in module

    :param session: sqlalchemy session from decorator
    :param user_id: int
    :param alias: string
    """
    session.add(User(user_id, alias))


@db_read
def get_user_by_alias(session, alias):
    """
    Return User instance by his telegram alias or None if user not found
    Note that session will be closed and any changes to this instance will be ignored

    :param session: sqlalchemy session from decorator
    :param alias: string
    :return: User
    """
    return session.query(User).filter_by(alias=alias).first()


@db_write
def set_user_alias(session, user_id, alias):
    """
    Update user`s alias in database

    :param session: sqlalchemy session from decorator
    :param user_id: int
    :param alias: string
    """
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.alias = alias


@db_write
def set_user_configured(session, user_id, configured):
    """
    Set user is_configured to
        True if all his groups are added
        False and delete all his groups (when user starts configuration of his groups)

    :param session: sqlalchemy session from decorator
    :param user_id: int
    :param configured: boolean
    """
    user = session.query(User).filter_by(id=user_id).first()
    if not configured:
        user.groups = []
    user.is_configured = configured
