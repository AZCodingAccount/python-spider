import json
import random
import re
import threading
import time
from requests.adapters import HTTPAdapter
import requests
from urllib3 import Retry

from 请求头加密 import convert_md5, get_secret_key
from cookie加密 import gen_b_lsid, gen_uuid
from 代理 import get_tunnel_proxies, get_proxy_dict

start_time = time.time()
# 全局计数器和线程锁
count_lock = threading.Lock()
play_count = 0
time_limit = 60 * 10  # 运行时间限制，10分钟


# 获取查询参数
def get_query_params(session, click_url):
    # 获取w_aid
    res = session.get(url=click_url, timeout=5)
    # 使用正则提取，直接把这个对象都给提取出来，后面还要拿东西。
    data_dict = re.search(r'window\.__INITIAL_STATE__=(.+);\(function\(', res.text).group(1)
    # 获取aid
    w_aid = json.loads(data_dict)['aid']
    # 获取播放量并打印一下，日志
    print(
        f"当前视频：{json.loads(data_dict)['videoData']['title']}，实际的播放量为：{json.loads(data_dict)['videoData']['stat']['view']}")
    # 模拟w_ftime，w_stime
    w_ftime = int(time.time()) + random.randint(1, 3)
    w_stime = int(time.time())
    # 模拟wts
    wts = int(time.time()) + random.randint(2, 6)
    # 获取web_location
    res1 = session.get("https://s1.hdslb.com/bfs/static/player/main/core.d98a5476.js", timeout=5)  # 获取js文件
    web_location = re.findall(r"function p\(e,t,r\){if\(e.web_location=(.*?),t", res1.text)  # 正则提取
    # 获取w_rid
    res2 = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=5)  # 获取img_url，sub_url
    secret_key = get_secret_key(res2)  # 将img_url和sub_url使用py代码复现加密逻辑
    str = f'w_aid={w_aid}&w_ftime={w_ftime}&w_part=1&w_stime={w_stime}&w_type=3&web_location={web_location}&wts={wts}' + secret_key
    # 获取到w_rid
    w_rid = convert_md5(str)
    params = {
        "w_aid": w_aid,
        "w_part": 1,
        "w_ftime": w_ftime,
        "w_stime": w_stime,
        "w_type": 3,
        "web_location": web_location,
        "w_rid": w_rid,
        "wts": wts
    }
    return params, json.loads(data_dict), res.text, res.cookies


# 获取请求体相关参数
def get_body_data(params, data_dict, text):
    # 获取cid和spm_id
    cid = data_dict['videoData']['cid']
    spm_id = data_dict['videoData']['embedPlayer']['stats']['spmId']

    # 获取session
    session_data_dict = re.search(r'window\.__playinfo__=(.*?)</script>', text, re.DOTALL).group(1)

    session = json.loads(session_data_dict)['session']
    data = {
        "aid": params.get('w_aid'),
        'cid': cid,
        'part': 1,
        'lv': 0,
        'ftime': params.get('w_ftime'),
        'stime': params.get('w_stime'),
        'type': params['w_type'],
        'sub_type': 0,
        'refer_url': "",
        'outer': 0,
        'spmid': spm_id,
        'from_spmid': "",
        'session': session,
        'csrf': ''
    }
    return data


# 获取cookie
def get_cookie(first_cookies, params, data, session):
    # buvid3和b_nut
    buvid3 = first_cookies.get('buvid3')
    b_nut = first_cookies.get('b_nut')

    # b_lsid和_uuid
    b_lsid = gen_b_lsid()
    _uuid = gen_uuid()
    # 获取sid
    params = {"aid": params['w_aid'],
              'cid': data['cid'],
              'web_location': params['web_location'],
              'w_rid': params['w_rid'],
              'wts': int(time.time())
              }
    res = session.get("https://api.bilibili.com/x/player/wbi/v2", params=params, timeout=5)  # 向这个请求发，获取cookie里面的sid
    sid = res.cookies.get('sid')

    # 获取buvid4和buvid_fp
    res = session.get("https://api.bilibili.com/x/frontend/finger/spi", timeout=5)
    buvid4 = res.json()['data']['b_4']
    # f700b2fa0217e916d769bf691fb41f92，浏览器的型号，所以buvid_fp这个是固定的
    cookies = {
        'buvid3': buvid3,
        'b_nut': b_nut,
        'CURRENT_FNVAL': '4048',
        'b_lsid': b_lsid,
        '_uuid': _uuid,
        'sid': sid,
        'buvid_fp': 'f700b2fa0217e916d769bf691fb41f92',
        'buvid4': buvid4
    }
    return cookies


# 获取当前ip
def get_current_ip(session):
    try:
        response = session.get("https://httpbin.org/ip", timeout=5)
        ip = response.json()["origin"]
        return ip
    except requests.RequestException as e:
        print(f"Error getting IP: {e}")
        return None


# 真正干活的函数
def increase_video_play_count(session, headers, click_url):
    global play_count
    try:
        params, data_dict, text, first_cookies = get_query_params(session, click_url)
        data = get_body_data(params, data_dict, text)
        cookies = get_cookie(first_cookies, params, data, session)
        request_url = "https://api.bilibili.com/x/click-interface/click/web/h5"
        response = session.post(url=request_url, params=params, data=data, cookies=cookies, timeout=5)
        ip = get_current_ip(session)
        print(f"当前请求的ip是：{ip}")
        # 更新计数器
        with count_lock:
            play_count += 1
            print(f"当前播放量理论上刷了: {play_count}个")
    except Exception as e:
        print(f"发生错误：{e}")


# 创建一个带有重试机制的session
def create_session_with_retry():
    session = requests.Session()

    # 定义重试策略
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],  # 重试的状态码
    )

    # 创建带有重试策略的 HTTPAdapter
    adapter = HTTPAdapter(max_retries=retries)

    # 将该适配器挂载到 HTTP 和 HTTPS
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


# 线程工作函数
def thread_worker(click_url, headers):
    # proxies = get_tunnel_proxies()
    while True:
        session = create_session_with_retry()
        proxies = get_proxy_dict()  # 按量计费的代理
        session.proxies.update(proxies)  # 把代理整上去
        session.headers.update(headers)  # 公共请求头
        increase_video_play_count(session, headers, click_url)
        # 时间达到限制时退出
        if time.time() - start_time > time_limit:
            break


# 主程序
if __name__ == '__main__':
    click_url = input("输入要刷的视频url:")
    thread_count = input("输入并发线程数:")
    # click_url = "https://www.bilibili.com/video/BV1Ce411q786/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Referer': click_url,
        'origin': 'https://www.bilibili.com'
    }

    threads = []
    for i in range(int(thread_count)):  # 10个线程
        t = threading.Thread(target=thread_worker, args=(click_url, headers))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end_time = int(time.time())

    print(f"播放量刷取完毕，一共刷取{play_count}个播放量，耗时{end_time - start_time}秒")
