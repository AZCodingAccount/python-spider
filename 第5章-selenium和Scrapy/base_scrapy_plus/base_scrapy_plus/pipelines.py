# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 这里为了简便，写到三个不同的txt文件里面就可以了
class BaseScrapyPlusPipeline:
    def open_spider(self, spider):
        print("爬虫开始了~")

    def process_item(self, item, spider):
        # print(item)
        return item

    def close_spider(self, spider):
        print(f"网站总url数量为：{spider.count}")
