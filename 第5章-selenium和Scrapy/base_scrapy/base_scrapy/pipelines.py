# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyPipeline:
    # 定义一些日志的变量
    page_count = 0
    count = 0
    start_time = None
    end_time = None

    # 创建一个递归函数，用来转换文章详情的多重列表(如果有的话)
    def recursive_join(self, lst, separator='\n'):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.append(self.recursive_join(item, separator))
            else:
                result.append(item)
        return separator.join(result)

    # 把之前封装好的集合给组装成一条一条的数据返回回去，清洗一下数据
    def trans_dict(self, crawl_result):
        result = []
        for i in range(0, len(crawl_result['title'])):
            one_res = {}
            for key, value in crawl_result.items():
                # print(key, value)  # 此时value是一个列表，接下来通过索引组装每一个段子
                # print(value[i])
                one_res[key] = value[i]
            one_res['detail'] = self.recursive_join(one_res['detail']) if isinstance(one_res['detail'], list) else \
                one_res[
                    'detail']
            result.append(one_res)
        return result

    def open_spider(self, spider):
        self.start_time = time.time()
        print('初始化数据库连接中......')

        # TODO：存储到MySQL数据库
        # 连接数据库
        self.db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="spidertestdb")
        self.cursor = self.db.cursor()
        # 创建表（title varchar给大点，500的话utf8就是500/3个汉字，uft8mb4就是125个汉字）
        create_sql = """
                   create table if not exists jokes
                   (
                       id             int primary key auto_increment comment '主键',
                       title          varchar(500) comment '段子标题',
                       date           date comment '段子发布日期',
                       author         varchar(100) comment '段子作者',
                       views_count    int comment '浏览量',
                       comments_count int comment '评论数',
                       detail         text comment '段子内容'
                   )
                   """
        # 建表语句
        self.cursor.execute(create_sql)
        delete_sql = "delete from jokes"
        # 删除之前的数据
        self.cursor.execute(delete_sql)
        print("数据库连接初始化成功")

    # 爬虫文件中提取数据的方法每yield一次item，就会运行一次
    # 在这里转换数据类型和存储到mysql数据库
    def process_item(self, item, spider):
        # spider可以获取转发过来的item的spider的属性，方法和名称。如
        # print(spider.name)    joke
        self.page_count += 1
        print(f"请稍等，正在为您努力爬取数据......已爬取{self.page_count}页")
        # 这里需要转换一下，把返回的数据转换成可以插入到数据库的格式
        result = self.trans_dict(item)
        # 往数据库插入数据
        # 遍历之前的字典
        for one_res in result:
            insert_sql = f"""
                    insert into jokes (title, date, author, views_count, comments_count, detail)
                    values (%s, %s, %s, %s, %s, %s)
                    """
            try:
                inserted_count = self.cursor.execute(insert_sql, (
                    one_res['title'], one_res['date'], one_res['author'], one_res['views_counts'],
                    one_res['comments_counts'],
                    one_res['detail']))
                self.count += inserted_count
                # print(f"插入了{inserted_count}条数据")
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(f"数据异常，回滚了~. 错误信息: {e},{one_res}")
        return item

    def close_spider(self, spider):
        self.end_time = time.time()
        print(
            f'共爬取了{self.count}条数据，已存储到MySQL数据库中，花费{self.end_time - self.start_time}秒\n关闭数据库连接中......')
        self.db.close()
        print("数据库连接关闭成功")
