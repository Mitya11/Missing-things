from Group import Group
from sqlalchemy import create_engine, Column, String, Integer, DateTime, BINARY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///mydb.db", echo=True)

def add_finding(group):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(group)
    session.commit()


def get_all():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Group).all()
    session.commit()
    return result
