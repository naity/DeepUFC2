# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class UfcBoutItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # use the TakeFirst processor, otherwise everything is a list
    event_name = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    location = scrapy.Field(output_processor=TakeFirst())
    attendance = scrapy.Field(output_processor=TakeFirst())
    result = scrapy.Field(output_processor=TakeFirst())
    fighter1 = scrapy.Field(output_processor=TakeFirst())
    fighter2 = scrapy.Field(output_processor=TakeFirst())
    winner = scrapy.Field(output_processor=TakeFirst())
    weight_class = scrapy.Field(output_processor=TakeFirst())
    title_fight = scrapy.Field(output_processor=TakeFirst())
    method = scrapy.Field(output_processor=TakeFirst())
    end_round = scrapy.Field(output_processor=TakeFirst())
    end_time = scrapy.Field(output_processor=TakeFirst())
