import json
import random
import re
import time
from requests.adapters import HTTPAdapter
import requests
from urllib3 import Retry

from 请求头加密 import convert_md5, get_secret_key
from cookie加密 import gen_b_lsid, gen_uuid
from 代理 import get_tunnel_proxies, get_proxy_dict


# 获取查询参数
def get_query_params():
    # 获取w_aid
    res = session.get(url=click_url)
    # 使用正则提取，直接把这个对象都给提取出来，后面还要拿东西。
    data_dict = re.search(r'window\.__INITIAL_STATE__=(.+);\(function\(', res.text).group(1)
    # 获取aid
    w_aid = json.loads(data_dict)['aid']
    # 获取播放量并打印一下，日志
    print(
        f"当前视频{json.loads(data_dict)['videoData']['title']}：实际的播放量为{json.loads(data_dict)['videoData']['stat']['view']}")
    # 模拟w_ftime，w_stime
    w_ftime = int(time.time()) + random.randint(1, 3)
    w_stime = int(time.time())
    # 模拟wts
    wts = int(time.time()) + random.randint(2, 6)
    # 获取web_location
    res1 = session.get("https://s1.hdslb.com/bfs/static/player/main/core.d98a5476.js")  # 获取js文件
    web_location = re.findall(r"function p\(e,t,r\){if\(e.web_location=(.*?),t", res1.text)  # 正则提取
    # 获取w_rid
    res2 = session.get("https://api.bilibili.com/x/web-interface/nav", headers=headers)  # 获取img_url，sub_url
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
def get_cookie(first_cookies, params, data):
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
    res = session.get("https://api.bilibili.com/x/player/wbi/v2", params=params)  # 向这个请求发，获取cookie里面的sid
    sid = res.cookies.get('sid')

    # 获取buvid4和buvid_fp
    res = session.get("https://api.bilibili.com/x/frontend/finger/spi", headers=headers)
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


# 真正干活的函数
def increase_video_play_count():
    # 刷播放量url
    request_url = "https://api.bilibili.com/x/click-interface/click/web/h5"
    # 获取查询参数
    params, data_dict, text, first_cookies = get_query_params()
    # 获取请求体
    data = get_body_data(params, data_dict, text)
    # 获取cookie
    cookies = get_cookie(first_cookies, params, data)

    # 直接请求
    res = session.post(url=request_url, params=params, data=data, cookies=cookies)


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


# main入口
if __name__ == '__main__':
    click_url = "https://www.bilibili.com/video/BV1ju4y1W78T/"  # 要
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    start_time = int(time.time())
    # 获取代理
    # proxies = get_tunnel_proxies()
    count = 2000
    for i in range(0, count):
        # 获取session
        session = create_session_with_retry()
        proxies = get_proxy_dict()  # 按量计费的代理
        # 给session设置代理
        session.proxies.update(proxies)
        # 给session统一设置请求头
        session.headers.update(headers)
        # 开始刷播放量
        increase_video_play_count()
        print(f"理论上刷了{i + 1}个播放量")
        print("----------------------------------------")
    end_time = int(time.time())

    print(f"播放量刷取完毕，一共刷取{count}个播放量，耗时{end_time - start_time}秒")

    # test1()
