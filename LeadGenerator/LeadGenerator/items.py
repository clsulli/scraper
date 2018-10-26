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
    email = scrapy.Field()
    website = scrapy.Field()
    search_location = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
