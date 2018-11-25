# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from .models import UfcFighterItem, db_connect, create_table


class CreateOrUpdate(object):
    """
    A filter that takes care of duplicate items
    """

    def create_or_update(self, item, session):
        # in case fighters have the same name
        fighter = session.query(UfcFighterItem).\
            filter_by(name=item["name"]).\
            filter_by(height=item["height"]).\
            filter_by(dob=item["dob"]).first()

        # if fighter does not exit, create a new entry
        # otherwise update
        if not fighter:
            fighter = UfcFighterItem(**item)
            session.add(fighter)
        else:
            fighter.win = item["win"]
            fighter.lose = item["lose"]
            fighter.draw = item["draw"]
            fighter.nc = item["nc"]
            # in case fighter changes weight class
            fighter.weight = item["weight"]
            fighter.stance = item["stance"]
            fighter.SLpM = item["SLpM"]
            fighter.Str_Acc = item["Str_Acc"]
            fighter.SApM = item["SApM"]
            fighter.Str_Def = item["Str_Def"]
            fighter.TD_Avg = item["TD_Avg"]
            fighter.TD_Acc = item["TD_Acc"]
            fighter.TD_Def = item["TD_Def"]
            fighter.Sub_Avg = item["Sub_Avg"]
            fighter.last_updated = item["last_updated"]

class UfcFighterPipeline(object):
    def __init__(self):
        # initialize databse connection, session, and table
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save business in database,
        update rating and votes for duplicate genes.
        """

        session = self.Session()

        try:
            CreateOrUpdate().create_or_update(item=item, session=session)
            session.commit()
        except:
            # undo in case of errors
            session.rollback()
            raise
        finally:
            session.close()

        return item
