# 固定格式，用于解决windows执行js文件输出汉字乱码问题
from functools import partial  # 锁定参数
import subprocess

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs  # 此时再引入execjs的时候. 里面就可以自动使用你的subprocess.Popen

import requests

url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
data = {
    "ids": "[1404596131]",
    "level": "standard",
    "encodeType": "aac",
    "csrf_token": ""
}

# 读取js代码
with open('./网易云-扣代码.js', mode='r', encoding='utf-8') as f:
    js_code = f.read()

# 加载代码
js = execjs.compile(js_code)

data = js.call("encrypt_data", data)
# print(data)
res = requests.post(url, headers=headers, data={"params": data.get("encText"), "encSecKey": data.get("encSecKey")})
print(res.json())
# 提取歌曲url
song_url = res.json()['data'][0]['url']
print(song_url)

# 下载音乐
res = requests.get(song_url, headers=headers)
with open("see you again.m4a",mode='wb') as f:
    f.write(res.content)
