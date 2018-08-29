# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Listing(scrapy.Item):
    name = scrapy.Field()
    detail_page = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    location = scrapy.Field()
