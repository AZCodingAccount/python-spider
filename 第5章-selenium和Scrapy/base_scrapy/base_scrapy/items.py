# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    views_counts = scrapy.Field()
    comments_counts = scrapy.Field()
    detail = scrapy.Field()
