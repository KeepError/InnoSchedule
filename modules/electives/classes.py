from sqlalchemy import Column, String, Integer, Table, ForeignKey

from modules.core.source import Base

# Table which stores which user has which elective
user_elective_association = Table(
    'electives_user_elective_association', Base.metadata,
    Column('user', Integer, ForeignKey('schedule_users.id')),
    Column('elective', Integer, ForeignKey('electives_elective.id')),
)


class Elective(Base):
    """
    Class that represent elective course. It is not required for user to be in
    a specific group, so each user should enroll individually.
    """
    __tablename__ = "electives_elective"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher = Column(String)
    block = Column(Integer)
    room = Column(Integer)
    acronym = Column(String)

    def __init__(self, name, teacher, block, room, acronym):
        self.acronym = acronym
        self.room = room
        self.block = block
        self.teacher = teacher
        self.name = name
