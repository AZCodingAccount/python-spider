# 数据处理相关的包
import re
# 请求相关的包
import random
import time
import requests
from lxml import etree
# 数据库的包
import pymysql
from pymongo import MongoClient
import redis

"""
            案例爬取：段子星。需求：爬取段子星首页的前20页段子，段子名—段子日期-段子作者-段子阅读量-段子评论-段子详细内容描述存储到数据库。
        由于主要是数据库案例，因此主要是存储到数据库的操作
"""


# 创建一个递归函数，用来转换文章详情的多重列表(如果有的话)
def recursive_join(lst, separator='\n'):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.append(recursive_join(item, separator))
        else:
            result.append(item)
    return separator.join(result)


# 把之前封装好的集合给组装成一条一条的数据返回回去，清洗一下数据
def trans_dict(crawl_result):
    result = []
    for i in range(0, len(crawl_result['title'])):
        one_res = {}
        for key, value in crawl_result.items():
            # print(key, value)  # 此时value是一个列表，接下来通过索引组装每一个段子
            # print(value[i])
            one_res[key] = value[i]
        one_res['detail'] = recursive_join(one_res['detail']) if isinstance(one_res['detail'], list) else one_res[
            'detail']
        result.append(one_res)
    return result


# 对请求回来的数据进行解析封装
def extract_html():
    # 定义一下抓取的列表
    title = []
    date = []
    author = []
    views_counts = []
    comments_counts = []
    detail_list = []
    for page_count in range(1, 21):
        time.sleep(random.randint(1, 3))
        url = "https://duanzixing.com/page/%d/" % page_count
        response = requests.get(url, headers=headers)
        # 使用xpath解析
        html = etree.HTML(response.text)
        # 获取段子标题
        one_page_title = html.xpath("/html/body/section/div/div/article/header/h2/a/text()")
        # 获取段子发布日期
        one_page_date = html.xpath("/html/body/section/div/div/article/p[1]/time/text()")
        # 获取段子作者
        one_page_author = html.xpath("/html/body/section/div/div/article/p[1]/span[1]/text()")
        # 获取段子浏览量
        views = html.xpath("/html/body/section/div/div/article/p[1]/span[2]/text()")
        one_page_views_counts = []
        # 处理views
        for view in views:
            views_count = re.findall(r"\d{1,}", view)[0]
            one_page_views_counts.append(views_count)
        # 获取评论数
        comments = html.xpath("/html/body/section/div/div/article/p[1]/a/text()")
        # 处理comments
        # comments_count = []
        # [comments_count.append(re.findall(r"\d+", comment)[0]) for comment in comments]
        one_page_comments_counts = [re.findall(r"\d+", comment)[0] for comment in comments]
        # 获取段子详情，这个需要进到段子里面，先获取段子详情页的url
        detail_urls = html.xpath("/html/body/section/div/div/article/header/h2/a/@href")
        # 对每个url进行requests请求，获取详情页的源码
        detail_code_list = [requests.get(detail_url, headers=headers).text for detail_url in detail_urls]
        # 再对每个详情页进行提取数据，存到detail_list这个列表中，这里需要注意，源码是根据<br>分割，因此会转换成列表。
        one_page_detail_list = [etree.HTML(detail_code).xpath("/html/body/section/div/div/article/p/text()") for
                                detail_code in detail_code_list]
        # 处理特殊字符
        for i in range(len(one_page_detail_list)):
            for j in range(len(one_page_detail_list[i])):
                one_page_detail_list[i][j] = one_page_detail_list[i][j].replace("\u200b", "")
        # 装到之前的列表里面
        title.extend(one_page_title)
        date.extend(one_page_date)
        author.extend(one_page_author)
        views_counts.extend(one_page_views_counts)
        comments_counts.extend(one_page_comments_counts)
        detail_list.extend(one_page_detail_list)
        print(f"第{page_count}页抓取封装完成~")
    # 把之前的数据封装成一个字典
    crawl_result = {'title': title, 'date': date, 'author': author, 'views_counts': views_counts,
                    'comments_counts': comments_counts, 'detail': detail_list}
    print("正在存储到数据库中~")
    return crawl_result


