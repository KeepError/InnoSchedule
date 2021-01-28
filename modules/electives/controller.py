from typing import List

from sqlalchemy import DateTime
from sqlalchemy.orm import Session

from modules.core.source import db_write, db_read
from modules.electives.classes import Elective, ElectiveLesson, User


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
    session.add_all(electives)


@db_read
def get_all_electives(session: Session) -> List[Elective]:
    """
    Return list of all available electives loaded from DB
    """
    return session.query(Elective).all()


@db_write
def add_elective_lesson(session: Session, elective: Elective, lesson: ElectiveLesson):
    """
    Creates lesson record for elective
    """
    session.add(lesson)
    session.refresh(elective)
    elective.lessons.append(lesson)


def enroll(elective: Elective, user: User):
    elective.users.append(user)


@db_read
def register_user(session: Session, user: User):
    session.add(user)


@db_write
def delete_elective(session: Session, elective: Elective):
    session.query(elective).delete()
