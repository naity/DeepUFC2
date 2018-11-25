# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class UfcFighterItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    win = scrapy.Field(output_processor=TakeFirst())
    lose = scrapy.Field(output_processor=TakeFirst())
    draw = scrapy.Field(output_processor=TakeFirst())
    nc = scrapy.Field(output_processor=TakeFirst())
    height = scrapy.Field(output_processor=TakeFirst())
    weight = scrapy.Field(output_processor=TakeFirst())
    reach = scrapy.Field(output_processor=TakeFirst())
    stance = scrapy.Field(output_processor=TakeFirst())
    dob = scrapy.Field(output_processor=TakeFirst())
    SLpM = scrapy.Field(output_processor=TakeFirst())
    Str_Acc = scrapy.Field(output_processor=TakeFirst())
    SApM = scrapy.Field(output_processor=TakeFirst())
    Str_Def = scrapy.Field(output_processor=TakeFirst())
    TD_Avg = scrapy.Field(output_processor=TakeFirst())
    TD_Acc = scrapy.Field(output_processor=TakeFirst())
    TD_Def = scrapy.Field(output_processor=TakeFirst())
    Sub_Avg = scrapy.Field(output_processor=TakeFirst())
    last_updated = scrapy.Field(output_processor=TakeFirst())
