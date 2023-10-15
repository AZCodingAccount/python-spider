import asyncio
import os.path
import re
from urllib.parse import urljoin
import aiohttp
import aiofiles
import time
import requests
from aiohttp import TCPConnector
from pyquery import PyQuery as pq
from lxml import etree

"""
        下面这个案例实现这个功能，爬取美剧天堂的视频，去网站查看有没有这个视频的源，点到集数这个页面复制上面的url，输入到程序中，
    程序会打印出所有集数。指定集数，会爬取指定集数的视频。并把视频存储为一个mp4文件，命名为视频名称-集数
    
    思路：
    1：首先找到美剧天堂的域名，输入url后，程序向这个网页发送请求获取到这个网页的数据。找到集数并打印在控制台。
    2：输入集数，程序再发一次请求，返回的是播放页的源码。然而我需要的是m3u8文件，播放页源码里面并不存在
    分析网络请求和源码可以发现，这个网站是向这个https://php.playerla.com/mjplay这个uri发送查询请求，携带一个查询参数id
    （这个id怎么获取呢，在每个播放页的源码里面会有所有相关集的id，利用正则匹配即可。）
    3：请求这个拼接一下这个url，发送第三次请求，获取与播放器相关的html，使用正则匹配到url地址。
    4：根据上述正则匹配的结果发送第四次请求，拿到这个文件了以后，拼接上前缀和里面的资源。就可以实现一个一个下载了。
    （这个前缀查看网络请求跟请求m3u8的url差不多，字符串切割一下存成baseurl）
    5：程序使用协程下载再发请求，这次下载的就是.ts文件。最后下载完毕使用merge函数合并，执行ffmpeg的一个命令即可
"""
# 定义全局变量,title为集数名，href为集数url，m3u8_url为请求m3u8文件的url，baseurl为请求，video_name为影片名，episode_n为第几集
title = href = m3u8_url = baseurl = video_name = episode_n = None


# 通过用户输入的url来查找当前美剧的名称和对应的episode
def get_section(url):
    global title, href
    page_code = requests.get(url, headers=headers)
    lis = pq(page_code.text)(".z-pannel_bd ul li a").items()
    name = pq(page_code.text)('h1').text()
    res = []
    # 得到里面的title和href属性值
    for li in lis:
        title = li.attr("title")
        href = "https://www.mjtt5.tv" + li.attr('href')
        if title and title.startswith('第') and title.endswith('集'):
            res.append({'title': title, 'href': href})
    res.append({'name': name})
    return res


# 从选集页面源码里面找到播放器相关的地址，供得到m3u8url使用
def find_m3u8_url(href):
    res = requests.get(href, headers=headers)
    ids = etree.HTML(res.text).xpath('/html/body/div[2]/div/div[1]/div[1]/script[1]/text()')
    id = str(ids[0])
    re_str = "\\\\/".join(href.rsplit("/", 3)[-3:])
    pattern = r'"(\w+?=?)","\\/{}"'.format(re_str)
    query_id = re.search(pattern, id).group(1)
    return f"https://php.playerla.com/mjplay/?id={query_id}"


# 通过上一个函数得到的播放器地址请求得到m3u8的url
def get_m3u8_url(m3u8_url):
    res = requests.get(m3u8_url, headers=headers)
    # 编写正则找到m3u8文件的url
    pattern = r'var playconfig = {\s*"url":\s*"([^"]+)"'
    m3u8_url = re.search(pattern, res.text).group(1)
    return m3u8_url


# 交互页面
def say_aloha():
    global m3u8_url, baseurl, video_name, episode_n
    print(
        "-----------------------------------------------你好^_^，欢迎使用----------------------------------------------")
    url = input("请输入需要下载的电影的url").strip()
    # 列表里面包字典
    section_list = get_section(url)
    section = int(input(f'美剧{section_list[-1].get("name")}共有{len(section_list)}集，请输入你需要下载第几集'))
    video_name = section_list[-1].get("name")
    episode_n = section
    # 得到的这个url原来是在线播放器的地址
    m3u8_url_page = find_m3u8_url(section_list[len(section_list) - section].get('href'))
    m3u8_url = get_m3u8_url(m3u8_url_page)
    # 得到这个url就可以传递给真正干活的协程那些方法干活去了
    baseurl = m3u8_url.rsplit("/", 1)[0] + "/"


# 创建m3u8文件，通过上面得到的m3u8的url请求，把m3u8文件存储到本地
async def find_m3u8(url):
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url, headers=headers) as res:
            data = await res.text(encoding="UTF-8")
            if not os.path.exists("./ts"):
                os.mkdir("ts")
            async with aiofiles.open('./ts/index.m3u8', mode='w', encoding='UTF-8') as f:
                await f.write(data)


# 下载一个ts文件的方法，加上try-except和while循环确保全部下完，使用协程和信号量
async def download_one(url, sem, i):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        "authority": "https://cdn8.tvtvgood.com"
    }
    async with sem:
        while True:
            try:
                async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
                    async with session.get(url, headers=headers, timeout=60) as res:
                        print("第" + str(i) + "个" + url + "爬取中~状态码为：", res.status)
                        data = await res.read()
                        async with aiofiles.open(f'./ts/{i}.ts', mode='wb') as f:
                            await f.write(data)
                            break
            except Exception as e:
                print(f"请求出错，原因是：{e}，正在重新爬取中......")


# 构建一个拼接电影文件的m3u8文件，供ffmpeg使用
def create_join_ts_file():
    i = 0
    with open('./ts/index.m3u8', mode='r') as f:
        lines = f.readlines()
        with open('./ts/index.m3u8', mode='w') as f:
            for line in lines:
                if line.startswith('#'):
                    f.write(line)
                else:
                    f.write(f'{i}.ts\n')
                    i += 1


# 下载所有的ts文件，创建一个任务列表，调用download_one方法干活
async def download_all():
    task_list = []
    with open('./ts/index.m3u8', mode='r', encoding='UTF-8') as f:
        line = "line"
        i = 0
        # 开始下载视频，首先创建一个信号量，控制并发协程数
        sem = asyncio.Semaphore(10)
        while line:
            line = f.readline()
            if line.startswith('#'):
                continue
            url = urljoin(baseurl, line.strip())
            if url == baseurl:
                continue
            task = asyncio.create_task(download_one(url, sem, i))
            task_list.append(task)
            i += 1
        await asyncio.wait(task_list)
        # 下完以后再合并
        create_join_ts_file()
        merge()


# 合并所有ts文件，并且把剩下的ts文件给删了
def merge():
    os.chdir('./ts')
    cmd = f'ffmpeg -i index.m3u8 -c copy {video_name}-{episode_n}.mp4'
    os.system(cmd)


def delete():
    os.chdir('./ts')
    # 删除m3u8和ts文件
    for file in os.listdir('./'):
        if file.endswith('.ts') and file.endswith('.m3u8'):
            os.remove(file)



# 程序主入口
async def main():
    # 进行爬虫数据收集和预先数据处理
    say_aloha()
    begin_time = time.time()
    print("开始下载视频......")
    # 得到m3u8文件
    task1 = asyncio.create_task(find_m3u8(m3u8_url))
    await task1
    # 开始下载
    task2 = asyncio.create_task(download_all())
    await task2
    end_time = time.time()
    print(f"下载视频完成，共用时{end_time - begin_time}秒")


# 文件的入口，启动程序主入口那个异步方法
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    # asyncio.run(main())
    delete()
