import json
from flask import Flask, render_template, request  # pip install Flask
from flask_cors import CORS
app = Flask(__name__)


# 跨域相关配置，最后也没带过来cookie~(失败的尝试，话说为啥该配的都配了本地还是带不过来cookie啊)
# CORS(app, origins="http://localhost:63342")
#
# CORS(app, supports_credentials=True)  # 注意添加supports_credentials=True
#
#
# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:63342'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type,token,token2'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
#     return response


@app.route("/")
def index():
    # 跳转到首页
    print("你曾经来过服务器")
    name = "alex"
    # 数据是在这里渲染后, 返回个客户端的html
    return render_template("JQuery发送AJAX请求.html", name=name)


# 开发一个接收get请求的接口
@app.route("/ajax_get")
def ajax_get_req():
    print(request.headers.get("token2"))
    # 接收cookie中的信息
    print(request.cookies.get("name"))
    n = request.cookies.get('name')
    print(n)
    if not n:
        return "没有cookie就不要来了."
    # 接收header中的信息
    token = request.headers.get('token')
    if not token:
        return "没token还想来?"

    # Flask接收get请求的参数
    name = request.args.get('name')
    _ = request.args.get('_')
    if name and _:
        # 返回json
        return {"name": 'zhangsan', "id": 10086, "isMen": True}
    else:
        return "回家去吧"


# 开发一个接收post请求的接口
@app.route("/ajax_post", methods=['POST'])
def ajax_get_post():
    # time.sleep(3)
    # 接收JSON数据
    print(request.json)

    lst = [
        {"id": 1, "name": "张飞", "age": 16},
        {"id": 2, "name": "孙斌", "age": 16},
        {"id": 3, "name": "樵夫", "age": 16},
        {"id": 4, "name": "大佬", "age": 16},
    ]

    return json.dumps(lst)


# 开发一个处理jsonp的接口
@app.route("/process_jsonp", methods=["GET"])
def process_jsonp():
    # 获取回调字符串
    cb = request.args.get("cb")
    data = {
        "name": "zhangsan",
        "age": 18
    }
    # 实际上就是导入script标签（不受同源策略的影响），自己就运行了，AJAX自己封装了一下。现在不用这个了，都是CORS，设置一下就可以访问了
    """
      <script src="http://127.0.0.1:5050/process_jsonp?callback=cb"></script>我们这里返回的时候就相当于把这个函数给运行了
     cb({"name":"zhangsan","age":18})。客户端那里有个函数等着接数据，数据就是这个cb里面的参数，
     这个相当于各种注入，SQL注入,URL注入，就是拼接。用来过CrossOrigin的 。因此逆向的时候可能会有a{..........}里面一大坨东西就是jsonp   
    """
    return cb + "(" + json.dumps(data) + ")"

if __name__ == '__main__':
    app.run()
