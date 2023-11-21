import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
"""
    这里数据分析一下代练订单的一些信息，暂定：
            1：发单大区
            2：发单人（10%的发单人发了90%的订单？）
            3：对单价，效率保证金，安全保证金进行简单的描述性统计（并无太大参考价值）
            4：对每个分段求一个平均值：如王者一星平均多少，星耀一星平均多少。巅峰赛一分多少——使用正则匹配
"""


# 指定中文字体，使用 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']
# 为了正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 使用 SQLAlchemy 创建数据库引擎
engine = create_engine('mysql+pymysql://root:123456@localhost/spidertestdb')

# 使用 Pandas 读取数据
query = "SELECT * FROM dailiantong_base;"
df = pd.read_sql(query, engine)

# 排除 'id' 列，基于所有其他列去重
df = df.drop_duplicates(subset=[col for col in df.columns if col != 'id'])

# 打印数据集的长度，即去重后的条目数
print(len(df))

# 把这个根据Creater分组，看看发单的究竟是哪些人？
# TODO:前多少的人发了多少单
grouped_creaters = df.groupby('Creater').size().sort_values(ascending=False)
print(grouped_creaters)


def analyze_zone():
    # 根据Zone分组，看看四大区的订单量
    grouped_zones = df.groupby('Zone').size().sort_values(ascending=False)
    grouped_zones = grouped_zones.drop('苹果微信')
    print(grouped_zones)

    # 将分组后的数据转换为DataFrame，为了饼状图的绘制
    zone_df = pd.DataFrame(grouped_zones).reset_index()
    zone_df.columns = ['Zone', 'Counts']

    # 自定义 autopct 函数
    def custom_autopct(pct):
        total = sum(zone_df['Counts'])
        count = int(round(pct * total / 100.0))
        return '{:.1f}%\n({:d} 单)'.format(pct, count)
    # 选择颜色主题
    colors = plt.cm.Paired(range(len(zone_df)))
    # 生成饼状图
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(zone_df['Counts'], labels=zone_df['Zone'], autopct=custom_autopct,
                                       startangle=140, colors=colors, shadow=True,
                                       explode=[0.1 if i == 0 else 0 for i in range(len(zone_df))])
    # 美化标签
    plt.setp(texts, size=12)
    plt.setp(autotexts, size=12, weight="bold", color="white")
    # 设置标题
    plt.title('游戏大区分布饼状图', fontsize=16)
    # 显示图例
    plt.legend(zone_df['Zone'], title="大区", loc="best")
    # 显示图表
    plt.axis('equal')
    plt.show()


analyze_zone()

# 对数据进行简单的描述性统计，包括单价，安全效率保证金，时间限制。
# TODO:绘制四分位图。
describe = df[['Price', 'Ensure1', 'Ensure2', 'TimeLimit']].describe()
print(describe)

# 对数据进行单价的计算，计算的仅仅是前几个字符里面有段位，如王者、星耀、砖石、铂金、青铜等。使用正则匹配匹配目前的星数。如果匹配不上就跳过这个数据
# 类似于巅峰赛，战力
# TODO:画一个柱状图。描述性统计

# 写入到mysql数据库和excel表格
df.to_excel('./data.xlsx',index=False)
df.to_sql('base_dailiantong',engine, schema='spidertestdb', if_exists='replace')

