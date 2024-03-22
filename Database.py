import datetime
from Finding import Finding

from sqlalchemy import create_engine, Column, String, Integer, DateTime, BINARY
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def add_finding(find):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(find)
    session.commit()

def find_by_vector():
    Session

def get_all():
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Finding).all()
    session.commit()
    return result



engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


date = datetime.date(2001, 1, 4)
find = Finding(13, "qwerty", "admin", "sdad", "dada.fda", "",
               date,"", None)




add_finding(find)
print(session.query(Finding).all())