import requests


# 普通代理
def get_proxy_dict():
    key = "6JD3LFEN"  # 用户key
    passwd = "D3BDB526FEE2"  # 用户密码

    res = requests.get(
        url="https://share.proxy.qg.net/get?key=6JD3LFEN&num=1&area=&isp=&format=json&seq=&distinct=false&pool=1"
    )
    host = res.json()['data'][0]['server']  # 121.29.81.215:52001

    # 账密模式
    proxy = 'http://{}:{}@{}'.format(key, passwd, host)

    return {"http": proxy, "https": proxy}


# 隧道代理
def get_tunnel_proxies():
    proxy_host = "tunnel3.qg.net:15156"
    proxy_username = "2F9CDB09"
    proxy_pwd = "F120C8FC7845"

    return {
        "http": f"http://{proxy_username}:{proxy_pwd}@{proxy_host}",
        "https": f"http://{proxy_username}:{proxy_pwd}@{proxy_host}"
    }
