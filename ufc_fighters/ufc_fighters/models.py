from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from . import settings


DeclarativeBase = declarative_base()


def db_connect():
    """ Database connection, return an sqlalchemy engine database"""
    return create_engine(URL(**settings.DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class UfcFighterItem(DeclarativeBase):
    """Model for the postgres database"""
    __tablename__ = "ufc_fighters"

    id = Column("fighter_id", Integer, primary_key=True)
    name = Column("name", String)
    win = Column("win", String, nullable=True)
    lose = Column("lose", String, nullable=True)
    draw = Column("draw", String, nullable=True)
    nc = Column("nc", String, nullable=True)
    height = Column("height", String)
    weight = Column("weight", String)
    reach = Column("reach", String, nullable=True)
    stance = Column("stance", String, nullable=True)
    dob = Column("dob", String, nullable=True)
    SLpM = Column("SLpM", String, nullable=True)
    Str_Acc = Column("Str_Acc", String, nullable=True)
    SApM = Column("SApM", String, nullable=True)
    Str_Def = Column("Str_Def", String, nullable=True)
    TD_Avg = Column("TD_Avg", String, nullable=True)
    TD_Acc = Column("TD_Acc", String, nullable=True)
    TD_Def = Column("TD_Def", String, nullable=True)
    Sub_Avg = Column("Sub_Avg", String, nullable=True)
    last_updated = Column("last_updated", DateTime)


