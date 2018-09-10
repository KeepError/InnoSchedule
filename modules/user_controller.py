import sqlite3
import threading

from modules.user import User

conn = sqlite3.connect('db.sqlite', check_same_thread=False)
cursor = conn.cursor()  # cursor allows to iterate over database data
lock = threading.RLock()  # at any moment of time only one thread may request db. All others are waiting


def register(user_id, alias):
    """
    Register new user in database

    :param user_id: int
    :param alias: string
    """
    with lock:
        cursor.execute("INSERT INTO users (telegram_id, telegram_alias) VALUES (?,?)", (user_id, alias,))
        conn.commit()


def set_course(user_id, course):
    """
    Set course for specified user

    :param user_id: int
    :param course: string
    """
    with lock:
        cursor.execute("UPDATE users SET course=? WHERE telegram_id=?", (course, user_id))
        conn.commit()


def set_course_group(user_id, course_group):
    """
    Set course group for specified user

    :param user_id: int
    :param course_group: string
    """
    with lock:
        cursor.execute("UPDATE users SET course_group=? WHERE telegram_id=?", (course_group, user_id))
        conn.commit()


def set_english_group(user_id, english_group):
    """
    Set english group for specified user

    :param user_id: int
    :param english_group: string
    """
    with lock:
        cursor.execute("UPDATE users SET english_group=? WHERE telegram_id=?", (english_group, user_id))
        conn.commit()


def set_reminders(user_id, need_reminders):
    """
    Set reminders for specified user
    0 - disable reminders
    1 - allow reminders

    :param user_id: int
    :param need_reminders: int [0-1]
    """
    with lock:
        cursor.execute("UPDATE users SET need_reminders=? WHERE telegram_id=?", (1 if need_reminders else 0, user_id))
        conn.commit()


def set_alias(user_id, alias):
    """
    Update user`s alias in database

    :param user_id: int
    :param alias: string
    """
    with lock:
        cursor.execute("UPDATE users SET telegram_alias=? WHERE telegram_id=?", (alias, user_id,))
        conn.commit()


def get(user_id):
    """
    Function returns User by his telegram id or None if user not found

    :param user_id: int
    :return: User or None
    """
    with lock:
        cursor.execute("SELECT * FROM users WHERE telegram_id=?", (user_id,))
        data = cursor.fetchone()
    return User(data) if data else None


def get_id_by_alias(alias):
    """
    Returns id of registered user by his telegram alias or None if user not found

    :param alias: string
    :return: int or None
    """
    with lock:
        cursor.execute("SELECT telegram_id FROM users WHERE telegram_alias=?", (alias,))
        data = cursor.fetchone()
    return data[0] if data else None


def is_configured(user_id):
    """
    Returns True if indicated user is registered and he entered all needed information about his course and groups

    :param user_id: int
    :return: boolean
    """
    user = get(user_id)
    if user and user.id and user.alias and user.course and user.course_group:
        if user.course == 1:  # first course must have english group
            return user.english_group
        return True
    return False


def is_registered(user_id):
    """
    Returns True if user with given id is registered in database

    :param user_id: int
    :return: boolean
    """
    return get(user_id) is not None


def delete(user_id):
    """
    Deletes user from database by his id.
    Function is called if some user blocked the bot in the telegram.

    :param user_id: int
    """
    with lock:
        cursor.execute("DELETE FROM users WHERE telegram_id=?", (user_id,))
        conn.commit()


def get_users_with_reminders():
    """
    Returns list of Users, who allowed to send them reminders

    :return: [User]
    """
    with lock:
        cursor.execute("SELECT * FROM users WHERE need_reminders=1")
        data = cursor.fetchall()
    return [User(x) for x in data]


def get_all_users():
    """
    Returns list of all Users

    :return: [User]
    """
    with lock:
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
    return [User(x) for x in data]
