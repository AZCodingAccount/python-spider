import threading

"""
        前面提到的进程在windows系统下消耗太大，因此爬虫一般不使用多进程抓取。然而多线程也有弊端，由于Python语言中的GIL锁的存在，导致一些场景使用
    多线程并不能显著的提高性能。在IO密集型任务中可以使用这个但是后面又有协程，因此可以说多线程可以说是高不成低不就了，在python的位置很尴尬。
    计算密集型使用多进程好一点（有独立的Python解释器）
    下面实现这些方面：
            1：如何创建并使用多线程，多线程之间如何传参，如何获取线程名称，查看当前主线程，
            2：线程之间数据共享，发生数据不一致问题如何解决
            3：线程池如何使用，如何获取线程任务的返回值
"""


def run(i):
    print(f"{i}号线程{threading.current_thread().name}在执行任务，当前主线程为{threading.main_thread().name}")


def get_name():
    print(f"当前姓名集合里面有{name_list}")


def set_name():
    name_list.append('赵六')
    print("往姓名集合里面添加一个姓名赵六")


if __name__ == '__main__':
    # TODO：创建并使用线程，现成传参，获取当前线程名和主线程名
    # # 创建存储线程对象的列表
    # thread_list = []
    # for i in range(1, 5):
    #     thread = threading.Thread(target=run, args=(i,), name=f'thread{i}')
    #     thread_list.append(thread)
    #     thread.start()
    # for thread in thread_list:
    #     thread.join()
    # print("任务执行完毕~")

    name_list = ['张三', '李四', '王五']
    get_name=threading.Thread(target=get_name)
    set_name=threading.Thread(target=set_name)
    # get_name2=threading.Thread(target=get_name)
    get_name.start()
    set_name.start()
    # get_name2.start()
    # get_name2.join()
    set_name.join()
    get_name.join()
    print("姓名操作完毕~")

