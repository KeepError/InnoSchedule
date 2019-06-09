from modules.sample.classes import User
from modules.core.source import db_read, db_write


@db_write
def register_user(session, user_id, string):
    """
    Register user to send him reminders

    :param session: sqlalchmey session from decorator
    :param user_id: int
    :param string: string
    """
    session.add(User(user_id, string))


@db_write
def set_string(session, user_id, string):
    """
    Set user's string

    :param session: sqlalchmey session from decorator
    :param user_id: int
    :param string: string
    """
    session.query(User).filter_by(id=user_id).first().string = string


@db_read
def get_string(session, user_id):
    """
    Get user's string or None if no such found

    :param session: sqlalchmey session from decorator
    :param user_id: int
    :return: string or None
    """
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return user.string
