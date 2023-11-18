import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

url = "https://www.kanzhun.com/api_to/search/salary.json"
# 需要复现的查询参数
kiv = "CSpFHJE0TN9oL3rF"
# AES复现
aes = AES.new(key=b'G$$QawckGfaLB97r', IV=b'CSpFHJE0TN9oL3rF', mode=AES.MODE_CBC)
ming = '{"query":"软件开发工程师","cityCode":"","industryCodes":"","pageNum":1,"limit":15}'
mi = aes.encrypt(pad(ming.encode('utf-8'), 16))
b = base64.b64encode(mi).decode().replace("/", "_").replace("+", "-").replace("=", "~")

params = {
    'b': b,
    'kiv': kiv
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    'Cookie': 'wd_guid=5632262a-3e0b-4746-b729-c972d1d21db9; historyState=state; __c=1700303213; __g=-; __l=l=%2Fwww.kanzhun.com%2Fsearch%3FcityCode%3D31%26industryCodes%3D%26pageNum%3D1%26query%3D%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%26type%3D4&r=; Hm_lvt_1f6f005d03f3c4d854faec87a0bee48e=1700299731,1700303213; R_SCH_CY_V=25761614; W_CITY_S_V=31; pageType=1; lasturl="https://www.kanzhun.com/search?cityCode=31&industryCodes=&pageNum=1&query=%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&type=4'
}
res = requests.get(url, params=params, headers=headers)
print(res.text)

# 进行解密的逻辑
aes_decrypt = AES.new(key=b'G$$QawckGfaLB97r', IV=b'CSpFHJE0TN9oL3rF', mode=AES.MODE_CBC)
data=unpad(aes_decrypt.decrypt(base64.b64decode(res.text)),16).decode('utf-8')
print(data)
