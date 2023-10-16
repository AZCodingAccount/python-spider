import time

from selenium.webdriver import Chrome

"""
        selenium本来是一个自动化测试工具，后来因为它是直接操作浏览器不容易被反爬就被用到了爬虫领域，但是一般用的也不太多。实在请求不到数据了，
    再使用它。
    下面演示这几个方面：
                1：selenium快速启动
                2：selenium定位元素
                3：selenium进阶操作，无头浏览器，处理cookie，解决frame嵌套问题
"""
# TODO:selenium快速启动
# 创建浏览器对象
blog = Chrome()
# 访问我的博客网站
blog.get("http://www.bugdesigner.cn")
# 打印我的博客网站的标题
print(blog.title)
# 给主页截个图
blog.save_screenshot("homepage.png")

# 搜索关于Docker的文章
# 找到输入框，给输入框设置值为Docker
blog.find_element("id", "search-widgets").send_keys("Docker")
# 点击搜索按钮
blog.find_element("id", "searchsubmit").click()

# 获取页面内容
source_code = blog.page_source
print(source_code)
# 获取cookie
cookies = blog.get_cookies()
print(cookies)
# 获取当前url
url = blog.current_url
print(url)
# 不让进程停止，这样浏览器就不会自动退出
input("输入任何东西结束")
# 退出
blog.close()  # 退出当前页面
blog.quit()  # 退出浏览器
