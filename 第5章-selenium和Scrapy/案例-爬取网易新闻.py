import time
import csv

import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

def selenium_crawl():
    chrome = Chrome()
    chrome.get("https://news.163.com/")
    chrome.maximize_window()
    load_more_tips = False
    count = 1
    # 模拟页面滑动，页面数据是动态加载的，滑动5次，（这样容易被检测）
    while count <= 6:
        print(f"第{count}次滑动")
        count += 1
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 点击加载更多
        button = chrome.find_element(By.XPATH,
                                     '//*[@id="index2016_wrap"]/div[3]/div[2]/div[3]/div[2]/div[5]/div/a[3]')
        # button.click()
        chrome.execute_script('arguments[0].click();', button)
        time.sleep(4)
    # 错误示范，没有考虑到一个文章有多个img
    # html = chrome.page_source
    # print(html)
    # # 从页面上提取数据
    # titles = chrome.find_elements(By.XPATH,
    #                               '//div[contains(@class,"ndi_main")]/div[contains(@class,"data_row")]//div[contains(@class,"news_title")]/h3//a')
    # # 这里的图片可能有多个
    # image_hrefs = chrome.find_elements(By.XPATH, "//div[contains(@class,'ndi_main')]/div[contains(@class,'data_row')]//img")
    # article_hrefs = chrome.find_elements(By.XPATH,
    #                                      "//div[contains(@class,'ndi_main')]/div[contains(@class,'data_row')]//div[contains(@class,'news_title')]/h3//a")
    # 遍历取出每一项，并把他们添加到列表中，列表中
    # articles = [{'title': title, 'url': url, 'img_url': img_url} for title, url, img_url in
    #             zip(titles, article_hrefs, image_hrefs)]
    # for index, title in enumerate(titles):
    #     print(index, title.text)
    #
    # for index, title in enumerate(image_hrefs):
    #     print(index, title.get_attribute("src"))
    # for index, title in enumerate(article_hrefs):
    #     print(index, title.get_attribute("href"))

    article_elements = chrome.find_elements(By.XPATH,
                                            '//div[contains(@class,"ndi_main")]/div[contains(@class,"data_row")]')  # 定位所有文章
    # 遍历所有文章取出每一个文章，并对这些文章进行提取
    articles = []
    for article_element in article_elements:
        # 对每篇文章，提取标题、URL等信息
        title = article_element.find_element(By.XPATH, ".//h3/a").text
        url = article_element.find_element(By.XPATH, ".//h3/a").get_attribute('href')

        # 提取当前文章内的所有图片链接
        img_urls = [img.get_attribute('src') for img in article_element.find_elements(By.XPATH, ".//img")]

        # 将信息添加到列表中
        articles.append({'title': title, 'url': url, 'img_urls': img_urls})

    # 打印共有多少新闻和新闻详情
    print(len(articles))
    for article in articles:
        print(article)

    # 接下来存储到数据库或者csv文件中
    with open('网易新闻数据.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'url', 'img_urls'])
        # 写入表头
        writer.writeheader()
        # 写入数据行
        for row in articles:
            writer.writerow(row)


def save_article(url):
    # 对于新闻，可以把所有数据都爬下来存储到一个html文件里面
    return requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    })


if __name__ == '__main__':
    # selenium爬取网易新闻信息
    selenium_crawl()
    # 演示一下怎么据为己有
    res = save_article("https://www.163.com/dy/article/IJG52MJK051282JL.html")
    with open("article.html", mode="w", encoding="utf-8") as f:
        f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')  # 设置一下编码
        f.write(res.text)