# 存储到MySQL数据库
def save_to_mysql(result):
    try:
        # TODO：存储到MySQL数据库
        # 连接数据库
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="spidertestdb")
        cursor = db.cursor()
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
        cursor.execute(create_sql)
        delete_sql = "delete from jokes"
        # 删除之前的数据
        cursor.execute(delete_sql)
        # 往数据库插入数据
        # 遍历之前的字典
        for one_res in result:
            insert_sql = f"""
            insert into jokes (title, date, author, views_count, comments_count, detail)
            values (%s, %s, %s, %s, %s, %s)
            """
            try:
                inserted_count = cursor.execute(insert_sql, (
                    one_res['title'], one_res['date'], one_res['author'], one_res['views_counts'],
                    one_res['comments_counts'],
                    one_res['detail']))
                # print(f"插入了{inserted_count}条数据")
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"数据异常，回滚了~. 错误信息: {e},{one_res}")
        print("向MySQL数据库存储数据存储成功")
    except Exception as e:
        print(f"Mysql-未知异常~，异常信息为{e}")


# 存储到MongoDB数据库
def save_to_mongodb(result):
    try:
        # TODO:存储到MongoDB数据库
        # 连接数据库
        conn = MongoClient(host="localhost", port=27017)
        # 创建集合，插入数据时会自动创建
        spider_collection = conn.test.spider
        # 删除集合里面的数据
        spider_collection.delete_many({})
        # 遍历列表，把每一条数据都插入进去
        for one_result in result:
            try:
                one = spider_collection.insert_one(one_result)
                # print(f"数据插入成功，插入数据的id为{one.inserted_id}")
            except Exception as e:
                print(f"数据插入失败，异常信息为{e}")
        print("向MongoDB数据库存储数据存储成功")
    except Exception as e:
        print(f"未知异常~异常信息为{e}")


# 存储到redis数据库
def save_to_redis(result):
    try:
        # TODO:存储到redis数据库
        # 连接数据库
        r = redis.StrictRedis(host="192.168.182.100", port=6380, password='123456', db=0, decode_responses=True)
        # 清空之前库中的数据
        r.flushall()
        # 因此采用redis的hash表来存储每一个段子，然后把hash表的对应段子的所有key存储到一个列表的一个key中作为value。
        # 这里我采用redis的incr函数，那么就相当于1-这个joke_id_counter的value都是hash表里面的键了
        # 但是这个是不考虑删除的情况，要是删除了这个值不会变，这个时候再定义一个列表或者Bitmap就行了
        # 遍历列表，把每一条数据都插入进去
        for one_result in result:
            # 首先生成一个id
            id = r.incr("joke_id_counter")
            r.hset(id, mapping=one_result)
        # 获取一下这个joke_id_counter里面的值，看看是不是正常的增加了
        count = r.get("joke_id_counter")
        # print(f"redis数据库现在段子数据共有{count}条")
        print("向Redis数据库存储数据存储成功")
    except Exception as e:
        print(f"Redis-未知异常~，异常信息为{e}")


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57'
    }
    url = "https://duanzixing.com/"
    # 封装数据
    crawl_result = extract_html()
    # 把数据转换成易于存储于数据库的格式
    result = trans_dict(crawl_result)
    # 所有数据都准备完毕了，接下来就是存储到数据库
    # 存储到mysql数据库
    save_to_mysql(result)
    # 存储到mongoDB数据库
    save_to_mongodb(result)
    # 这时需要注意，result被MongoDB数据库修改了加了一个_id，因此解决方法可以是在redis中把主键给删了或者重新转换一下
    result = trans_dict(crawl_result)
    # 存储到redis数据库
    save_to_redis(result)
