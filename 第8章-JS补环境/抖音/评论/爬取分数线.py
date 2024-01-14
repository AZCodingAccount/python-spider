# 数据来源：高考网：https://college.gaokao.com/。中国教育在线：https://www.eol.cn/e_html/gk/fsx/index.shtml
# 看着ui，感觉还是第二个靠谱一点，应该是官方的吧？我们也不需要近20年的数据，参考价值也不大
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

headers = {
    'authority': 'www.eol.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

response = requests.get('https://www.eol.cn/e_html/gk/fsx/index.shtml', headers=headers)

html = response.content.decode("utf-8")
# print(html)
doc1 = pq(html)
# 首先明确我们需要什么？要采集的数据有：每个省份的名称，年份，每个批次招收的最低分数线
# 提取数据
province_items = doc1(".fsshowli.hascore")  # 提取出所有的小方格，所有的省份
# print(province_items)
data = []  # 存储所有省份的数据

for city_index, province in enumerate(province_items.items()):
    province_data = {}
    # 提取每个省份的数据
    province_data['city'] = province('.topline .city').text()  # 提取省份名称
    # 这里得提取每个年份的数据，year:2023.score_line:['批次，分数线','普通本科批，463','艺术类本科，点击查看']
    # 其实筛选一下，本科一批，本科二批就可以了，但是爬取完后面再数据处理也可以，更多的扩展空间

    years = province('.sline .year').text().split(' ')  # 提取年份名称
    score_data = []  # 存储每年数据的数组
    for year_index, line in enumerate(province('.tline div').items()):
        # [print(tr.text().strip().replace('\n','')) for tr in line('tr').items()]
        # print(line.text())
        # 存储每一行的数据
        score_line = [tr.text() for tr in line('tr').items()]
        # 把这一行数据映射到当年
        score_data.append({years[year_index]: score_line})
    province_data['data'] = score_data  # 把数据复制给对象
    print(province_data)
    data.append(province_data)
print(data)
# 由于刚才用到了mysql数据库，这个数据结构也不是很规则，这次我们练习一下mongodb数据库
# 创建连接
conn = MongoClient(host="localhost", port=27017)
collection = conn.test.scoreline
# 存储数据，没错，就一行命令
collection.insert_many(data)
