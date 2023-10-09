"""
        背景1：  当我们浏览到了一个非常有吸引力的网站——诗词名句网，作为一个诗迷，我们想把所有的诗据为己有。而网站没有提供下载功能，这可咋办呢？
        需求：诗人选择：1：输出网站默认推荐的前100位诗人，2：自定义输入作者，如果不存在这个作者，重新输入
                     3：选择下载诗的数量：输入参数，下载即可（会输出总数量，不能大于总数量）
                     4：存储：默认存储到当前目录下面的poems文件夹，一首诗一个txt文件
        背景2：  这个时候我们突然看到了古籍，它对我们的吸引力远大于古诗，我们想把所有古籍据为己有，这个时候咋办呢？
        实现2：  1：请求所有的古籍名，存到一个字典中，进行对比，并输出排名前10位的古籍。
                2：输入古籍名称和下载模式，开始下载，可以选择下载到一个txt文件或者分开章节下载
                3：存储到./books这个文件夹下
"""
import os.path
import time
import requests
from pyquery import PyQuery as pq


# 定义交互的方法
def say_aloha(books_name):
    print(
        "-----------------------------------------------你好^_^，欢迎使用----------------------------------------------")
    print(f"您查询到的前10个古籍为：{' '.join(list(books_name.keys())[0:10])}")
    book_name = input("请输入您想下载的古籍：（输入古籍名即可，不需书名号）")
    mode = int(input("请输入您选择的下载的存储模式：（1：所有章节存储到一个txt文件中。2：章节分开存储。）"))
    user_choice = {'book_name': book_name, 'mode': mode}
    return user_choice


# 定义获取html字符串的方法
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response.content.decode()


# 定义获取所有古籍的方法
def get_books_name():
    cate_html = get_html("https://www.shicimingju.com/book/")
    # 开始提取所有书名，并把书名和url映射存储到一个字典中返回回去
    cate_doc = pq(cate_html)
    a_s = cate_doc('#main_left ul li a').items()
    books_dict = {}
    for a in a_s:
        book_name = a.text()
        href = domain_name + a.attr('href')
        books_dict[book_name] = href
    return books_dict


# 开始下载书籍每一章的数据
def get_section(url):
    # 获取章节页面
    cate_html = get_html(url)
    # 解析章节名称和url
    sections = pq(cate_html)('#main_left ul li a').items()
    sections_dict = {}
    for section in sections:
        section_name = section.text()
        section_href = domain_name + section.attr('href')
        sections_dict[section_name] = section_href
    return sections_dict


def save_section_content(book_name, section_name, url, mode):
    # 睡眠0.3秒再访问
    time.sleep(0.3)
    if mode == 2:
        content_html = get_html(url)
        section_content = pq(content_html)(".chapter_content").text()
        section_content.replace('\n', '\n\n        ')
        if not (content_html or section_content):
            return False
        # 写入文件
        if not os.path.exists("./books"):
            os.mkdir('./books')
        with open(f'./books/{book_name}-{section_name}.txt', 'w', encoding='utf-8') as f:
            f.write(section_content)
        return True
    else:
        # 直接创建一个文件，追加写入，章节名写一个换个行
        content_html = get_html(url)
        section_content = pq(content_html)(".chapter_content").text()
        section_content.replace('\n', '\n\n')
        if not (content_html or section_content):
            return False
        # 写入文件
        if not os.path.exists("./books"):
            os.mkdir('./books')
        with open(f'./books/{book_name}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n\n        {section_name}\n\n\n')
            f.write(section_content)
        return True


# 控制下载各个章节的方法
def save_sections_text(sections_dict, mode, book_name):
    # 这里就直接遍历了，判断用户选择的模式，看看是写到一个还是多个文件中
    flag = True
    for (section_name, url) in sections_dict.items():
        flag = save_section_content(book_name, section_name, url, mode)
        print("章节" + section_name + "下载完成~")
        if not flag:
            flag = False

    return flag


# 下载古籍的主方法
def save_book(books_name, user_choice):
    # 匹配书籍url
    url = books_name.get('《' + user_choice.get('book_name') + '》')
    if not url:
        return False
    # 获取章节url和章节名
    sections_dict = get_section(url)
    # 存储章节文本到文件中
    flag = save_sections_text(sections_dict, user_choice.get('mode'), user_choice.get('book_name'))
    return flag


# 主函数
if __name__ == '__main__':
    try:
        domain_name = 'https://www.shicimingju.com'
        # 获取网站所能提供的所有方法，并存储到一个字典里面
        books_name = get_books_name()
        # 获取到下载的名称和模式
        user_choice = say_aloha(books_name)
        # 开始下载书籍，下载成功返回一个标志
        flag = save_book(books_name, user_choice)
        print(f"开始下载书籍{user_choice.get('book_name')}~")
        if flag:
            print(f"书籍{user_choice.get('book_name')}下载成功~")
        else:
            print(f"书籍{user_choice.get('book_name')}下载失败~")
    except:
        print("未知异常~")
