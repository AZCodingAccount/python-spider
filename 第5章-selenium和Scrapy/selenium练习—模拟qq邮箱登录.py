# 实现一些访问时候的停止功能模块
import random
import time
# 创建Chrome的web驱动模块和选择器模块和可选项模块
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# 显式等待模块，没用上
from selenium.webdriver.support.ui import WebDriverWait
# 模拟鼠标行为的模块
from selenium.webdriver.common.action_chains import ActionChains
# 打码平台用到的模块
import base64
import requests

"""
    这个练习实现了QQ邮箱的自动登录，技术点有:
                    1：iframe的嵌套
                    2：打码平台的使用
                    3：一些选择器，基本语法，隐式显式等待，全局option等等
    用户名和密码改一下就能用，打码平台token需要自己整一个。
"""


# 定义一个切换iframe的函数
def change_iframe():
    qq_driver.switch_to.default_content()  # 先回到主页面
    iframe = qq_driver.find_element(By.XPATH,
                                    "//iframe[contains(@src,'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=102013353&scope=get_user_info%2Cget_app_friends&theme=10&auth_item_state=1&redirect_uri=https%3A%2F%2Fwx.mail.qq.com%2Flist%2Freadtemplate%3Fname%3Dlogin_jump.html%26scene%3D1%26login_type%3Dqq')]")
    qq_driver.switch_to.frame(iframe)
    iframe2 = qq_driver.find_element(By.XPATH,
                                     "//iframe[contains(@src,'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=716027609&daid=383&style=33&login_text=%E7%99%BB%E5%BD%95&hide_title_bar=1&hide_border=1&target=self&s_url=https%3A%2F%2Fgraph.qq.com%2Foauth2.0%2Flogin_jump&pt_3rd_aid=102013353&pt_feedback_link=https%3A%2F%2Fsupport.qq.com%2Fproducts%2F77942%3FcustomInfo%3D.appid102013353&theme=10&verify_theme=')]")
    qq_driver.switch_to.frame(iframe2)


# 打码平台的函数
def decode_code():
    # 开始打码
    url = "http://www.jfbym.com/api/YmServer/customApi"
    with open(r'verifyCode.png', 'rb') as f:
        im = base64.b64encode(f.read()).decode()
    data = {
        'token': 'xxxxxxxx',  # 输入自己的token
        'type': '30221',
        'image': im,
    }
    _headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=_headers, json=data)
    # 其实也就是中点位置，这个时候对数据进行处理,边框大概是4px，忽略就好了
    # 对x值进行这样的处理，如果说x>290px,那么直接给x赋值为135（最右边）。如果说<10px，直接给x赋值为-135（最左边）.其他的就给x值减去150px
    # 对y值进行这样的处理，直接给y-115px就可以了
    # 点击验证码模拟鼠标操作
    coords_str = response.json().get('data').get('data')
    coords = [tuple(map(int, coord.split(','))) for coord in coords_str.split('|')]
    print(coords)
    # 使用ActionChains模拟鼠标操作
    actions = ActionChains(qq_driver)
    verify_frame = qq_driver.find_element(By.ID, "newVcodeIframe")
    for coord in coords:
        x, y = coord
        if x > 290:
            x = 135
        elif x < 10:
            x = -135
        else:
            x = x - 150
        y = y - 115
        # 为了提供更精确的点击，将鼠标移到验证码元素的左上角，然后偏移特定的x, y坐标
        actions.move_to_element_with_offset(verify_frame, x, y).click().perform()


# 通过验证码的函数
def pass_verifyCode():
    global newVcodeIframe
    while newVcodeIframe.is_displayed():
        # 出现弹框了截个图，截取指定部分的，等下发给打码平台
        qq_driver.find_element(By.ID, "newVcodeIframe").screenshot("verifyCode.png")
        print("验证码截图成功~")
        # 开始打码
        decode_code()
        change_iframe()
        # 这个非常重要，你还得进一层iframe，不然找不到那个按钮
        path3 = "//iframe[contains(@src,'https://captcha.gtimg.com/1/template/drag_ele.html')]"
        iframe3 = qq_driver.find_element(By.XPATH, path3)
        qq_driver.switch_to.frame(iframe3)
        # 点击确认按钮
        qq_driver.find_element(By.CLASS_NAME, "verify-btn-text").click()
        # 强制等待5s，看看页面是不是跳转了，如果验证失败或者二次验证就继续循环验证
        time.sleep(5)
        change_iframe()
        # 更新页面的可见性，这里之所以获取一下是因为如果再循环就报错了，严谨一点
        newVcodeIframe = qq_driver.find_element(By.ID, "newVcodeIframe")


def input_info():
    # 获取用户名和密码这个输入框，填充数据并点击登录
    qq_driver.find_element(By.ID, "u").send_keys("xxxxxx")
    qq_driver.find_element(By.ID, "p").send_keys("xxxxx")
    # 旧版验证码，因此点击太快会提示你没有输入验证码
    # verify_area = qq_driver.find_element(By.ID, "verifycode")
    # current_value = verify_area.get_attribute("value")
    qq_driver.implicitly_wait(10)
    # 获取新版验证码对象
    newVcodeArea = qq_driver.find_element(By.ID, "newVcodeArea")
    # 腾讯本身表单有问题，就一直点击这个按钮，除非出现了验证码。还需要考虑不需要登录的情况，点击一次系统会自动更新这个可见性
    # 因此循环内不需更新条件也不会出现死循环，
    while not newVcodeArea.is_displayed():
        try:
            qq_driver.find_element(By.ID, "login_button").click()
        except:
            time.sleep(random.randint(1, 3))
            print("继续点击按钮~")


if __name__ == '__main__':
    # 禁用弹出框
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    # 创建驱动对象
    qq_driver = Chrome(options=chrome_options)
    # 启动浏览器
    qq_driver.get("https://mail.qq.com")
    qq_driver.maximize_window()
    # 改变当前frame
    change_iframe()
    # 获取密码登录这个超链接并点击
    qq_driver.find_element(By.ID, "switcher_plogin").click()
    # 输入用户名和密码
    input_info()
    # 强制等5s，给验证码加载的时间
    time.sleep(5)
    newVcodeIframe = qq_driver.find_element(By.ID, "newVcodeIframe")
    # 通过验证码
    pass_verifyCode()
    # 通过验证码以后一般就是进去了，但是还有的还需要进行短信验证，这里需要虚拟机或者说第三方云平台啥的。但是原理是一样的
# 来个死循环，让页面不自动关闭
while True:
    pass
