# 导包
from bson import ObjectId
from pymongo import MongoClient

"""
            MongoDB数据库好像是Node生态里面的一个十分重要的数据库，它的特点是是非关系型数据库，非常自由，键值对形式。
        你可以不用关心数据的约束，因为没有约束（当然可以自定义约束）。
        这里演示数据库的连接和关闭和简单的CRUD
"""

# # 连接数据库
# conn = MongoClient(host="localhost", port=27017)
# collection = conn.test.test
#
# # 获取当前数据库名称
# database_name = conn.test.name
# print(database_name)

# TODO:添加数据
# 插入数据
# data = collection.insert_one({"name": "zhangsan", "age": 18, "gender": "women"})
# # print(data.inserted_id)
# # 插入多条数据
# many_data = collection.insert_many([{"name": "lisi", "age": 18, "gender": "women"},
#                                     {"name": "wangwu", "age": 20, "gender": "man"},
#                                     {"name": "zhaoliu", "age": 22, "gender": "women", "hobby": "唱跳rap"}])
# 打印插入的id列表
# print(list(map(str, many_data.inserted_ids)))

# TODO:查询数据
# 查询单个数据
# result_one = collection.find_one({"name": "zhangsan"})
# print(result_one)
# 查询所有数据
# result_all = collection.find({"name": "zhangsan"})
# 把列表转换成字符串形式并且换行
# print("\n".join(map(str, result_all)))
# 根据id查询
# result_id = collection.find({"_id": ObjectId("652fe0ef60e487842ba421f5")})
# print(list(result_id)[0])
# 排序查询，查询大于等于20的并降序排列
# result_sort = collection.find({"age": {"$gte": 20}}).sort("age", -1)
# 使用列表推导式打印所有符合条件的数据
# [print(item) for item in result_sort]
# 限制打印5条
# result_sort_limit = collection.find({"age": {"$gte": 20}}).sort("age", -1).limit(5)
# [print(item) for item in result_sort_limit]

# # TODO：更新数据
# # 修改第一个符合条件的数据，把name为zhangsan的age设置为99
# update_one_result = collection.update_one({"name": "zhangsan"}, {"$set": {"age": 99}})
# print(f"受影响的条数为{update_one_result.matched_count}条")
# # 修改所有符合条件的数据,把name为lisi的name都设置为李四,age设置为10086
# update_many_result = collection.update_many({"name": "lisi"}, {"$set": {"name": "李四", "age": 10086}})
# print(f"受影响的条数为{update_many_result.matched_count}条")

# # TODO：删除数据
# # 删除第一条符合条件的数据,删除第一个age为99的数据
# delete_result = collection.delete_one({"age": 99})
# print(f"删除的条数为{delete_result.deleted_count}条")
# # 删除多条数据，删除所有名字为zhangsan的用户和age为10086的用户（就是李四）
# delete_many_result = collection.delete_many({"$or": [{"name": "zhangsan"}, {"age": 10086}]})
# print(f"删除的条数为{delete_many_result.deleted_count}条")

# # 关闭数据库连接
# conn.close()
