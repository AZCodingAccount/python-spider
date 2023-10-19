import time

import redis

"""
            redis是一个非常好用的nosql数据库，一般跟后端生态连接起来了，redis一共有10大数据类型，这里就简单介绍一下
        1：redis的连接和关闭
        2：redis5大数据类型，str，list，hash，set，zset的存取操作
        3：redis的常见命令，删除键，获取键的数据类型，获取所有键，查看库，切换库，刷新库
"""

# TODO：连接数据库
# 这里连接是我本地虚拟机的redis，要确定redis.conf配置文件可以允许外部连接，并且要打开虚拟机的6380端口,Centos7
'''
sudo firewall-cmd --list-all
sudo firewall-cmd --zone=public --add-port=6380/tcp --permanent
sudo firewall-cmd --reload
'''
r = redis.StrictRedis(host="192.168.182.100", port=6380, password='123456', db=0, decode_responses=True)

# TODO:五大数据类型的操作
# 对字符串的操作
r.set('name', "张狗蛋")
print(r.get("name"))
# 设置过期时间
r.set("expire_key", "value", 20)
time.sleep(1)
ttl = r.ttl("expire_key")
print(f"还有{ttl}秒过期")

# 使用列表
# 左插法，因此先进去的应该是最后打印的
r.lpush('hobby', '唱', '跳', 'rap')
r.lpush('hobby', '篮球')
print(r.lrange('hobby', 0, -1))

# 使用哈希表
r.hset("person", "name", "zhangsan")
r.hset("person", "age", "18")
# 一次添加多个键值对
r.hset('person', mapping={"name": "李四", "age": 23, "gender": "man"})
# 获取单个键的值
print(r.hget("person", "age"))
# 获取person里面的所有键值对
print(r.hgetall("person"))

# 使用集合
r.sadd('features', "thin", "handsome", "wealthy")
print(r.smembers("features"))
print(r.sismember("features", "fat"))

# 使用zset
r.zadd("ips", {"ip1": 100, "ip2": 98, "ip3": 60, "ip4": 58})
# 从低到高，并且返回分数
print(r.zrange("ips", 0, -1, withscores=True))
# 从高到低返回
print(r.zrevrange("ips", 0, -1, withscores=True))
# 修改分数的值，给ip2这个元素的分数-1
r.zincrby("ips", -1, "ip2")
print(r.zrange("ips", 0, -1, withscores=True))

# TODO:redis的常用操作
# 删除单个键
r.delete("name")
# 查询所有键
keys = r.keys("*")
print(f"所有的键为：{keys}")
# 查看当前键的数据类型
r_type = r.type("ips")
print(f"ips键的数据类型为：{r_type}")
# 查询当前数据库
current_db = r.connection_pool.connection_kwargs['db']
print(f"当前数据库为：{current_db}库")
# 切换数据库
db = r.select(1)
print(f"切换结果：{db}")
# 清空所有数据库缓存
r.flushall()
print("数据库清除成功~")
