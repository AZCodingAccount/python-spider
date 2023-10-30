# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 这里为了简便，写到三个不同的md文件里面就可以了
class BaseScrapyPlusPipeline:
    content = None
    tag = None
    cate = None

    def open_spider(self, spider):
        print("初始化环境中~")
        if not os.path.exists('./爬取的文件'):
            os.mkdir('./爬取的文件')
        self.content = open('./爬取的文件/文章.md', mode='w', encoding='utf-8')
        self.tag = open('./爬取的文件/标签.md', mode='w', encoding='utf-8')
        self.cate = open('./爬取的文件/分类.md', mode='w', encoding='utf-8')

    def process_item(self, item, spider):
        # 判断传过来的item是哪个方法传过来的
        if 'title' in item:
            print("文章正在写入中......")
            self.content.write("# ")
            self.content.write(item['title'])
            self.content.write("\n")
            self.content.write(item['content'].replace("#", ""))
            self.content.write("\n")
        elif 'tag' in item:
            print("标签正在写入中......")
            self.tag.write("## ")
            self.tag.write(item['tag'])
            self.tag.write("\n")
            for title in item['tag_title']:
                self.tag.write('- ')
                self.tag.write(title)
                self.tag.write("\n")
        elif 'cate' in item:
            print("分类正在写入中......")
            self.cate.write("## ")
            self.cate.write(item['cate'])
            self.cate.write("\n")
            for title in item['cate_title']:
                self.cate.write('- ')
                self.cate.write(title)
                self.cate.write("\n")
        return item

    def close_spider(self, spider):
        print(f"网站经过筛选的总url数量为：{spider.count}")
        print("关闭环境中")
        self.content.close()
        self.tag.close()
        self.cate.close()
