import json
import random
import re
import time

import requests
import scrapy
from lxml import etree

from ..items import ScrapyItem

"""
            scrapy底层是基于协程的，这里还是之前的数据库的案例，看一下同样是存储20页数据，scrapy有多快。基础的scrapy使用就演示下面几点：
        1：scrapy发送请求和转发请求
        2：scrapy把数据转发到管道存储到数据库
        3：items的使用
"""


class JokeSpider(scrapy.Spider):
    name = "joke"
    allowed_domains = ["duanzixing.com"]
    start_urls = ["https://duanzixing.com"]

    def get_data(self, response):
        # TODO：常用的就是一个url和text，响应头也可以
        # # 获取响应的url地址
        print(f"响应的url：{response.url}")
        # # 获取当前响应对应的请求的url地址
        # print(f"请求的url：{response.request.url}")
        # # 解码响应头
        # decoded_response_headers = {
        #     k.decode('utf-8'): [v.decode('utf-8') for v in v_list]
        #     for k, v_list in response.headers.items()
        # }
        # print(f"响应头：{decoded_response_headers}")
        #
        # # 解码请求头
        # decoded_request_headers = {
        #     k.decode('utf-8'): [v.decode('utf-8') for v in v_list]
        #     for k, v_list in response.request.headers.items()
        # }
        # print(f"响应的请求头：{decoded_request_headers}")
        # # 获取响应体
        # # print(f"响应体为：{response.body}")
        # # 返回响应的内容（字符串形式）
        # # print(f"响应内容为：{response.text}")
        # # 获取响应状态码
        # print(f"响应状态码：{response.status}")
        # # 获取返回的json数据（解析不了会报错，用于请求后台接口的场景）
        # # json_data = json.loads(response.text)
        # # print(f"返回的json数据为：{json_data}")

    def parse(self, response, **kwargs):
        # self.get_data(response)
        # 获取请求的url
        url = "https://duanzixing.com/page/%d/"
        # 循环获取数据
        for page_count in range(1, 21):
            time.sleep(random.randint(1, 3))
            page_url = url % page_count
            # 把请求转发给parse_data这个方法进行处理
            yield scrapy.Request(page_url, callback=self.parse_data, meta={'url': page_url})

    def parse_data(self, response, **kwargs):
        # 这个url还是有用的，这个案例不按照顺序存，如果需要顺序存的时候把字典加个标志key就可以了，到时候排个序。
        url = response.meta['url']
        # 获取到这个response，就可以进行解析了
        # 获取段子标题
        one_page_title = response.xpath("/html/body/section/div/div/article/header/h2/a/text()").extract()
        # 获取段子发布日期
        one_page_date = response.xpath("/html/body/section/div/div/article/p[1]/time/text()").extract()
        # 获取段子作者
        one_page_author = response.xpath("/html/body/section/div/div/article/p[1]/span[1]/text()").extract()
        # 获取段子浏览量
        views = response.xpath("/html/body/section/div/div/article/p[1]/span[2]/text()").extract()
        one_page_views_counts = []
        # 处理views
        for view in views:
            views_count = re.findall(r"\d{1,}", view)[0]
            one_page_views_counts.append(views_count)
        # 获取评论数
        comments = response.xpath("/html/body/section/div/div/article/p[1]/a/text()").extract()
        # 处理comments
        # comments_count = []
        # [comments_count.append(re.findall(r"\d+", comment)[0]) for comment in comments]
        one_page_comments_counts = [re.findall(r"\d+", comment)[0] for comment in comments]

        # 获取段子详情，这个需要进到段子里面，先获取段子详情页的url
        detail_urls = response.xpath("/html/body/section/div/div/article/header/h2/a/@href").extract()
        # 对每个url进行requests请求，获取详情页的源码，这里当然也可以把所有参数带着转发给一个函数。scrapy.Request(...)，
        # 但是为了简便就不这么写了。缺点就是变成同步的了。也可以使用async那一套
        detail_code_list = [requests.get(detail_url, headers=self.settings.get('DEFAULT_REQUEST_HEADERS')).text for
                            detail_url in detail_urls]
        # 再对每个详情页进行提取数据，存到detail_list这个列表中，这里需要注意，源码是根据<br>分割，因此会转换成列表。
        one_page_detail_list = [etree.HTML(detail_code).xpath("/html/body/section/div/div/article/p/text()") for
                                detail_code in detail_code_list]
        # 处理特殊字符
        for i in range(len(one_page_detail_list)):
            for j in range(len(one_page_detail_list[i])):
                one_page_detail_list[i][j] = one_page_detail_list[i][j].replace("\u200b", "")
        # 把之前的数据封装成一个字典
        crawl_result = {'title': one_page_title, 'date': one_page_date, 'author': one_page_author,
                        'views_counts': one_page_views_counts,
                        'comments_counts': one_page_comments_counts, 'detail': one_page_detail_list}
        # 转发给管道存储数据
        # yield crawl_result
        # 当然也可以使用之前的item
        item = ScrapyItem()
        item['title'] = one_page_title
        item['date'] = one_page_date
        item['author'] = one_page_author
        item['views_counts'] = one_page_views_counts
        item['comments_counts'] = one_page_comments_counts
        item['detail'] = one_page_detail_list
        yield item
