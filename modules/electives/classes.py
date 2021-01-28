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

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    teacher: str = Column(String)
    block: int = Column(Integer)
    room: int = Column(Integer)
    acronym: str = Column(String)

    def __init__(self, name: str, teacher: str, block: int, room: int, acronym: str):
        self.acronym = acronym
        self.room = room
        self.block = block
        self.teacher = teacher
        self.name = name

    def __str__(self):
        """
        Converts current lesson to string for easy output

        :return: String
        """
        return f"{self.name}\n" \
               f"👨‍🏫 {self.teacher}\n" \
               f"🕐 {self.block} 	— {self.acronym}\n" \
               f"🚪 {self.room if self.room != -1 else '?'}\n"
