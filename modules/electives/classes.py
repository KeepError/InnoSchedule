from datetime import datetime
from sqlalchemy import Column, String, Integer, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from modules.core.source import Base

# Table that stores which user has which elective
user_elective_association = Table(
    'electives_user_elective_association', Base.metadata,
    Column('user', Integer, ForeignKey("electives_user.chat_id")),
    Column('elective', Integer, ForeignKey("electives_elective.id")),
)


class User(Base):
    """
    User who uses electives schedule functionality
    """
    __tablename__ = "electives_user"

    chat_id: int = Column(Integer, primary_key=True)
    electives = relationship(
        "Elective", secondary=user_elective_association,
        backref=backref('users', lazy='joined')
    )

    def __init__(self, chat_id: int):
        self.chat_id = chat_id


class Elective(Base):
    """
    Class that represent elective course. It is not required for user to be in
    a specific group, so each user should enroll individually.
    """
    __tablename__ = "electives_elective"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    teacher: str = Column(String)
    acronym: str = Column(String)

    lessons = relationship("ElectiveLesson", cascade="delete, delete-orphan")

    def __init__(self, name: str, teacher: str, acronym: str):
        self.acronym = acronym
        self.teacher = teacher
        self.name = name


class ElectiveLesson(Base):
    """
    Class that represents one particular lesson on an elective
    """
    __tablename__ = "electives_lessons"
    datetime: datetime = Column(DateTime, primary_key=True)
    room: int = Column(Integer)
    elective_id = Column(Integer,
                         ForeignKey('electives_elective.id'), primary_key=True)

    def __init__(self, room: int, date_time: datetime):
        self.room = room
        self.datetime = date_time
