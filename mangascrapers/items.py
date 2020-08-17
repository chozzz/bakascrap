# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MangascrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MangabookItem(scrapy.Item):
    source = scrapy.Field()
    uri = scrapy.Field()
    name = scrapy.Field()
    alternative_name = scrapy.Field()
    rating = scrapy.Field()
    author = scrapy.Field()
    genres = scrapy.Field()
    booktype = scrapy.Field()
    summary = scrapy.Field()
    thumbnail = scrapy.Field()
    pass

class MangapageItem(scrapy.Item):
    source = scrapy.Field()
    uri = scrapy.Field()
    page = scrapy.Field()
    images = scrapy.Field()
    pass