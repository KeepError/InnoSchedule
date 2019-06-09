from sqlalchemy import Column, Integer

from modules.core.source import Base


class User(Base):
    """
    Remind module users
    Stored to remember who wants to be reminded
    """

    __tablename__ = "remind_users"

    id = Column(Integer, primary_key=True, unique=True)

    def __init__(self, id_):
        self.id = id_

    def __repr__(self):
        return f"User({self.id})"
