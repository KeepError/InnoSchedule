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

    def __eq__(self, other: "User"):
        return self.chat_id == other.chat_id


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

    # Basically, group is the sheet name. Users not belong to it, it is just for convenience
    # of choosing elective from long list of available ones
    group: str = Column(String)

    lessons = relationship("ElectiveLesson", cascade="delete, delete-orphan", back_populates="elective")

    def __init__(self, name: str, teacher: str, acronym: str, group: str):
        self.acronym = acronym
        self.teacher = teacher
        self.name = name
        self.group = group

    def __eq__(self, other: "Elective"):
        return self.name == other.name and \
               self.teacher == other.teacher and \
               self.group == other.group


class ElectiveLesson(Base):
    """
    Class that represents one particular lesson on an elective
    """
    __tablename__ = "electives_lessons"
    date_time: datetime = Column(DateTime, primary_key=True)
    room: int = Column(Integer)
    elective_id = Column(Integer,
                         ForeignKey('electives_elective.id'), primary_key=True)
    elective = relationship("Elective", back_populates="lessons")

    def __init__(self, room: int, date_time: datetime):
        self.room = room
        self.date_time = date_time

    def __eq__(self, other: "ElectiveLesson"):
        return self.elective_id == other.elective_id and \
               self.date_time == other.date_time and \
               self.room == other.room
