import requests
from lxml import etree

""" 
    现在考虑这样一个需求:小张想在猪八戒平台上面找一个logo设计的商家，但是它需要多种维度进行分析，
    销量，价格，好评率，主营业务和商家名称这些信息都是很重要的参考指标，现在抓取前6条数据存储到猪八戒logo设计商家.csv这个文件中以便进一步数据分析
    因为只能抓取6条，好像是ajax动态加载，需要用后面的库才能实现模拟请求
"""

url = "https://www.zbj.com/logosjzbj/f.html?r=2"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
# 初始化
html_zbj = etree.HTML(response.text)
# 获取到所有div对象（一个div对应一个商家信息）
divs = html_zbj.xpath("//div[@class='search-result-list-service']/div")
i = 1
total_html = ''
for div in divs:
    if i > 6:
        break
    price = div.xpath("./div/div/div[1]/span[1]/text()")[0]
    sell_count = "".join(div.xpath("./div/div[@class='bot-content']/div[@class='descprit-box']/div[2]//text()"))
    top_rate_count = "".join(div.xpath("./div/div[@class='bot-content']/div[@class='descprit-box']/div[3]//text()"))
    main_business = div.xpath("./div/div[@class='bot-content']/div[@class='name-pic-box']//text()")[0]
    shop_name = div.xpath("./div//div[@class='shop-detail']//text()")[0]
    # 把这些数据写入到csv文件中
    with open('猪八戒logo设计商家信息统计.csv', 'a', encoding="utf-8") as f:
        if i == 1:
            with open('猪八戒logo设计商家信息统计.csv', 'w'):
                pass
            f.write("商家名,主营业务,价格,销售量,好评数\n")
        f.write(f"{shop_name},{main_business},{price},{sell_count},{top_rate_count}\n")
    i += 1
print("写入完成")
# 数据已经封装好了，美中不足的就是数据有点少，后面学了一些高级的请求数据的框架就可以解决这个问题了
