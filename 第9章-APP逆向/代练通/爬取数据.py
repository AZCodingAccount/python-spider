import pprint
import time
import requests
from urllib.parse import parse_qs, urlparse, parse_qsl
from hashlib import md5

from 数据库操作 import MyDatabase
from Heroes import heroes  # 会自动运行Heroes里面的代码

"""
        这个逆向其实并不难，但是为了对代练通的尊重，我还是该插桩插桩，该hook就hook，其实就是一个简单的请求参数+时间戳+signkey的md5加密，作为app逆向的入门案例还是挺不错的。
    主要的思路就是逆向出来sign，把代练通app反编译出来搜索LevelOrderList，话说代练通是DCloud旗下的吗，还是使用uniapp开发的，怎么包名都不是代练通。    
"""


# 这些参数的含义分别是，分页索引，分页长度，接单状态（1普通接单，9已被接单），平台（1安卓全区，0安卓ios都有），查询字符串
def get_logined_data(page_index, page_size, pub_type, pg_type, search_str):
    # 伪造时间戳
    time_stamp = int(time.time())
    # 准备url
    UserID = 11340745  # 这个使用UserID的时候会从本地里面拿出来token校验，这里我们没有把token拿出来，所以就不搞这个了。如果想的话，去hook getUserToken这个方法
    url = f"https://server.dailiantong.com.cn/API/APPService.ashx?Action=LevelOrderList&IsPub={pub_type}&GameID=107&ZoneID=0&ServerID=0&SearchStr={search_str}&Sort_Str=&PageIndex={page_index}&PageSize={page_size}&Price_Str=&PubCancel=0&SettleHour=0&FilterType=0&PGType={pg_type}&Focused=-1&STier=&ETier=&Score1=0&Score2=0&UserID={UserID}&TimeStamp={time_stamp}&Ver=1.0&AppOS=Android&AppID=DLTAndroid&AppVer=4.3.1&Sign=3d19d7bfd9b74e4dc6c913105ed3bf88"
    base_url = "https://server.dailiantong.com.cn/API/APPService.ashx"  # 这个是发请求的url

    query = urlparse(url).query  # 提取出查询字符串
    params = dict(parse_qsl(query, keep_blank_values=True))  # 把查询参数转成字典方便处理
    signKey = "9c7b9399680658d308691f2acad58c0a"  # app里面的salt
    UserToken = "CA0DCB65795E46B798BD0134705891C3"  # UserToken，这个没有就不能有UserID，UserID也得用那个0的
    # 但是如果不登录能爬取的数据不太准确，但是登录了返回的数据变少了，看自己的取舍吧，
    # 获取用于加密md5的字典
    value_dict = dict(parse_qsl(query[:query.rfind("&")]))
    ValueStr = ""  # 模仿加密时的拼接字符串
    # 循环读取
    for key, value in value_dict.items():
        ValueStr += value

    sign = md5((signKey + ValueStr + UserToken).encode("utf-8")).hexdigest()  # 获取sign值
    params['Sign'] = sign  # 拼接到查询参数里面
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I003DD Build/PI)",
        "Host": "server.dailiantong.com.cn",
    }
    # 发送请求
    res = requests.get(base_url, headers=headers, params=params)
    return res.json()


