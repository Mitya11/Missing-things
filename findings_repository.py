from Finding import Finding
from sqlalchemy import create_engine, Column, String, Integer, DateTime, BINARY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///mydb.db", echo=True)

def add_finding(find):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(find)
    session.commit()


def find_by_vector():
    return 1


def get_all():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Finding).all()
    session.commit()
    return result