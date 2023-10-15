import asyncio
import aiohttp
import aiofiles
import time

from aiohttp import TCPConnector

"""
        协程是爬虫的重中之重，前面提到虽然多进程利于处理计算密集型任务，多线程和协程利于处理IO密集型任务， 但是计算密集型的应用对于爬虫毕竟还是
    几乎没有应用的，因此我们选择的范围是线程和协程，但是线程的切换还是有成本的，协程是在一个线程里面成本会小很多。这里的应用类似于JS的异步。
    主要介绍下面几个方面：
                1：协程的基本使用。创建协程，封装协程为task对象，创建事件循环，添加task到事件循环中
                2：aiohttp和aiofiles的基本使用。(协程当中发请求和存数据的库)
                3：控制协程的并发量
"""


async def run(i):
    await asyncio.sleep(2)
    print(f"第{i}号协程在执行任务")
    return i + 1


# TODO:协程的基本使用
# 简单解释一下下面这行代码，run(i)创建了一个coroutine对象（因为有async修饰），传递给create_task封装程task对象。
# 后面的for循环是创建了4个任务封装成task。通过await关键字等待任务执行的结果添加到res_list里面并打印
# 最后通过async.run(main())函数创建了事件循环并管理这些任务
# async def main():
#     begin_time = time.time()
#     task_list = [asyncio.create_task(run(i)) for i in range(1, 5)]
#     res_list = []
#     for task in task_list:
#         res = await task
#         res_list.append(res)
#
#     print(res_list, time.time() - begin_time)   # 2s多，处理IO也是这样，等待IO时候调用其他协程完成其他任务
#
#
# # 运行主协程
# asyncio.run(main())

# TODO:aiohttp和aiofiles基本使用
# 解释一下下面代码，首先打开aiohttp的客户端服务，然后开启服务端发送请求请求数据。开启客户端时候可以配置ssl连接，指定自己cookies。
# 发送请求时候指定请求头，请求体，请求查询参数。获取数据后使用asyncfiles这个模块进行文件的写入。设置编码格式，异步等待文件写入完成
# async def aio_main():
#     cookies = {}
#     async with aiohttp.ClientSession(connector=TCPConnector(ssl=False), cookies=cookies) as session:
#         params = [('s', '后端')]
#         data = {}
#         headers = {}
#         # proxy = "http://127.0.0.1:10080"  # 有需要自己配置代理
#         html = ""
#         async with session.get('https://bugdesigner.cn', params=params, data=data, headers=headers) as res:
#             print(res.status)
#             # 使用这个所有进行异步加载的都必须加上await等待结果，比如说请求数据，io操作
#             html = await res.text(encoding='utf-8')
#             print(html)
#             # print(await res.read())  请求回来的数据不是文本格式，比如说图片
#             async with  aiofiles.open('index.html', mode='w',encoding='utf-8') as f:
#                 await f.write(html)
# asyncio.run(aio_main())

# TODO:控制协程并发量
# 简单解释一下下面代码。首先创建一个信号量对象，在创建任务的时候创建了20个协程，但是传入了信号量进行约束，因此可以实现5个协程一起执行，控制并发
# async def sem_run(semaphore, i):
#     async with semaphore:
#         await asyncio.sleep(5)
#         print(f"协程正在执行工作——{i}")
#
#
# async def sem_main():
#     semaphore = asyncio.Semaphore(5)
#     task_list = [asyncio.create_task(sem_run(semaphore, i)) for i in range(1, 21)]
#     for task in task_list:
#         await task
#
#
# asyncio.run(sem_main())
