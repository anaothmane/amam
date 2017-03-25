# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy.crawler import CrawlerProcess

class RefugeeScrapeItem(scrapy.Item):
    person=Field()
    comment=Field()
