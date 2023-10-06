# 导入请求和解析数据模块
import time

import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# 采用新发地这个网站做演示，由于这个网站的数据是使用JS动态加载的，并且我还可以直接向他们服务器发送数据请求接口，简单一点直接请求json数据解析就可以了
# 简单一点，就直接算一个蔬菜类一个小类的平均价格了，     因为如果不传这个品类id的话，默认他这个接口返回的是蔬菜类的。
# 当然，还可以拿到所有品类的详细数据，导出做各种数据分析，这里就不这样做了，毕竟是练习bs4库（虽然网站改版了没有练习到）
# 发送请求
url = 'http://www.xinfadi.com.cn/getPriceData.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
# 定义页数,总价格，查找时间
page_count = 1
sum_avg_Price = 0
pubDateEndTime = datetime.today().strftime("%Y/%m/%d")
pubDateStartTime = (datetime.today() - timedelta(days=30)).strftime("%Y/%m/%d")
# 选择蔬菜->水菜这个品类来进行统计，统计最近30天的平均价格（没办法不传品类id，不传品类id不能通过时间段请求）
data = {
    'limit': 20,
    'current': page_count,
    "pubDateStartTime": pubDateStartTime,
    "pubDateEndTime": pubDateEndTime,
    "prodPcatid": 1186,
    "prodCatid": 1199
}
response = requests.post(url, headers=headers, data=data)
total = response.json()['count']
# 定义一个while循环爬取数据，一次爬取20条
while response.json()['list']:
    # 睡眠0.5秒以免给别人的服务器造成负担
    time.sleep(0.5)
    # 指针+1
    page_count = page_count + 1
    # 拿出来每个品类的avgPrice，然后求一个平均
    goodsList = response.json()['list']
    for goods in goodsList:
        sum_avg_Price += float(goods['avgPrice'])
    # 更新请求体重发请求
    data = {
        'limit': 20,
        'current': page_count,
        "pubDateStartTime": pubDateStartTime,
        "pubDateEndTime": pubDateEndTime,
        "prodPcatid": 1186,
        "prodCatid": 1199
    }
    response = requests.post(url, headers=headers, data=data)

print(
    f"根据爬虫数据显示：最近一个月新发地蔬菜大类下的水菜数据一共有{page_count}页{total}条，平均销售价格为：{round(sum_avg_Price / total, 2)}")
