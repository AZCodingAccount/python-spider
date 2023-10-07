# 爬取优美图库的图片，因为之前那个菜市场直接请求的接口，没有练习到BS4。BS4这个库常用的也就是find和find_all，select也可以用吧，节点啥的感觉用不到
# 需求：爬取可爱图片的10张图片，存储到当前目录下面的images文件夹下面，文件命名要与网站一致
# 导入模块
import time

import requests
from bs4 import BeautifulSoup

# 请求数据
response = requests.get("https://www.umei.cc/weimeitupian/keaitupian/")
response.encoding = "utf-8"
# 如果只是爬取图片的话直接找img里面的data-original属性就可以了，但是我还想要他的图片名，还需要找title那个div标签
# 提取所有a里面的href属性，初始化
html = BeautifulSoup(response.text, 'html.parser')
divs = html.find_all('div', attrs={'class': 'item masonry_brick'})
# 定义一个计数器，读取到10个就停
count = 0
for div in divs:
    time.sleep(0.2)
    if count > 10:
        break
    image_src = div.find('img').get('data-original')
    image_name = div.find('img').get('alt').split(' ')[0]
    # 发送一次请求获取图片的字节数据
    image = requests.get(image_src).content
    # 把图片保存到文件夹里面
    with open(f"./images/{image_name}.jpg", 'wb') as f:
        f.write(image)
    print(f"{image_name}.jpg图片写入成功")
    count += 1
print("写入完成")
