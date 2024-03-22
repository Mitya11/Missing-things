from sqlalchemy import Column, String, Integer, DateTime, BINARY, Enum
from sqlalchemy.ext.declarative import declarative_base
from GroupType import GroupType


class Group(declarative_base()):
    __tablename__ = "group"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    city = Column("city", String)
    type = Column("type", Enum(GroupType))
    last_message = Column("last_message", Integer)

    def __init__(self, id, name, city, type, last_message):
        self.id = id
        self.name = name
        self.city = city
        self.type = type
        self.last_message = last_message
