# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IfScraperItem(scrapy.Item):
    # path to downloads folder
    path = scrapy.Field()
    # custom filename : preserve order
    filename = scrapy.Field()
    # url to download from
    url = scrapy.Field()
    pass
