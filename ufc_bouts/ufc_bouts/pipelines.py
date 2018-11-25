# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from .models import UfcBoutItem, db_connect, create_table

class CreateOrIgnore(object):
    """
    A filter that takes care of duplicate items
    """

    def create_or_ignore(self, item, session):
        """ early UFC events followed a tournament format, so fighters
        might fight multiple times in a single event, crazy shit"""

        bout = session.query(UfcBoutItem).\
        filter_by(date=item["date"]).\
        filter_by(fighter1=item["fighter1"]).\
        filter_by(fighter2=item["fighter2"]).\
        filter_by(end_round=item["end_round"]).\
        filter_by(end_time=item["end_time"]).first()

        # if match does not exit, create a new entry
        # otherwise ignore
        if not bout:
            bout = UfcBoutItem(**item)
            session.add(bout)


class UfcBoutPipeline(object):
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
            CreateOrIgnore().create_or_ignore(item=item, session=session)
            session.commit()
        except:
            # undo in case of errors
            session.rollback()
            raise
        finally:
            session.close()

        return item
