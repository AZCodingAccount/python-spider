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

    # 这个数据库里面主要装爬取的所有评论数据
    def create_table(self):
        create_table_sql = """
              CREATE TABLE IF NOT EXISTS tiktok_comments (
                  id BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  aweme_id BIGINT COMMENT  '视频id',
                  cid BIGINT comment '评论id',
                  comment_text text comment '评论内容',
                  digg_count int comment '点赞数',
                  reply_comment_total int comment '回应的评论数',
                  nickname varchar(100) comment '昵称',
                  ip_label VARCHAR(100) comment 'ip属地',
                  create_time datetime comment '评论发送时间'
              )
          """
        self.cursor.execute(create_table_sql)

    def save_data(self, datas):
        insert_sql = """
        INSERT INTO tiktok_comments (cid, aweme_id,comment_text, digg_count, reply_comment_total, nickname, ip_label, create_time)
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            for data in datas:
                values = (
                    data.get("cid", ""),
                    data.get('aweme_id', ""),
                    data.get("text", 0),
                    data.get("digg_count", 0),
                    data.get("reply_comment_total", 0),
                    data.get("nickname", 0),
                    data.get("ip_label", ""),
                    datetime.fromtimestamp(data.get("create_time", int(time.time()))).strftime(
                        '%Y-%m-%d %H:%M:%S'),
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
