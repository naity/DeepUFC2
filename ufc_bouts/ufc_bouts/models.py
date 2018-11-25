from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from . import settings


DeclarativeBase = declarative_base()


def db_connect():
    """ Database connection, return an sqlalchemy engine database"""
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class UfcBoutItem(DeclarativeBase):
    """Model for the postgres database"""
    __tablename__ = "ufc_bouts"

    id = Column("bout_id", Integer, primary_key=True)
    event_name = Column("event_name", String)
    date = Column("date", Date)
    location = Column("location", String)
    attendance  = Column("attendance ", Integer, nullable=True)
    result = Column("result", String)
    fighter1 = Column("fighter1", String)
    fighter2 = Column("fighter2", String)
    winner = Column("winner", String, nullable=True)
    weight_class = Column("weight_class", String)
    title_fight = Column("title_fight", Boolean)
    method = Column("method", String)
    end_round = Column("end_round", Integer)
    end_time = Column("end_time", String)
