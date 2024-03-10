from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

"""
    使用selenium模拟访问Github主页、玩玩就行了，刷徽标的访问量（仓库）、刷fork次数也是一样的道理 fork完再删再fork。
"""

# 无头浏览器
opt = Options()
opt.add_argument("--headless")
opt.add_argument('--disable-gpu')

# todo：自己的主页或者仓库地址
url = "https://github.com/AZCodingAccount"
noHeaderDriver = Chrome(options=opt)
try:
    for i in range(0, 51):
        noHeaderDriver.get(url)

        # 隐式等待页面加载
        noHeaderDriver.implicitly_wait(5)

        print(f"访问第{i + 1}次")
except Exception as e:
    print("出现异常，异常原因", e)
