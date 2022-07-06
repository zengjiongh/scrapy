# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGuessItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    name = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    year = scrapy.Field()
    mouth = scrapy.Field()
    Praise_rate = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()

