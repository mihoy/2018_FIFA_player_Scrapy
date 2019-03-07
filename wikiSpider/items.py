# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WikispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    name = scrapy.Field()
    link = scrapy.Field()
    numb = scrapy.Field()
    position = scrapy.Field()
    DOB = scrapy.Field()
    caps = scrapy.Field()
    goals = scrapy.Field()
    club = scrapy.Field()
    team = scrapy.Field()
    citizenship = scrapy.Field()
    mass = scrapy.Field()
    participated = scrapy.Field()
    height = scrapy.Field()
    #freeBaseID = scrapy.Field()
    FIFAID = scrapy.Field()
    TransferMKT_ID = scrapy.Field()


    pass