# 这个函数是不登录的时候发请求
# 这些参数的含义分别是，分页索引，分页长度，接单状态（1普通接单，9已被接单），平台（1安卓全区，0安卓ios都有），查询字符串
def get_data(page_index, page_size, pub_type, pg_type, search_str):
    # 伪造时间戳
    time_stamp = int(time.time())
    # 准备url
    UserID = 0  # 这个使用UserID的时候会从本地里面拿出来token校验，这里我们没有把token拿出来，所以就不搞这个了。如果想的话，去hook getUserToken这个方法
    url = f"https://server.dailiantong.com.cn/API/APPService.ashx?Action=LevelOrderList&IsPub={pub_type}&GameID=107&ZoneID=0&ServerID=0&SearchStr={search_str}&Sort_Str=&PageIndex={page_index}&PageSize={page_size}&Price_Str=&PubCancel=0&SettleHour=0&FilterType=0&PGType={pg_type}&Focused=-1&STier=&ETier=&Score1=0&Score2=0&UserID={UserID}&TimeStamp={time_stamp}&Ver=1.0&AppOS=Android&AppID=DLTAndroid&AppVer=4.3.1&Sign=3d19d7bfd9b74e4dc6c913105ed3bf88"
    base_url = "https://server.dailiantong.com.cn/API/APPService.ashx"  # 这个是发请求的url

    query = urlparse(url).query  # 提取出查询字符串
    params = dict(parse_qsl(query, keep_blank_values=True))  # 把查询参数转成字典方便处理
    signKey = "9c7b9399680658d308691f2acad58c0a"  # app里面的salt
    # 但是如果不登录能爬取的数据不太准确，但是登录了返回的数据变少了，看自己的取舍吧，
    # 获取用于加密md5的字典
    value_dict = dict(parse_qsl(query[:query.rfind("&")]))
    ValueStr = ""  # 模仿加密时的拼接字符串
    # 循环读取
    for key, value in value_dict.items():
        ValueStr += value

    sign = md5((signKey + ValueStr).encode("utf-8")).hexdigest()  # 获取sign值
    params['Sign'] = sign  # 拼接到查询参数里面
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I003DD Build/PI)",
        "Host": "server.dailiantong.com.cn",
        "Cookie": "SERVERID=e99d03716a9aa7fd702a811546645e6b|1700577296|1700576638; SERVERCORSID=e99d03716a9aa7fd702a811546645e6b|1700577296|1700576638"
        # cookie带不带都行
    }
    # 发送请求
    res = requests.get(base_url, headers=headers, params=params)
    return res.json()


def get_all_data(pub_type, pg_type):
    count = 0
    # 创建类实例
    my_database = MyDatabase()
    start_time = time.time()
    for i in range(0, 2000):
        res = get_data(i + 1, 20, pub_type, pg_type, "")
        # 存储数据
        count += len(res["LevelOrderList"])
        print(i + 1, res["RecordCount"])
        time.sleep(1000)
        if len(res["LevelOrderList"]) == 0:
            break
        my_database.save_data(res)
        time.sleep(5)  # 每次睡5秒
    my_database.close()
    print("----------------------------------------")
    print(f"本次数据爬取完成，共爬取{count}条数据，花费{time.time() - start_time}秒")


def get_data_by_search_str(search_str):
    count = 0
    # 创建类实例
    my_database = MyDatabase()
    start_time = time.time()
    for i in range(0, 2000):
        res = get_logined_data(i + 1, 20, 1, 0, search_str)
        # 存储数据
        count += len(res["LevelOrderList"])
        print(f"第{i + 1}次请求，总数据还有{res['RecordCount']}条")
        time.sleep(1000)

        if len(res["LevelOrderList"]) == 0:
            break
        my_database.save_heroes_data(res, search_str)
        time.sleep(5)  # 每次睡5秒
    my_database.close()
    print(f"本次数据爬取完成，共爬取{count}条数据，花费{time.time() - start_time}秒")
    print("----------------------------------------------------")


if __name__ == '__main__':
    """
        一共27个字段，其实我主要想分析的是单价，但是没有真机，用模拟器升一下新版本直接闪退，也不知道怎么这个UnitPrice这个字段才可以有值，感觉是查询参数这里设置的，
    但是也抓不到包，很烦。因此这里就简单分析一下，以后有真机了再重新搞这个。还有这个筛选巅峰赛荣耀战力功能，是通过levelType实现的，但是也很奇怪，筛选出来的根本不对。
    这里就简单一点，只提取:
    标题(Title)、价格(Price)、安全保证金(Ensure1)、效率保证金(Ensure2)、时间限制(TimeLimit)、发单人(Create)、发布时间(Stamp)、游戏大区(Zone)
    ! Stamp比真实时间戳少了255845872秒，到时候记得加上去。加上三个字段 单价UnitPrice、发单者ID(UserID)、订单号(SerialNo)
    第二个分析的点是指定英雄的所有订单    
    2023-11-21：update  这次我把UserToken和UserID加上去了，用来爬取指定英雄的所有订单（不登录好东西不让看）。
    新的表字段我还是用的原来的字段，只不过加了一个hero方便分组
    
    
    """
    # get_all_data(1,1) # 这里爬取未被抢的订单，安卓的，失误
    # get_all_data(9,1) # 这里爬取已被抢的订单，安卓的，失误
    # 这里爬取所有订单（包括安卓和ios）
    # get_all_data(1, 0)

    # 这里对每一个英雄进行搜索爬取
    for index, hero in enumerate(heroes):
        print(f"第{index + 1}个英雄，英雄是{hero}")
        get_data_by_search_str(hero)
