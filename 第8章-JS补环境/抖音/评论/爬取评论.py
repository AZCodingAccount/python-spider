import csv
import random
import time

import requests
# 固定格式，用于解决windows执行js文件输出汉字乱码问题
from functools import partial  # 锁定参数
import subprocess

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs  # 此时再引入execjs的时候. 里面就可以自动使用你的subprocess.Popen

from 存储到mysql数据库 import MyDatabase

# 获取任意页的数据，主要进行的测试
def fake_get_data():
    # time.sleep(random.randint(1, 3))  # 每次睡几秒
    cursor = 587 * 20
    count = 20
    params = f"device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7323036659463785791&cursor={cursor}&count={count}&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=120.0.0.0&browser_online=true&engine_name=Blink&engine_version=120.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=1.45&effective_type=3g&round_trip_time=300&webid=7322737813169997322&msToken=X-9sXWNcpTGrbIJ0La4G7SuEFTfKEvsl9OSplNoSfm-xiqor6oqsZI1HlDy9WSyXRxUP5HENnRfeXFtkPEiuf4WgmvrU1BujPNtJcg-kKZfoQNNAQQDoGg=="
    # 读取js代码
    with open('../接单/扣代码.js', mode='r', encoding='utf-8') as f:
        js_code = f.read()

    # 加载代码
    js = execjs.compile(js_code)

    # 执行js代码中的函数，传递url字符串
    X_Bogus = js.call("fn", params)
    params += f"&X-Bogus={X_Bogus}"
    response = requests.get(
        base_url + params,
        headers=headers,
    )
    print(response.json())


def get_all_data():
    global page
    global total_page
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:  # mode一定是a
        for item_id in item_id_list:
            is_begin = True  # 是不是刚开始
            is_continue = 0  # 还要不要继续爬
            page = 1  # 重置页数
            while is_begin or is_continue == 1:
                # time.sleep(random.randint(1, 3))  # 每次睡几秒
                cursor = page * 20
                count = 20
                params = f"device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={item_id}&cursor={cursor}&count={count}&item_type=0&insert_ids=&whale_cut_token=&cut_version=1&rcFT=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=120.0.0.0&browser_online=true&engine_name=Blink&engine_version=120.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=1.45&effective_type=3g&round_trip_time=300&webid=7322737813169997322&msToken=X-9sXWNcpTGrbIJ0La4G7SuEFTfKEvsl9OSplNoSfm-xiqor6oqsZI1HlDy9WSyXRxUP5HENnRfeXFtkPEiuf4WgmvrU1BujPNtJcg-kKZfoQNNAQQDoGg=="
                # 读取js代码
                with open('../接单/扣代码.js', mode='r', encoding='utf-8') as f:
                    js_code = f.read()

                # 加载代码
                js = execjs.compile(js_code)

                # 执行js代码中的函数，传递url字符串
                X_Bogus = js.call("fn", params)
                params += f"&X-Bogus={X_Bogus}"
                response = requests.get(
                    base_url + params,
                    headers=headers,
                )
                # print(response.json())
                # has_more字段应该是标识还有没有数据了，0没有，1有
                is_continue = response.json()['has_more']
                if (is_continue == 0):
                    continue  # 应该是爬取到头了，直接break然后跳到下一个item，或者让他进continue，这里字节应该在上一个请求设置字段啊......
                comments = response.json()['comments']
                # 这里我们存储什么字段？
                # cid 【评论id？】  text：评论内容   digg_count：点赞数   reply_comment_total：评论回复数  nickname：用户昵称   ip_label：所在地域 create_time:创建时间
                # for comment in comments:
                #     print(comment)
                # 下面这个列表推导式做的的工作有从评论中筛选出来指定的字段，并且赋值给新的数组
                fields_ = ['cid', 'aweme_id', 'text', 'digg_count', 'reply_comment_total', 'nickname', 'ip_label',
                           'create_time']
                data = [{k: v for k, v in d.items() if k in fields_} for d in comments]

                print(f"当前爬取的是第{page}页数据，itemid为{item_id}，具体数据是{data}")
                # 1：存储到csv文件:2：存储到mysql数据库

                # 写入CSV
                try:
                    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                    if is_begin:
                        writer.writeheader()
                    for comment in data:
                        writer.writerow(comment)
                except Exception as e:
                    print("写入csv文件时候出错了，错误信息是：", e)

                # 写入mysql
                my_database = MyDatabase()
                my_database.save_data(data)
                page += 1  # 更新页的参数
                total_page += 1  # 更新页的参数
                is_begin = False


