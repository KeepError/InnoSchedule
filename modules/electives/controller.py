"""
This is a controller that contains functions to manipulate database entities
related to electives. All the functions are designed with "fail-fast" philosophy
and raise exceptions if something goes wrong (querying nonexistent user for
example)
"""
from typing import List, Tuple

from sqlalchemy.orm import Session

from modules.core.source import db_write, db_read
from modules.electives.classes import Elective, ElectiveLesson, User


# Exceptions
class DBException(Exception):
    pass


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
def add_elective(session: Session, elective: Elective):
    """
    Save one elective to DB. If it already exists, raise DBException
    """
    inserted_elective = Elective(elective.name,
                                 elective.teacher,
                                 elective.acronym,
                                 elective.group)
    if session.query(Elective).filter_by(name=elective.name).count() == 0:
        session.add(inserted_elective)
        session.commit()
    else:
        raise DBException("Elective already exists")
    elective.id = inserted_elective.id


@db_read
def get_elective(session: Session, elective_id: int) -> Elective:
    """
    Get elective from db based on its id
    """
    return session.query(Elective).filter_by(id=elective_id).one()


@db_read
def get_all_electives(session: Session) -> List[Elective]:
    """
    Return list of all available electives loaded from DB. List can be empty
    """
    return session.query(Elective).all()


@db_write
def delete_elective(session: Session, elective_id: int):
    q_elective = session.query(Elective).filter(Elective.id == elective_id).one()
    # To use sqlalchemy autodeletes, they should be done like this
    session.delete(q_elective)


@db_read
def get_categories(session: Session) -> List[str]:
    groups: List[Tuple[str]] = session.query(Elective.group).distinct()
    return [group[0] for group in groups]


#
# Lessons
#

@db_write
def delete_lessons(session: Session):
    session.query(ElectiveLesson).delete()


@db_write
def delete_lesson(session: Session, lesson: ElectiveLesson):
    session.query(ElectiveLesson).filter_by(elective_id=lesson.elective_id,
                                            datetime=lesson.date_time).delete()


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
    if session.query(User).filter_by(chat_id=user.chat_id).count() == 0:
        inserted_user = User(user.chat_id)
        session.add(inserted_user)


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
    inserted_lesson = ElectiveLesson(room=lesson.room, date_time=lesson.date_time)
    inserted_lesson.elective_id = elective_id
    session.add(inserted_lesson)
    q_elective = session.query(Elective).filter(Elective.id == elective_id).one()
    q_elective.lessons.append(inserted_lesson)


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
