import re

import pymysql
import requests
from lxml import etree

"""
            案例爬取：段子星。需求：爬取段子星首页的前10页，段子名—段子日期-段子作者-段子阅读量-段子评论-段子详细内容描述存储到数据库。
        由于主要是数据库案例，因此主要是存储到数据库的操作
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57'
}
url = "https://duanzixing.com/"
response = requests.get(url, headers=headers)
# 使用xpath解析
# print(response.text)
html = etree.HTML(response.text)
# 获取段子标题
title = html.xpath("/html/body/section/div/div/article/header/h2/a/text()")
# 获取段子发布日期
date = html.xpath("/html/body/section/div/div/article/p[1]/time/text()")
# 获取段子作者
author = html.xpath("/html/body/section/div/div/article/p[1]/span[1]/text()")
# 获取段子浏览量
views = html.xpath("/html/body/section/div/div/article/p[1]/span[2]/text()")
views_counts = []
# 处理views
for view in views:
    views_count = re.findall(r"\d{1,}", view)[0]
    views_counts.append(views_count)
# 获取评论数
comments = html.xpath("/html/body/section/div/div/article/p[1]/a/text()")
# 处理comments
# comments_count = []
# [comments_count.append(re.findall(r"\d+", comment)[0]) for comment in comments]
comments_counts = [re.findall(r"\d+", comment)[0] for comment in comments]
# 获取段子详情，这个需要进到段子里面，先获取段子详情页的url
detail_urls = html.xpath("/html/body/section/div/div/article/header/h2/a/@href")
# 对每个url进行requests请求，获取详情页的源码
detail_code_list = [requests.get(detail_url, headers=headers).text for detail_url in detail_urls]
# 再对每个详情页进行提取数据，存到detail_list这个列表中
detail_list = [etree.HTML(detail_code).xpath("/html/body/section/div/div/article/p/text()") for
               detail_code in detail_code_list]

# 把之前的数据封装成一个字典，这里一些详情里面的特殊的字符如\u200b就不处理了，有需要可以replace替换掉，不影响读取。
crawl_result = {'title': title, 'date': date, 'author': author, 'views_counts': views_counts,
                'comments_counts': comments_counts, 'detail': detail_list}
# print(crawl_result)
# 所有数据都准备完毕了，接下来就是存储到数据库
# 连接数据库
db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456", database="spidertestdb")
cursor = db.cursor()
# 创建表
create_sql = """
create table if not exists jokes
(
    id             int primary key auto_increment comment '主键',
    title          varchar(50) comment '段子标题',
    date           date comment '段子发布日期',
    author         varchar(20) comment '段子作者',
    views_count    int comment '浏览量',
    comments_count int comment '评论数',
    detail         text comment '段子内容'
)
"""
cursor.execute(create_sql)
# 往数据库插入数据
# 遍历之前的字典
for i in range(0, len(crawl_result['title'])):
    one_res = {}
    for key, value in crawl_result.items():
        # print(key, value)  # 此时value是一个列表，接下来通过索引组装每一个段子
        # print(value[i])
        one_res[key] = value[i]
    # 每次循环完一遍就插入数据库
    insert_sql = f"""
    insert into jokes (title, date, author, views_count, comments_count, detail)
    values (%s, %s, %s, %s, %s, %s)
    """
    try:
        detail_text = '\n'.join(one_res['detail']) if isinstance(one_res['detail'], list) else one_res['detail']
        inserted_count = cursor.execute(insert_sql, (
        one_res['title'], one_res['date'], one_res['author'], one_res['views_counts'], one_res['comments_counts'],
        detail_text))
        print(f"插入了{inserted_count}条数据")
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"数据异常，回滚了~. 错误信息: {e}")

