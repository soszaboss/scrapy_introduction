# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from dataclasses import dataclass

class BookItems(scrapy.Item):
    title = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=float)
    description = scrapy.Field(serializer=str)
    upc = scrapy.Field(serializer=str)
    avaibility = scrapy.Field(serializer=int)
