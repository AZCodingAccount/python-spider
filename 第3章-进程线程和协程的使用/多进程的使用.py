import os
import time
from multiprocessing import Process, Manager, Pool

"""
        主要介绍下面几个方面：
                1：进程的创建，进程如何传参，进程如何提升效率？
                2：进程之间如何通信
                3：进程池的使用
"""


# 老生常谈的run方法
def run(i):
    # 祖传先睡一秒
    time.sleep(1)
    print("数据正在爬取中~", i)


# 生产者消费者模拟进程通信，应用场景是生产者抓取数据，消费者进程下载数据
def run_provider(msg_queue, time_dict):
    msg_queue.put("product1")
    msg_queue.put("product2")
    msg_queue.put("product3")
    time_dict['producer'] = time.time_ns()
    print(f"生产者——当前父进程是{os.getppid()}，当前子进程是{os.getpid()}")


def run_consumer(msg_queue, time_dict):
    product1 = msg_queue.get()
    time_dict['consumer'] = time.time_ns()
    product2 = msg_queue.get()
    product3 = msg_queue.get()  # 设置timeout时间，几秒内没有生产者放东西就直接结束
    print(f"消费者——当前父进程是{os.getppid()}，当前子进程是{os.getpid()},{product1},{product2},{product3}")


def run_process_pool(i):
    time.sleep(3)
    print(f"进程开始工作了~{i}")


if __name__ == '__main__':
    # TODO:进程创建，传参，提高效率
    # 看一下相对于单进程节约多长时间
    # start_time = time.time()
    # # 定义一个列表存储进程对象
    # p_list = []
    # for i in range(1, 7):
    #     # 创建进程，target传入要让这个子进程干的事（即方法），args传入要传递给这个子进程的参数（加,号防止误认为是字符串或是int等）
    #     p = Process(target=run, args=(i,))
    #     p_list.append(p)
    #     p.start()
    #     # p.terminate()     # 这个方法用于终止进程
    # for p in p_list:
    #     # 为了让主进程等待这些子进程执行完
    #     p.join()
    # end_time = time.time()
    # print(f"一共运行了{end_time - start_time}")  # 只运行了1.6s，而单进程至少是6s多

    # TODO:进程之间如何通讯
    # msg_queue = Manager().Queue()
    # time_dict = Manager().dict()
    # # 创建一个生产者和一个消费者
    # p_provider = Process(target=run_provider, args=(msg_queue, time_dict))
    # p_consumer = Process(target=run_consumer, args=(msg_queue, time_dict))
    # p_provider.start()
    # p_consumer.start()
    # p_provider.join()
    # p_consumer.join()
    # # 这个时间不太固定，探究也没啥意义，生产者生产，消费者消费
    # print(f"父进程结束了~{time_dict.get('producer')},{time_dict.get('consumer')}")

    # 进程池的使用，跟Java线程池，数据库连接池都差不多，为了减少频繁创建和销毁
    p = Pool()  # 不传参默认cpu核心数，传参代表进程池有几个进程
    print(f"cpu核心数为{os.cpu_count()}")
    # 创建32个进程
    for i in range(1, 33):
        p.apply_async(run_process_pool, args=(i,))
    p.close()
    p.join()
    # 打印时候可能同一时刻两个进程打印到控制台就会出现没有正常换行的现象
    print("父进程结束了~")
