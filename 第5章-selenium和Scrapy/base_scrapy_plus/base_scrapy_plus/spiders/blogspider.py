import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from base_scrapy_plus.items import BaseScrapyPlusItem

"""
            这里演示scrapy的全站抓取和分布式爬虫，配置随机UA和手动维护cookie，全站抓取一定要慎重，不要影响别人网站的正常运行。配置好rules和delay。
        这里以我的博客演示，一共就几十个url，快一点点。
        但是这里需要思考，我们要哪个页面是为了提取什么数据，
                    打开具体的文章，就获取文章标题和内容。定义一个提取文章数据的方法parse_article
                    比如说我打开博客的标签，就是获取标签下的文章标题，就定义一个提取文章标题的方法parse_tag_headlines。
                    打开博客的分类，要获取当前分类下的文章标题，定义一个提取分类下面的标题长度方法parse_cate_headlines
        分别转发给不同的parse方法就可以了。引入分布式爬虫，快一些
"""


class BlogspiderSpider(RedisCrawlSpider):
    count = 0
    name = "blogspider"
    allowed_domains = ["bugdesigner.cn"]
    # start_urls = ["https://bugdesigner.cn"]
    redis_key = 'blogQuene'  # 使用管道名称

    rules = (
        Rule(LinkExtractor(allow=r"https://www.bugdesigner.cn/(?!tag/|cate/|aboutme/)[^/]+/$"),
             callback="parse_article",
             follow=True),
        # 匹配https://www.bugdesigner.cn/tag/开头的，中间匹配不是/的字符，遇到/结束
        Rule(LinkExtractor(allow=r"https://www.bugdesigner.cn/tag/[^/]+/$"),
             callback="parse_tag_headlines",
             follow=True),
        Rule(LinkExtractor(allow=r"https://www.bugdesigner.cn/category/[^/]+/$"),
             callback="parse_cate_headlines",
             follow=True),
        Rule(LinkExtractor(allow=r".*"), callback="parse_count", follow=False),)

    # 保底的方法
    def parse_count(self, response):
        self.count += 1
        # print(response.request.url)

    # 批量抓取文章
    def parse_article(self, response):
        # print(response.request.url)
        # 实例化item，一个字典
        item = BaseScrapyPlusItem()
        # 记录爬取的url个数
        self.count += 1
        # 提取博客文章标题
        item['title'] = response.xpath("/html/body/div[2]/div/div/div[1]/div[1]/div[2]/h1/text()").extract_first()
        # print(title)
        # print(response.text)
        # 提取博客文章内容
        item['content'] = response.xpath('//div[@id="lightgallery"]').extract_first()
        # print(content)
        yield item

    # 获取标签和对应的文章标题
    def parse_tag_headlines(self, response):
        self.count += 1
        # print(response.request.url)
        # 提取当前标签下面的所有文章标题，存储到item里面
        item = BaseScrapyPlusItem()
        # 获取标签名
        item['tag'] = response.xpath('//div[@class="k-header"]//div[@class="title"]/text()').extract_first()
        # 获取标签名下面的文章，文章不止一个
        item['tag_title'] = response.xpath('//div[@class="row"]//h3[@class="title"]/a/text()').extract()
        # print(item['tag'], item['tag_title'], self.i)
        yield item

    # 获取分类和对应的文章标题
    def parse_cate_headlines(self, response):
        self.count += 1
        # print(response.request.url)
        item = BaseScrapyPlusItem()
        # 提取文章分类名
        item['cate'] = response.xpath('//div[@class="k-header"]//div[@class="title"]/text()').extract_first()
        # 提取下面的文章名
        item['cate_title'] = response.xpath('//div[@class="row"]//h3[@class="title"]/a/text()').extract()
        # print(item['cate'], item['cate_title'])
        yield item
