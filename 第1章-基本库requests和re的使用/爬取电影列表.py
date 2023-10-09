# 导入模块
import requests
import re
# 这里简单的解析打印了一下相关内容，后续没有封装，主要正则太麻烦了，后面使用一些解析库就行了

# 定义函数封装爬取的方法
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    # 这里使用try-except捕捉一下异常
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 定义接收爬取回来的数据的方法
def get_data():
    # 抓取前10页数据
    for page in range(1, 10):
        url = f'https://ssr1.scrape.center/page/{page}'
        one_page = get_one_page(url)
        parse_one_page(one_page)


total_title_list = []

# 利用正则解析爬取回来的字符串
def parse_one_page(html):
    title_pattern = re.compile("<h2.*?m-b-sm\">(.*?)</h2>")
    # 这里之所以会匹配到\n和空字符串，原因在于.*?可能会匹配空和\n，使用strip函数去掉即可
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
    # search为第一次查找，findall查找全部
    scores = re.findall(score_pattern, html)
    for score in scores:
        score = score.strip()
        print(f"score为：{score}")
    time_pattern = re.compile(r'\d{4}-\d{2}-\d{2}\s?上映')
    times = re.findall(time_pattern, html)
    for time in times:
        print(f"time为：{time}")
    title = re.findall(title_pattern, html)
    total_title_list.append(title)


get_data()
# 这是对标题的处理
i = 0
for idx1, title_list in enumerate(total_title_list):
    for idx2, title in enumerate(title_list):
        prev = str(i) + ':'
        total_title_list[idx1][idx2] = prev + title
        i = i + 1

result1 = ''.join([str(item) for item in total_title_list])
result = result1.replace(', ', '\n').replace('\'', '').replace('[', '').replace(']', '')
print(result)
