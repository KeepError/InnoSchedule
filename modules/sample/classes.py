from sqlalchemy import Column, Integer, String

from modules.core import source as core


class User(core.Base):
    """
    Sample module user
    """

    __tablename__ = "sample_users"

    id = Column(Integer, primary_key=True)
    string = Column(String)

    def __init__(self, id_, string_):
        self.id = id_
        self.string = string_
