import pymysql

"""
    这里主要演示MySQL数据库的连接和如何执行sql语句。一些其他的分页，排序分组多表就是编写sql语句的事情了
"""

# 连接MySQL数据库
db = pymysql.connect(host='localhost', user='root', password='123456', database='spidertestdb')
# 创建游标对象
cursor = db.cursor()
# 执行sql语句验证是否连接无误
cursor.execute('show databases')
databases = cursor.fetchall()
# print(databases)
# print(type(databases))

# TODO:创建表并插入数据
create_table_sql = """
CREATE TABLE IF NOT EXISTS novel_info (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    novel_name VARCHAR(50),
    novel_author VARCHAR(50),
    novel_desc TEXT
)
"""
cursor.execute(create_table_sql)

insert_sql = """
insert into novel_info values(null,"三国演义","罗贯中","这是一个三国的小说"),
                             (null,"西游记","吴承恩","这是一个西游的小说"),
                             (null,"水浒传","施耐庵","这是一部水浒的小说")
"""
# 必须try-expect，因为开启了事务，返回的是影响的行数
try:
    insert_count = cursor.execute(insert_sql)
    print(f"此次插入影响了{insert_count}行")
    db.commit()
except:
    db.rollback()

# TODO:查询数据，查询表中的所有数据，返回的是元组
query_sql = """select * from novel_info"""
cursor.execute(query_sql)
datas = cursor.fetchall()
print(f"目前数据库的所有数据为{datas}")

# TODO:修改数据，把西游记的作者修改成张狗蛋
update_sql = """update novel_info set novel_author='张狗蛋' where novel_name='西游记' """
update_count = cursor.execute(update_sql)
print(f"此次更改影响了{update_count}行")

# TODO:删除数据，删除三国演义这部小说
delete_sql = """delete from novel_info where novel_name='三国演义'"""
delete_count = cursor.execute(delete_sql)
print(f"此次删除影响了{delete_count}行")
