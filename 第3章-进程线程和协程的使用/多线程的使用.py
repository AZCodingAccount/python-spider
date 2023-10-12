import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait

"""
        前面提到的进程在windows系统下消耗太大，因此爬虫一般不使用多进程抓取。然而多线程也有弊端，由于Python语言中的GIL锁的存在，导致一些场景使用
    多线程并不能显著的提高性能。在IO密集型任务中可以使用这个但是后面又有协程，因此可以说多线程可以说是高不成低不就了，在python的位置很尴尬。
    计算密集型使用多进程好一点（有独立的Python解释器）
    下面实现这些方面：
            1：如何创建并使用多线程，多线程之间如何传参，如何获取线程名称，查看当前主线程，
            2：线程之间数据共享，发生数据不一致问题如何解决（这是指的是多线程同时操作一片内存空间可能影响数据，高版本python已解决这个问题）
            3：线程池如何使用，如何获取线程任务的返回值。获取返回值可通过数据共享实现（kv键值对）
"""


def run(i):
    print(f"{i}号线程{threading.current_thread().name}在执行任务，当前主线程为{threading.main_thread().name}")


def get_name():
    print(f"当前姓名集合里面有{name_list}")


def set_name():
    name_list.append('赵六')
    print("往姓名集合里面添加一个姓名赵六")


def pool_run(i):
    time.sleep(1)  # 睡一秒，不然线程池之间线程直接被重用了，看不到5个线程都被利用起来的效果
    print(f"{i}号线程{threading.current_thread().name}在执行任务，当前主线程为{threading.main_thread().name}")
    return i


if __name__ == '__main__':
    # TODO：创建并使用线程，线程传参，获取当前线程名和主线程名
    # 下面代码创建了4个线程，并把循环变量i传入run方法中，由run方法并发执行多个线程，由循环等待运行完毕，并打印运行run方法的线程的信息
    # # 创建存储线程对象的列表
    # thread_list = []
    # for i in range(1, 5):
    #     thread = threading.Thread(target=run, args=(i,), name=f'thread{i}')
    #     thread_list.append(thread)
    #     thread.start()
    # for thread in thread_list:
    #     thread.join()
    # print("任务执行完毕~")

    # TODO:线程之间如何进行数据共享（显然直接定义全局变量即可）
    # 下面代码定义了一个姓名列表，创建了三个不同的线程，这三个线程对这个列表进行读写操作，观察数据是否可以共享
    name_list = ['张三', '李四', '王五']
    # get_name_thread = threading.Thread(target=get_name)
    # set_name_thread = threading.Thread(target=set_name)
    # get_name2_thread = threading.Thread(target=get_name)
    # get_name_thread.start()
    # set_name_thread.start()
    # get_name2_thread.start()
    # get_name2_thread.join()
    # set_name_thread.join()
    # get_name_thread.join()
    # print("姓名操作完毕~")

    # TODO:线程池的使用
    # 下面代码创建了一个5个容量的线程池，并把任务分配给了五个线程，最后获取线程的返回值
    # pool = ThreadPoolExecutor(5)
    # # 采用简化的写法
    # futures = [pool.submit(pool_run, i) for i in range(1, 6)]
    # # 接收返回值,还可以使用as_completed，那个不返回not_done对象
    # done, not_done = wait(futures)
    # for future in done:
    #     print(future.result())
