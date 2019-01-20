# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PabkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class novelItem(scrapy.Item):
    name = scrapy.Field()
    # novel name
    author = scrapy.Field()
    # author
    last_update = scrapy.Field()
    # last update
    cont_intro = scrapy.Field()
    # content introduction
    novelurl = scrapy.Field()
    # novel url