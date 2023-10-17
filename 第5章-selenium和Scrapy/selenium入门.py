import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

"""
        selenium本来是一个自动化测试工具，后来因为它是直接操作浏览器不容易被反爬就被用到了爬虫领域，但是一般用的也不太多。实在请求不到数据了，
    再使用它。
    下面演示这几个方面：
                1：selenium快速启动
                2：selenium定位元素
                3：selenium进阶操作，无头浏览器，处理cookie，解决frame嵌套问题
"""
# # TODO:selenium快速启动
# # 创建浏览器对象
# blog = Chrome()
# # 访问我的博客网站
# blog.get("http://www.bugdesigner.cn")
# blog.maximize_window()  #最大化浏览器窗口
# # 打印我的博客网站的标题
# print(blog.title)
# # 给主页截个图
# blog.save_screenshot("homepage.png")
#
# # 搜索关于Docker的文章
# # 找到输入框，给输入框设置值为Docker
# blog.find_element("id", "search-widgets").send_keys("Docker")
# # 点击搜索按钮
# blog.find_element("id", "searchsubmit").click()
#
# # 获取页面内容
# source_code = blog.page_source
# # print(source_code)
# # 获取cookie
# cookies = blog.get_cookies()
# # print(cookies)
# # 获取当前url
# url = blog.current_url
# # print(url)

# # TODO:selenium定位元素
# # selenium提供很多选择器，但是常用的只有三个，css，id，xpath。
# # 使用选择器值定位。获取博客内有关Docker的文章内容
# labels = blog.find_elements(By.CSS_SELECTOR, ".a-post .label")
# titles = blog.find_elements(By.CSS_SELECTOR, ".a-post .title a")
# contents = blog.find_elements(By.CSS_SELECTOR, ".a-post .content p")
# data = {
#     "label": labels,
#     "title": titles,
#     "content": contents
# }
# for key, value in data.items():
#     for index, item in enumerate(value):
#         print(f"第{index + 1}个文章的{key}为{item.text}")

# # TODO:selenium进阶操作
# # 1. 获取当前所有的窗口
# current_windows = blog.window_handles
# # 2. 根据窗口索引进行切换
# blog.switch_to.window(current_windows[1])

# # 无头浏览器
# opt = Options()
# opt.add_argument("--headless")
# opt.add_argument('--disable-gpu')
# opt.add_argument("--window-size=4000,1600")  # 设置窗口大小
#
# noHeaderDriver = Chrome(options=opt)
# noHeaderDriver.get("https://www.bugdesigner.cn")
# cookies = noHeaderDriver.get_cookies()

# # 添加cookie
# for cookie in cookies:
#     print(cookie)
#     noHeaderDriver.add_cookie(cookie)
# noHeaderDriver.get("https://www.bugdesigner.cn")
# title1 = noHeaderDriver.title
# print(title1)
# # 不让进程停止，这样浏览器就不会自动退出
# input("输入任何东西结束")
# 对页面的操作
# blog.forward()     # 前进
# blog.back()        # 后退
# blog.refresh()    # 刷新
# blog.close()  # 退出当前页面
# blog.quit()  # 退出浏览器
