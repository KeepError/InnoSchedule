from datetime import datetime

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean

from modules.core.source import Base


# what groups does the user belong to
user_group_association = Table('schedule_user_group_association', Base.metadata,
                               Column('user', Integer, ForeignKey('schedule_users.id')),
                               Column('group', Integer, ForeignKey('schedule_groups.name')))


class User(Base):
    __tablename__ = "schedule_users"

    id = Column(Integer, primary_key=True)
    alias = Column(String)
    is_configured = Column(Boolean)  # chosen groups are saved
    groups = relationship("Group", secondary=user_group_association)

    def __init__(self, id_, alias_):
        self.id = id_
        self.alias = alias_

    def __repr__(self):
        return f"User({self.id}, {self.alias})"


class Group(Base):
    __tablename__ = 'schedule_groups'

    name = Column(String, primary_key=True)
    lessons = relationship("Lesson", backref=backref("schedule_groups"))

    def __repr__(self):
        return f"Group({self.name})"


class Lesson(Base):
    __tablename__ = "schedule_lessons"

    id = Column(Integer, primary_key=True)
    group = Column(String, ForeignKey('schedule_groups.name'))
    subject = Column(String)
    teacher = Column(String)
    day = Column(Integer)
    start = Column(String)
    end = Column(String)
    room = Column(Integer)

    def __init__(self, group, subject, teacher, day, start, end, room):
        self.group = group
        self.subject = subject
        self.teacher = teacher
        self.day = day
        self.start = start
        self.end = end
        self.room = room

    def __repr__(self):
        return f"Lesson({self.subject}, {self.start})"

    @property
    def start_struct(self):
        """
        Converts start time from string to time object
        :return: datetime
        """
        return datetime.now().replace(hour=int(self.start[:2]), minute=int(self.start[3:]))

    @property
    def end_struct(self):
        """
        Converts end time from string to time object
        :return: datetime
        """
        return datetime.now().replace(hour=int(self.end[:2]), minute=int(self.end[3:]))

    @property
    def minutes_until_start(self):
        """
        Total number of minutes until lesson begins

        :return: int
        """
        seconds_left = (self.start_struct - datetime.now()).total_seconds()
        return round(seconds_left / 60)

    @property
    def minutes_until_end(self):
        """
        Total number of minutes until lesson ends

        :return: int
        """
        seconds_left = (self.end_struct - datetime.now()).total_seconds()
        return round(seconds_left / 60)

    def __lt__(self, other):
        """
        Compares this lesson with given. Used in lesson sort

        :param other: Lesson
        :return: boolean
        """
        return self.start_struct < other.start_struct

    def __str__(self):
        """
        Converts current lesson to string for easy output

        :return: String
        """
        return f"{self.subject}\n"\
               f"👨‍🏫 {self.teacher}\n"\
               f"🕐 {self.start} 	— {self.end}\n" \
               f"🚪 {self.room}\n"

    def get_str_current(self):
        """
        Returns string, which indicates how many time left until current lesson will be finished.
        Used when NOW button is pressed and current lesson is going

        :return: String
        """
        hours_until_end = self.minutes_until_end // 60
        return f"{self}⏸️ {str(hours_until_end)+'h ' if hours_until_end > 0 else ''}" \
               f"{self.minutes_until_end % 60}m\n"

    def get_str_future(self):
        """
        Returns string, which indicates how many time left until current lesson will be started.
        Used when NOW button is pressed and current lesson will start next

        :return: String
        """
        hours_until_start = self.minutes_until_start // 60
        return f"{self}▶ ️{str(hours_until_start)+'h ' if hours_until_start > 0 else ''}" \
               f"{self.minutes_until_start % 60}m\n"
