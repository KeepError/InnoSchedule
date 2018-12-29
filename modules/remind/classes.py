from sqlalchemy import Column, Integer

from modules.core import source as core


class User(core.Base):
    """
    Remind module users
    Stored to remember who wants to be reminded
    """

    __tablename__ = "remind_users"

    id = Column(Integer, primary_key=True)

    def __init__(self, id_):
        self.id = id_

    def __repr__(self):
        return f"User({self.id})"
