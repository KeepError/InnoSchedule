from typing import List

from sqlalchemy.orm import Session

from modules.core.source import db_write, db_read
from modules.electives.classes import Elective


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
