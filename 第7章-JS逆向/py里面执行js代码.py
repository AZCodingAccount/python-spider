# 固定格式，用于解决windows执行js文件输出汉字乱码问题
from functools import partial  # 锁定参数
import subprocess

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs  # 此时再引入execjs的时候. 里面就可以自动使用你的subprocess.Popen

# 读取js代码
with open('./抠出来的代码文件.js', mode='r', encoding='utf-8') as f:
    js_code = f.read()

# 加载代码
js = execjs.compile(js_code)

# 执行js代码中的函数，可以看出，就跟多进程一样，就是直接调用的函数，里面的log是不执行的
# c = js.call("fn", 1, 2)
# print(c)
#
# c2 = js.call("fn2")
# print(c2)

# # 直接执行js代码
# js_code2="""
#  '牛逼666我的宝贝'.substring(0,2)
# """
# c3 = js.eval(js_code2)
# print(c3)
