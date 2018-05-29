# -*- coding: utf-8 -*-

"""
ORM for spendtrak database
"""
import datetime
import logging
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()


class User(Base):
    """
    ORM class for table users
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email_address = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255), nullable=False)
    last_updated = Column(DateTime, onupdate=datetime.datetime.now)
    accounts = relationship('Account', back_populates='user')


class Account(Base):
    """
    ORM class for table accounts
    """
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    flow_balance = Column(Float, nullable=False, default=0.0)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String(255), default=None)
    last_updated = Column(DateTime, onupdate=datetime.datetime.now)
    user = relationship('User', back_populates='accounts')

    def __str__(self):
        return 'name: [{0}], description: [{1}], balance: [{2}]'. \
            format(self.name, self.description, self.flow_balance)


def get_db_engine(dbname):
    db_str = 'sqlite:///' + dbname
    engine = create_engine(db_str, echo=True)
    return engine


def get_db_session(engine):
    Session.configure(bind=engine)
    session = Session()
    return session


def get_new_session(dbname):
    db_str = 'sqlite:///' + dbname
    engine = create_engine(db_str, echo=True)
    Session.configure(bind=engine)
    session = Session()
    return session


def persist_record(session, data):
    session.add(data)
    session.commit()


def main():
    engine = get_db_engine("/Users/suser/dev/python/spendtrak/data/spendtrak.db")
    session = get_db_session(engine)
    # user_a = User(last_name='Tom',
    #               email_address='tt@book.com',
    #               last_updated=datetime.datetime.now())
    # user_a.accounts = [
    #                     Account(name='tom-account', last_updated=datetime.datetime.now())
    # ]
    # persist_record(session, user_a)
    for user in session.query(User).filter(User.email_address == 'tt@book.com'):
        user.accounts.append(Account(name='tom-account2', last_updated=datetime.datetime.now()))
        persist_record(session, user)
    logging.info('task done')


if __name__ == "__main__":
    main()
