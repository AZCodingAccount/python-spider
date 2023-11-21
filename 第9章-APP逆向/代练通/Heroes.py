import requests
from pyquery import PyQuery as pq
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 这个类是获取王者荣耀英雄列表的
heroes = []


def get_heros_order():
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument('--disable-gpu')
    opt.add_argument("--window-size=4000,1600")  # 设置窗口大小

    driver = Chrome(options=opt)
    driver.get("https://pvp.qq.com/web201605/herolist.shtml")
    driver.implicitly_wait(10)
    lis = driver.find_elements(By.CSS_SELECTOR, ".herolist li")
    for li in lis:
        # 把数据存储到列表中
        heroes.append(li.text)


get_heros_order()
