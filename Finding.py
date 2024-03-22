from sqlalchemy import Column, String, Integer, DateTime, BINARY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class Finding(declarative_base()):
    __tablename__ = "findings"

    id = Column("id", Integer, primary_key=True)
    text = Column("text", String)
    username = Column("username", String)
    chanel_name = Column("chanel_name", String)
    object_vector = Column("object_vector", String)
    feature_vector = Column("feature_vector", String)
    phone_number = Column("phone_number", String)
    datetime = Column("datetime", DateTime)
    image = Column("image", BINARY)
    group_id = Column("group_id", ForeignKey("group.id"))

    def __init__(self, id, text, username, chanel_name, object_vector, feature_vector, datetime, phone_number, image):
        self.id = id
        self.text = text
        self.username = username
        self.object_vector = object_vector
        self.image = image
        self.feature_vector = feature_vector
        self.datetime = datetime
        self.phone_number = phone_number
        self.chanel_name = chanel_name

    def __repr__(self):
        return f"({self.id}) {self.username} {self.text} {self.object_vector} {self.image}"