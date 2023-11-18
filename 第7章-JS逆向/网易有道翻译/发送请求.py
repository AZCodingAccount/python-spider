import requests
import time
from hashlib import md5

"""
        逆向请求参数的思路是首先抓包，看到请求体里面有sign，时间戳，显然是需要逆向的。这时搜一下webtranslate（或者搜mysticTime等），然后找到加密入口
    发现是md5加密，传过去的时候有一个"fsdsogkndfokasodnaso"字符串，猜测可能是盐，再发一次请求，这个字符串不变，肯定了这个猜想
    （注意，那个js文件里面没有这个参数赋值的操作，应该是暴露出去，另外的文件调用传参的）。
    接下来找到加密的函数，标准md5加密，在py里面复现就可以了，只有e（也就是time在变）,另外需要注意的是传1,2,这种的时候一般传数字，有时候传字符串也行（看服务端）
"""

url = "https://dict.youdao.com/webtranslate"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": "https://fanyi.youdao.com/",
    "Cookie": "OUTFOX_SEARCH_USER_ID=1138325494@10.105.137.204; OUTFOX_SEARCH_USER_ID_NCOO=46378145.29139559",
    "Origin": "https://fanyi.youdao.com"
}
# 伪造时间戳,py里面是秒，转成毫秒
times = int(time.time() * 1000)

# 伪造sign，直接复现md5
# 准备数据
d = "fanyideskweb"
e = times
u = "webfanyi"
t = "fsdsogkndfokasodnaso"
str = f"client={d}&mysticTime={e}&product={u}&key={t}"
# 加密得到sign
sign = md5(str.encode("utf-8")).hexdigest()

data = {
    "i": "like",
    "from": "auto",
    "to": "",
    "dictResult": "true",
    "keyid": "webfanyi",
    "sign": sign,
    "client": "fanyideskweb",
    "product": "webfanyi",
    "appVersion": "1.0.0",
    "vendor": "web",
    "pointParam": "client,mysticTime,product",
    "mysticTime": e,
    "keyfrom": "fanyi.web",
    "mid": "1",
    "screen": "1",
    "model": "1",
    "network": "wifi",
    "abtest": "0",
    "yduuid": "abcdefg"
}

# 发送请求
res = requests.post(url, headers=headers, data=data)
print(res.text)
