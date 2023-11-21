import time
from datetime import datetime

import pymysql

# 这个类是用来把数据存储到Mysql数据库的
class MyDatabase:

    # 初始化数据库连接环境
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='123456', database='spidertestdb')
        self.cursor = self.db.cursor()
        self.create_table()

    # 这个数据库里面主要装爬取的所有数据，重复的也可以装
    def create_table(self):
        create_table_sql = """
              CREATE TABLE IF NOT EXISTS dailiantong_base (
                  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  Title VARCHAR(10000) comment '标题',
                  Price int comment '价格',
                  Ensure1 int comment '安全保证金',
                  Ensure2 int comment '效率保证金',
                  TimeLimit int comment '时间限制',
                  Creater VARCHAR(100) comment '发单人',
                  Stamp DATETIME comment '发布时间',
                  Zone VARCHAR(100) comment '游戏大区',
                  UnitPrice int comment '单价',
                  UserID VARCHAR(100) comment '发单人ID',
                  SerialNo VARCHAR(100) comment '订单ID'
              )
          """
        # 这个数据库主要装按照英雄分类的时候爬取到的数据
        create_table_sql2="""
         CREATE TABLE IF NOT EXISTS heroes_table(
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            hero VARCHAR(100) COMMENT '英雄名称',
            Title VARCHAR(10000) comment '标题',
            Price int comment '价格',
            Ensure1 int comment '安全保证金',
            Ensure2 int comment '效率保证金',
            TimeLimit int comment '时间限制',
            Creater VARCHAR(100) comment '发单人',
            Stamp DATETIME comment '发布时间',
            Zone VARCHAR(100) comment '游戏大区',
            UnitPrice int comment '单价',
            UserID VARCHAR(100) comment '发单人ID',
            SerialNo VARCHAR(100) comment '订单ID'
            
         ) 
        """
        self.cursor.execute(create_table_sql)
        self.cursor.execute(create_table_sql2)
        # 还有个表base_dailiantong用来装清洗过后的数据


    def save_data(self, datas):
        insert_sql = """
        INSERT INTO dailiantong_base (Title, Price, Ensure1, Ensure2, TimeLimit, Creater, Stamp, Zone, UnitPrice,UserID,SerialNo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
        """
        try:
            for data in datas["LevelOrderList"]:
                values = (
                    data.get("Title", ""),
                    data.get("Price", 0),
                    data.get("Ensure1", 0),
                    data.get("Ensure2", 0),
                    data.get("TimeLimit", 0),
                    data.get("Create", ""),
                    datetime.fromtimestamp(data.get("Stamp", int(time.time())) + 255845872).strftime(
                        '%Y-%m-%d %H:%M:%S'),
                    data.get("Zone", ""),
                    data.get("UnitPrice", 0),
                    data.get("UserID", ""),
                    data.get("SerialNo", "")
                )
                self.cursor.execute(insert_sql, values)
            self.db.commit()
        except Exception as e:
            print("插入数据时候出错了:", e)
            self.db.rollback()

    # 把英雄数据保存到数据库中
    def save_heroes_data(self, datas,search_str):
        insert_sql = """
                INSERT INTO heroes_table (hero,Title, Price, Ensure1, Ensure2, TimeLimit, Creater, Stamp, Zone, UnitPrice,UserID,SerialNo)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
                """
        try:
            for data in datas["LevelOrderList"]:
                values = (
                    search_str,
                    data.get("Title", ""),
                    data.get("Price", 0),
                    data.get("Ensure1", 0),
                    data.get("Ensure2", 0),
                    data.get("TimeLimit", 0),
                    data.get("Create", ""),
                    datetime.fromtimestamp(data.get("Stamp", int(time.time())) + 255845872).strftime(
                        '%Y-%m-%d %H:%M:%S'),
                    data.get("Zone", ""),
                    data.get("UnitPrice", 0),
                    data.get("UserID", ""),
                    data.get("SerialNo", "")
                )
                self.cursor.execute(insert_sql, values)
            self.db.commit()
        except Exception as e:
            print("插入数据时候出错了:", e)
            self.db.rollback()

    # 关闭数据库连接
    def close(self):
        self.cursor.close()
        self.db.close()
