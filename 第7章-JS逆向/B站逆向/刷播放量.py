import math
import random
import time
import uuid
import requests
import re
import json

"""
-.js -.css -.png -.svg -.html -data: 首先在过滤器里面把静态资源相关的先过滤了
找到请求URL为：https://api.bilibili.com/x/click-interface/click/now。但是这个是GET，一看这个不用

https://api.bilibili.com/x/click-interface/click/web/h5，最后找到这个
观察url没有需要过逆向的，接下来就是看这些参数，哪些是需要逆向的。（一般加上id、auth这种的）

查询字符串参数：
    w_aid: 325318514        // 可能需要逆向
    w_part: 1               // 一般不需逆向
    w_ftime: 1703944675     // 时间戳，ftime是first_time，第一次播放
    w_stime: 1703944674     // 时间戳，stime是start_time，这个应该是进来的时间，因为比上面那个小
    w_type: 3               // 这个应该是类型，一般不需逆向
    web_location: 1315873   // 这个location，不知道是啥，10%的可能性需要逆向
    w_rid: 156c3c9ccf38bbe3e32c2a8481540e07 // 这个需要逆向
    wts: 1703944676     // 这个也是时间戳，不知道是啥
请求体：
    aid: 325318514      // 跟上面那个aid一样
    cid: 1381936481     // 应该需要逆向
    part: 1             // 跟上面part一样
    lv: 0               // 一般不需逆向
    ftime: 1703944675   // 跟上面查询参数一样
    stime: 1703944674   // 跟上面查询参数一样
    type: 3             // 跟上面类型一样
    sub_type: 0         // 发布类型，应该是视频投稿时候的类型
    refer_url: 
    outer: 0
    spmid: 333.788.0.0  // 这个不知道是啥，应该需要逆向
    from_spmid: 
    session: 43b386d7ec6e006b96315d0a242ae6de   // 用户会话标识，必须逆向
    csrf: 

// 下面这些cookie只有两种情况，一种是前面请求返回回来的，一种是前端生成的。一般不会在这里搞一些特别复杂的加密。
Cookie:
    buvid3=961F977A-3B6C-A0B4-0084-31ECF47E0EBD72322infoc; 
    b_nut=1703944672; CURRENT_FNVAL=4048; 
    b_lsid=DC319B4B_18CBB045E54; 
    _uuid=107BBB10BC-A2DF-D12E-5B44-10D35E10A7D3A774908infoc;
    sid=8batyilc; 
    buvid4=F20CC40F-8052-82EB-7114-6644F359C14273809-023123013-r%2Ft%2FxrhceKtUMRV2iYDcYg%3D%3D;
    buvid_fp=f700b2fa0217e916d769bf691fb41f92
"""


def gen_uuid():
    uuid_sec = str(uuid.uuid4())
    time_sec = str(int(time.time() * 1000 % 1e5))
    time_sec = time_sec.rjust(5, "0")

    return "{}{}infoc".format(uuid_sec, time_sec)


def gen_b_lsid():
    data = ""
    for i in range(8):
        v1 = math.ceil(16 * random.uniform(0, 1))
        v2 = hex(v1)[2:].upper()
        data += v2
    result = data.rjust(8, "0")

    e = int(time.time() * 1000)
    t = hex(e)[2:].upper()

    b_lsid = "{}_{}".format(result, t)
    return b_lsid


def play(video_url, proxies):
    bvid = video_url.rsplit("/")[-1]
    session = requests.Session()
    session.proxies = proxies
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    })

    res = session.get(video_url)
    data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', res.text)
    data_dict = json.loads(data_list[0])
    aid = data_dict['aid']
    cid = data_dict['videoData']['cid']

    _uuid = gen_uuid()
    session.cookies.set('_uuid', _uuid)

    b_lsid = gen_b_lsid()
    session.cookies.set('b_lsid', b_lsid)

    session.cookies.set("CURRENT_FNVAL", "4048")

    res = session.get("https://api.bilibili.com/x/frontend/finger/spi")
    buvid4 = res.json()['data']['b_4']
    session.cookies.set("buvid4", buvid4)
    session.cookies.set("CURRENT_BLACKGAP", "0")
    session.cookies.set("blackside_state", "0")

    ctime = int(time.time())
    res = session.post(
        url="https://api.bilibili.com/x/click-interface/click/web/h5",
        data={
            "aid": aid,
            "cid": cid,
            "bvid": bvid,
            "part": "1",
            "mid": "0",
            "lv": "0",
            "ftime": ctime - random.randint(100, 500),  # 浏览器首次打开时间
            "stime": ctime,
            "jsonp": "jsonp",
            "type": "3",
            "sub_type": "0",
            "from_spmid": "",
            "auto_continued_play": "0",
            "refer_url": "",
            "bsource": "",
            "spmid": ""
        }
    )

    # print(res.text)


def get_video_view_count(video_url, proxies):
    session = requests.Session()
    bvid = video_url.rsplit('/')[-1]
    res = session.get(
        url="https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp".format(bvid),
        proxies=proxies
    )

    cid = res.json()['data'][0]['cid']

    res = session.get(
        url="https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}".format(cid, bvid),
        proxies=proxies
    )
    res_json = res.json()
    view_count = res_json['data']['stat']['view']
    duration = res_json['data']['duration']
    print("\n视频 {}，平台播放量为：{}".format(bvid, view_count))
    session.close()


def get_proxy_dict():
    key = "6JD3LFEN"  # 用户key
    passwd = "D3BDB526FEE2"  # 用户密码

    res = requests.get(
        url="https://share.proxy.qg.net/get?key=6JD3LFEN&num=1&area=&isp=&format=json&seq=&distinct=false&pool=1"
    )
    host = res.json()['data'][0]['server']  # 121.29.81.215:52001

    # 账密模式
    proxy = 'http://{}:{}@{}'.format(key, passwd, host)

    return {"http": proxy, "https": proxy}


def run():
    video_url = "https://www.bilibili.com/video/BV1aw41157V3"

    view_count = 0
    while True:
        try:
            # 获取代理
            proxies = get_proxy_dict()
            # 获取当前视频播放量
            get_video_view_count(video_url, proxies)
            # 开始刷播放量
            play(video_url, proxies)
            view_count += 1
            print("理论刷的播放量：", view_count)
        except Exception as e:
            pass


if __name__ == '__main__':
    run()
