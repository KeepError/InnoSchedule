from copy import copy
from typing import List

from sqlalchemy.orm import Session

from modules.core.source import db_write, db_read
from modules.electives.classes import Elective, ElectiveLesson, User


#
# Electives
#

@db_write
def delete_electives(session: Session):
    """
    Delete all electives from DB
    """
    session.query(Elective).delete()


@db_write
def save_electives(session: Session, electives: List[Elective]):
    """
    Save list of electives to DB
    """
    session.add(electives)


@db_read
def get_all_electives(session: Session) -> List[Elective]:
    """
    Return list of all available electives loaded from DB
    """
    return session.query(Elective).all()


@db_write
def delete_elective(session: Session, elective_id: int):
    q_elective = session.query(Elective).filter(Elective.id == elective_id).one()
    session.delete(q_elective)


#
# Lessons
#

@db_write
def delete_lessons(session: Session):
    session.query(ElectiveLesson).delete()


@db_read
def get_lessons(session: Session) -> List[ElectiveLesson]:
    return session.query(ElectiveLesson).all()


#
# User
#

@db_read
def get_user(session: Session, user_id: int) -> User:
    return session.query(User).filter(User.chat_id == user_id).one()


@db_write
def register_user(session: Session, user: User):
    q_user = copy(user)
    if session.query(User).filter_by(chat_id=user.chat_id).count() == 0:
        session.add(q_user)


@db_write
def delete_user(session: Session, user_id: int):
    session.query(User).filter_by(chat_id=user_id).delete()


#
# Relations
#

@db_write
def add_elective_lesson(session: Session, elective_id: int, lesson: ElectiveLesson):
    """
    Creates lesson record for elective. Objects, passed as parameters should be
    reloaded then
    """
    lesson.elective_id = elective_id
    session.add(lesson)
    # Since objects can be not bound to session, we should query them from db
    q_lesson = session.query(ElectiveLesson).filter(
        ElectiveLesson.datetime == lesson.datetime and
        ElectiveLesson.elective_id == elective_id).one()
    q_elective = session.query(Elective).filter(Elective.id == elective_id).one()
    q_elective.lessons.append(q_lesson)


@db_read
def get_lessons_of_elective(session: Session, elective_id: int) -> List[ElectiveLesson]:
    q_elective = session.query(Elective).filter_by(id=elective_id).one()
    return q_elective.lessons


@db_read
def get_electives_of_user(session: Session, user: User) -> List[Elective]:
    q_user = session.query(User).filter_by(chat_id=user.chat_id).one()
    return q_user.electives


@db_write
def enroll(session: Session, elective_id: int, user_id: int):
    q_elective = session.query(Elective).filter_by(id=elective_id).one()
    q_user = session.query(User).filter_by(chat_id=user_id).one()
    q_elective.users.append(q_user)


@db_write
def un_enroll(session: Session, elective_id: int, user_id: int):
    q_user = session.query(User).filter(User.chat_id == user_id).one()
    q_elective = session.query(Elective).filter(Elective.id == elective_id).one()
    q_elective.users.remove(q_user)
