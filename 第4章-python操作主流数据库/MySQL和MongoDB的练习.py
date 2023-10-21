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
comments_count = [re.findall(r"\d+", comment)[0] for comment in comments]
# 获取段子详情，这个需要进到段子里面
detail = html.xpath("/html/body/section/div/div/article/p[2]/text()")
print(detail)