if __name__ == '__main__':
    base_url = "https://www.douyin.com/aweme/v1/web/comment/list/?"
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'ttwid=1%7C3RF4jSjUuHRykLjmCE0XvH22oXsLrJjAd_1rhwea81A%7C1704957772%7Cd5de9e3ac1a04f5f28de1740078ca4cde389bb9154032b370fd72447f2eef79b; dy_swidth=1440; dy_sheight=900; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; ttcid=52612352430d49f998d97c8b38ae9b4736; s_v_web_id=verify_lr8vvkte_XEcA0Jys_0GbJ_4kkB_AryH_1UhpKssCsoj7; passport_csrf_token=52440d3ed22f14c0098d58eee34df89d; passport_csrf_token_default=52440d3ed22f14c0098d58eee34df89d; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; bd_ticket_guard_client_web_domain=2; download_guide=%223%2F20240111%2F0%22; passport_assist_user=CkGcEizHYrICAOhlighTQykMuNrH8FVFExZHqq6O8jY4q1ilhCa3qitzfdnSGu3p6Nf6hkmIiG7lRTqtKQ-12PL9-RpKCjzGNSUcJhoarxi4_C5pXOMzO0vo0ET2IEB3mNaXs61TxkF9o9_PDVa00RdALKvWE6spDmtCvf5TcazzrU8QorDGDRiJr9ZUIAEiAQMT9w93; n_mh=13zwzL9MgH4qiZZNvz6VgUrKf7141N7fMjaTafXwvSg; sso_uid_tt=9b8b28c3cf5c814d355a84ef25c89de2; sso_uid_tt_ss=9b8b28c3cf5c814d355a84ef25c89de2; toutiao_sso_user=1f1edda202f5d36d8185131094a4f82e; toutiao_sso_user_ss=1f1edda202f5d36d8185131094a4f82e; sid_ucp_sso_v1=1.0.0-KDIwZTYwODkxOGNmYTM1ZWZhM2Q2MzI2YTgyNDMzMmNhOThkMmFkZGQKHwjk0cCAiozlBhDn0v6sBhjvMSAMMNKEqJAGOAZA9AcaAmxxIiAxZjFlZGRhMjAyZjVkMzZkODE4NTEzMTA5NGE0ZjgyZQ; ssid_ucp_sso_v1=1.0.0-KDIwZTYwODkxOGNmYTM1ZWZhM2Q2MzI2YTgyNDMzMmNhOThkMmFkZGQKHwjk0cCAiozlBhDn0v6sBhjvMSAMMNKEqJAGOAZA9AcaAmxxIiAxZjFlZGRhMjAyZjVkMzZkODE4NTEzMTA5NGE0ZjgyZQ; passport_auth_status=1ffd90169b48b20fc8b94e7edbd9862a%2C; passport_auth_status_ss=1ffd90169b48b20fc8b94e7edbd9862a%2C; uid_tt=8090c4b439be6386ae8c25d643cd00f5; uid_tt_ss=8090c4b439be6386ae8c25d643cd00f5; sid_tt=69eeab161bc0c2fec010a37e04326d84; sessionid=69eeab161bc0c2fec010a37e04326d84; sessionid_ss=69eeab161bc0c2fec010a37e04326d84; LOGIN_STATUS=1; store-region=cn-hl; store-region-src=uid; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=9f92a67df42160bb656dd3dd86775d1a; __security_server_data_status=1; sid_guard=69eeab161bc0c2fec010a37e04326d84%7C1704962427%7C5183983%7CMon%2C+11-Mar-2024+08%3A40%3A10+GMT; sid_ucp_v1=1.0.0-KGY1YmVmOTA0ZmQ1ZGQxOGE0MTEzOTJhM2Q1YWFkMzY0MTEzY2E2MmUKGwjk0cCAiozlBhD70v6sBhjvMSAMOAZA9AdIBBoCaGwiIDY5ZWVhYjE2MWJjMGMyZmVjMDEwYTM3ZTA0MzI2ZDg0; ssid_ucp_v1=1.0.0-KGY1YmVmOTA0ZmQ1ZGQxOGE0MTEzOTJhM2Q1YWFkMzY0MTEzY2E2MmUKGwjk0cCAiozlBhD70v6sBhjvMSAMOAZA9AdIBBoCaGwiIDY5ZWVhYjE2MWJjMGMyZmVjMDEwYTM3ZTA0MzI2ZDg0; pwa2=%220%7C0%7C3%7C0%22; my_rd=2; EnhanceDownloadGuide=%221_1704966403_0_0_0_0%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAJGPAk8yXuLh_sfymNjO_NFrV1fK1u09aBJxPgjJcdQ43_-Beejmxgaf2Mo-80NUp%2F1704988800000%2F0%2F1704966489201%2F0%22; douyin.com; xg_device_score=7.627371509122499; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A7.5%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; csrf_session_id=bccebc3fbe81580f677a46ad97cfcd99; strategyABtestKey=%221705122861.306%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAJGPAk8yXuLh_sfymNjO_NFrV1fK1u09aBJxPgjJcdQ43_-Beejmxgaf2Mo-80NUp%2F1705161600000%2F0%2F1705122861742%2F0%22; passport_fe_beating_status=true; __ac_nonce=065a21c4800cdd38db5e2; __ac_signature=_02B4Z6wo00f01eLlXCgAAIDClMqBZyPmRa3ixViAAB0dcnzK1sJ2X72-3s4aCoADPsuK7-LC1kGnREdKtLNa4HOH6XsmqdjaV6r05Wo2SaunYf3mmsndjs2t2IK61Xabo16db8WYPmUtLyI5a9; SEARCH_RESULT_LIST_TYPE=%22single%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRnMwSWZRUTZUeXFrenpzbU1Zdk1CVHVDTllITVpXMW43L3VQVGRLWFlsbGRHMG4yaS9uT1ZJcXphVG9QVzhGVGFtT3oxeDZBSHQ0NURNSTdNYndhbUk9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; publish_badge_show_info=%220%2C0%2C0%2C1705122897180%22; msToken=k3zUhX77Lp2s8G-gHCdqPiA5LTTTcJreSaGrlUdaQ4YloO3q2AzE_dduIMuOr7yKDyG4gZvsOtqIy2WOSekze7b-dr1YLHOvq0fUsjDWHqS3iTu8vwDUnw==; tt_scid=j8-WPk42cgZtl1U0R6P5p.c1xhG3O4ejJ7jVYiB5bPJK6dRjEVVyinMNdT1LkYQXbe95; odin_tt=704f9f9eb371476ddc6ee5a1b88d44542688ad53451b9e481979b521fb169beb67148c143f9abd0976e6ec6c4a3e8436; msToken=X-9sXWNcpTGrbIJ0La4G7SuEFTfKEvsl9OSplNoSfm-xiqor6oqsZI1HlDy9WSyXRxUP5HENnRfeXFtkPEiuf4WgmvrU1BujPNtJcg-kKZfoQNNAQQDoGg==',
        'referer': 'https://www.douyin.com/search/%E5%A4%A7%E5%BA%86%E5%9B%9E%E5%BA%94%E6%B2%B3%E5%8D%97%E4%B8%AD%E8%80%83%E7%94%9F%E7%A7%BB%E6%B0%91?aid=65a94252-11ae-427d-a91d-f75f7a134446&publish_time=0&sort_type=0&source=recom_search&type=general',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    }
    # 7323036659463785791
    # 第一个视频500多页，第二个视频364页，第三个视频126页
    item_id_list = ["7323036659463785791", "7323096163404565786", "7323115639957163279","7323051287136734479","7323066454583135498","7323054311179603238"]  # 爬取这三个视频的评论
    # cursor = 40  # 偏移量
    # count = 20
    total_page = 1
    page = 1
    start_time = time.time()  # 开始时间
    # 指定CSV文件名
    filename = 'comments.csv'
    try:
        get_all_data()  # 爬取评论数据
        # fake_get_data()
    except Exception as e:
        print("爬取数据发生了异常，异常信息为", e)
    end_time = time.time()

    print(f"数据爬取完成，爬取{total_page}页数据，数据共{20 * total_page}条，花费时间为{int((end_time - start_time))}秒")
