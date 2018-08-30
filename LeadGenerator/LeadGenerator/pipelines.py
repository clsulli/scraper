# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem

class LeadgeneratorPipeline(object):

    def open_spider(self, spider):
        self.file = open('leads.jl', 'w')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        if item['location'] is not None:
            if item['location'].lower() == item['search_location']:
                line = json.dumps(dict(item)) + '\n'
                self.file.write(line)
                return item
            else:
                raise DropItem("Locations do not match in {}".format(item))
        else:
            raise DropItem("Location is None in {}".format(item))
