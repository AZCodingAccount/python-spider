from functools import partial  # 锁定参数
import subprocess

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

import execjs
import requests

# 0XwwzxGlqEopfJXc0zE5LyGT0xKVdsseU2Gk3EmS3Ndm5iTe71ct5Eo7wWJ5EmXLFMA19OpyZAccLG10Wqk_2.4AJgAiccOn6
"""
        这个是碰运气，我找了两小时，在拦截器发送的时候还没有带查询参数呢，但是发出去的时候带了个很诡异的查询字符串。于是我就继续单步调试
    后来是在VM的js文件里面找到了加密入口，但是太难调用了（见请求参数加密.js），不知道他们是改了axios的源码还是引入了第三方包。
    这个网站请求参数带了个查询参数，试了一下同一请求参数还不一样。但是它发送请求的时候请求头或者查询参数也没带什么时间戳之类的信息，服务端校验怎么校验呢
    因此我就猜测这个可能是它就根据一定算法生成的一个参数，那么它随机，我就直接定死就可以了，发个请求还真能返回数据（后来发现就算不带这个参数也是能返回数据）
    至于解密就太简单了，标准的DES加密。iv都没用
    （ps，这种网站用vue2写的，一看就不太专业，他们的加密也不会很难，猜就行，服务端校验也不会特别严格。
        禁用F12可以使用右边那个开发者工具打开，有的无限debugger等就得用其他方法过了）
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    , "Referer": "https://ctbpsp.com/",

}
oArpptFq = "0ofDDValqEtvpRign5gCU7Tm8ZF8BW5db.6bPxs1lQ2lSW8c8nRDpEi0nXordd_3e_FWQt..gA3yLTG34PguuJDy5OOkd.fYC"
url = f"https://ctbpsp.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/1?oArpptFq={oArpptFq}"

resp = requests.get(url, headers=headers)

# 打印一下看看是不是返回加密前的疏忽了
print(resp.text)

# 读取js代码
f = open('返回数据解密.js', mode='r', encoding='utf-8')
js_code = f.read()
f.close()

# 加载代码
js = execjs.compile(js_code)
# 返回回来的加密数据去解密
result = js.call("decryptByDES", resp.text.strip('"'))
print(result)
