# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseScrapyPlusItem(scrapy.Item):
    # 定义一下需要爬取的数据,文章标题，内容，标签下面的文章标题，分类下面的文章标题
    # 这里规范的应该是定义三个不同的item类，这里为了简便就不定义了，不能为了规范而规范
    title = scrapy.Field()
    content = scrapy.Field()
    tag=scrapy.Field()
    tag_title=scrapy.Field()
    cate=scrapy.Field()
    cate_title=scrapy.Field()

