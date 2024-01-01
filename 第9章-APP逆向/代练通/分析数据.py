import re

import pandas as pd
import seaborn as sns
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


def ana_heros():
    # 使用 Pandas 读取数据
    query = "SELECT * FROM heroes_table;"
    heros_df = pd.read_sql(query, engine)
    # 排除 'id' 列，基于所有其他列去重
    heros_df = heros_df.drop_duplicates(subset=[col for col in df.columns if col != 'id'])
    print(f"英雄总数据集共{len(heros_df)}个")
    print("-------------------------------------------------------------------")
    # 这个我们只分析最受欢迎的10个英雄和10个平均价格最高的英雄
    # 分析最受欢迎的英雄（出现频率最高的10个英雄）
    popular_heroes = heros_df['hero'].value_counts().head(10)

    # 计算每个英雄的平均价格
    avg_price_per_hero = round(heros_df.groupby('hero')['Price'].mean(), 1)

    # 找出平均价格最高的10个英雄
    highest_avg_price_heroes = avg_price_per_hero.sort_values(ascending=False).head(10)

    # 绘制最受欢迎的英雄的柱状图
    ax = popular_heroes.plot(kind='bar', color='skyblue', rot=0, figsize=(12, 6))
    # 设置横坐标标签横向显示
    plt.xticks(rotation='horizontal')
    plt.ylabel('频次', rotation=360, labelpad=20)

    for p in ax.patches:  # ax.patches 是所有柱子的列表
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.title('最受欢迎的10个英雄')
    plt.xlabel('英雄')
    plt.ylabel('频次')
    plt.ylim(0, 330)
    plt.show()

    # 绘制平均价格最高的英雄的柱状图
    ax = highest_avg_price_heroes.plot(kind='bar', color='skyblue', rot=0, figsize=(12, 8))
    # 设置横坐标标签横向显示
    plt.xticks(rotation='horizontal')
    plt.ylabel('价格', rotation=360, labelpad=20)
    plt.ylim(0, 490)
    for p in ax.patches:  # ax.patches 是所有柱子的列表
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    plt.title('每单平均价格最高的10个英雄')
    plt.xlabel('英雄')
    plt.ylabel('价格')
    plt.show()


# 排除 'id' 列，基于所有其他列去重
df = df.drop_duplicates(subset=[col for col in df.columns if col != 'id'])

# 打印数据集的长度，即去重后的条目数
print(f"总数据集共{len(df)}个")

# 对数据进行简单的描述性统计，包括单价，安全效率保证金，时间限制。
# TODO:绘制四分位图。
describe = df[['Price', 'Ensure1', 'Ensure2', 'TimeLimit']].describe()


# 分析创建者发了多少单
def get_creater_count():
    # 把这个根据Creater分组，看看发单的究竟是哪些人？
    # TODO:前多少的人发了多少单
    percentages = [0.1, 0.5, 1, 5, 10, 20, 30, 40, 50]  # 百分比列表
    total_order_count = len(df)
    grouped_creaters = df.groupby('Creater').size().sort_values(ascending=False)  # 获取发单人发了多少单
    total_creater_count = len(grouped_creaters)  # 获取总的发单人个数

    # 计算发单人群体的百分比贡献
    creater_counts_list = [int(total_creater_count * p / 100) for p in percentages]  # 计算相应百分比的发单人数
    creater_counts_list = [max(count, 1) for count in creater_counts_list]  # 确保至少有1个人
    # 计算发单人的相应百分比对一个发单数的百分比
    # 下面代码的逻辑是首先获取0.1%、0.5%......所对应的发单人人数，然后求出这些人发单总数的和/总的发单数就是他们所占的比例
    orders_percentages_creaters = [grouped_creaters.head(count).sum() / total_order_count * 100 for count in
                                   creater_counts_list]

    # 创建图表
    plt.figure(figsize=(10, 6))
    plt.bar([f'Top {p}%' for p in percentages], orders_percentages_creaters, color='skyblue')
    plt.xlabel('发单者的比例')
    plt.ylabel('总订单的比例')
    plt.title('计算发单者与订单数的相关关系')
    plt.grid(axis='y')

    # 在每个条形上显示百分比
    for i, value in enumerate(orders_percentages_creaters):
        plt.text(i, value + 0.5, f'{value:.2f}%', ha='center')

    # 显示图表
    plt.show()


def analyze_zone():
    # 根据Zone分组，看看四大区的订单量
    grouped_zones = df.groupby('Zone').size().sort_values(ascending=False)
    grouped_zones = grouped_zones.drop('苹果微信')
    # print(grouped_zones)

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


# 绘制描述性统计图表，不包括最大值和最小值，使用柔和的配色方案
def describe_stat(stats):
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    ax = ax.ravel()  # 降维成一维数组
    colors = ['lightblue', 'lightcoral', 'lightgreen']  # 定义配色

    for i, (key, value) in enumerate(stats.items()):
        # 绘制柱状图
        ax[i].bar('平均值', value['mean'], color=colors[0], label='平均值')
        ax[i].bar('标准差', value['std'], color=colors[1], label='标准差')
        # 绘制折线图
        ax[i].plot(['25%', '50%', '75%'],
                   [value['25%'], value['50%'], value['75%']],
                   color=colors[2], label='四分位数', zorder=3)
        # 绘制散点图
        ax[i].scatter(['25%', '50%', '75%'],
                      [value['25%'], value['50%'], value['75%']],
                      color='black', zorder=4)
        # 加上数值标记
        for j, percentile in enumerate(['25%', '50%', '75%']):
            ax[i].annotate(f"{value[percentile]:.0f}",
                           (percentile, value[percentile]),
                           textcoords="offset points",
                           xytext=(0, 10),
                           ha='center')
        if key == 'Price':
            ax[i].set_title("价格")
        elif key == 'Ensure1':
            ax[i].set_title("安全保证金")
        elif key == 'Ensure2':
            ax[i].set_title("效率保证金")
        elif key == 'TimeLimit':
            ax[i].set_title("时间限制")
        ax[i].legend()

    plt.tight_layout()
    plt.show()


starlight_count = king_count = peak_competition_count = 0  # 记录提取的个数

# 每个提取的个数
s1 = k1 = k2 = k3 = k4 = p0 = p1 = p2 = p3 = p4 = p5 = 0
# 1-25星。26-50星。51-75星。76以上
starlight_avg_price = [0] * 20000
king1_avg_price = [0] * 20000
king2_avg_price = [0] * 20000
king3_avg_price = [0] * 20000
king4_avg_price = [0] * 20000  # 记录单价
# 1200-1500  1500-1800  1800-2100   2100-2200   2200-2300   2300以上
peak_competition_avg_price0 = [0] * 20000
peak_competition_avg_price1 = [0] * 20000
peak_competition_avg_price2 = [0] * 20000
peak_competition_avg_price3 = [0] * 20000
peak_competition_avg_price4 = [0] * 20000
peak_competition_avg_price5 = [0] * 20000


def extract_price(index, title, price):
    global starlight_count, king_count, peak_competition_count
    global starlight_avg_price, king1_avg_price, peak_competition_avg_price0, king2_avg_price, king3_avg_price, king4_avg_price
    global peak_competition_avg_price1, peak_competition_avg_price2, peak_competition_avg_price3, peak_competition_avg_price4, peak_competition_avg_price5
    global s1, k1, k2, k3, k4, p0, p1, p2, p3, p4, p5

    # 对这些数据进行正则匹配，先考虑官方的
    if re.match(r'^.?.?星耀', title) and re.match(r'^.?.?星耀\d.?\d.*', title) and not (
            "有实力的可以看下方订单说明" in title):  # 把这个情况2给过滤了，还有这种 星耀2四星到25星 铭文150级
        # 这里需要定义规则了，星耀一般标题是1：星耀4 4星-王者1星。2：扫码星耀5-王者1星  铭文全满。3：星耀2/3星-最强王者6星 铭文150
        # 对于每种规则都需要考虑到，这里简单一点，如果说你是星耀，那我就直接把单价给你。如果说你是王者，王者不超过1颗星的还是星耀。超过1颗星的就是计算到王者里面
        starlight_count += 1
        # 如果说都是星耀的情况，筛选脏数据
        if re.match(r'.*?星耀.*?星耀.*', title):
            s1 += 1
            count_list = re.findall('\d', title)
            count_list = [int(count) for count in count_list]  # 转换成整数
            # 接下来就是计算星数了
            if (len(count_list) < 4):  # 有的还不写星数
                return
            # print(count_list,title)
            star_count = (count_list[0] - count_list[2]) * 5 + count_list[3] - count_list[1]  # 计算总星数
            starlight_avg_price[index] = price / star_count  # 把这个平均值记录下来
            # print(star_count, price, title, starlight_avg_price)
        elif re.match(r'.*?星耀.*?王者.*', title):
            count_list = re.findall(r'(0|[1-9][0-9]?|100)', title)
            count_list = [int(count) for count in count_list]  # 转换成整数
            if (len(count_list) < 3 or count_list[0] > 5):
                return
            if count_list[2] == 1:  # 如果说星耀到王者一星
                s1 += 1
                star_count = count_list[0] * 5 + 1 - count_list[1]  # 计算总星数
                starlight_avg_price[index] = price / star_count  # 把这个平均值记录下来
                # print(star_count, title, starlight_avg_price[index])
            elif count_list[2]:  # 星耀到王者很多星,统一都加到1-26星这里了
                k1 += 1
                star_count = count_list[0] * 5 + count_list[2] - count_list[1]  # 计算总星数 -1+1 约了
                king1_avg_price[index] = price / star_count  # 把这个平均值记录下来
                # print(star_count, title, king2_avg_price[index])
    elif re.match(r'^.?.?王者.*?王者.*', title):  # 王者-王者
        # 这个提取就简单了，提取前两个。0-200
        count_list = re.findall(r'(?<!\d)(0|[1-9]|[1-9]\d|1[0-9]\d|200)(?!\d)', title)
        count_list = [int(count) for count in count_list]  # 转换成整数
        if (len(count_list) < 2):
            return
        # print(count_list, title)
        # 根据上面分的4种类型
        star_count = count_list[1] - count_list[0]
        if count_list[1] < 26:
            k1 += 1
            king1_avg_price[index] = price / star_count
        elif count_list[0] >= 26 and count_list[1] < 51:
            k2 += 1
            king2_avg_price[index] = price / star_count
        elif count_list[0] >= 51 and count_list[1] < 76:
            # print(title, count_list, count_list[1])
            k3 += 1
            king3_avg_price[index] = price / star_count
        elif count_list[0] >= 76:
            k4 += 1
            king4_avg_price[index] = price / star_count
        king_count += 1
    elif re.match(r'^.?.?巅峰赛', title):
        peak_competition_count += 1
        count_list = re.findall(r'(?<!\d)(1\d{3}|2[0-6]\d{2}|2700)(?!\d)', title)
        count_list = [int(count) for count in count_list]  # 转换成整数
        if len(count_list) < 2:
            return
        score_count = count_list[1] - count_list[0]
        if score_count < 0: return
        # 根据不同的分数定义不同的分段
        if count_list[1] <= 1500:
            p0 += 1
            peak_competition_avg_price0[index] = price / score_count
            # print(title, count_list, peak_competition_avg_price0[index])
        elif count_list[0] > 1500 and count_list[1] <= 1800:
            p1 += 1
            peak_competition_avg_price1[index] = price / score_count
            # print(title, count_list, peak_competition_avg_price1[index])
        elif count_list[0] > 1800 and count_list[1] <= 2100:
            p2 += 1
            peak_competition_avg_price2[index] = price / score_count
        elif count_list[0] > 2100 and count_list[1] <= 2200:
            p3 += 1
            peak_competition_avg_price3[index] = price / score_count
        elif count_list[0] > 2200 and count_list[1] <= 2300:  # 从哪开始的已经无所谓了
            p4 += 1
            peak_competition_avg_price4[index] = price / score_count
            # print(title, count_list, peak_competition_avg_price4[index])
        elif count_list[0] > 2300:
            p5 += 1
            peak_competition_avg_price5[index] = price / score_count
            # print(title, count_list, peak_competition_avg_price5[index])
        # print(count_list, title)


def cal_price_and_print():
    # 对数据进行单价的计算，计算的仅仅是前几个字符里面有段位，如王者、星耀、砖石、铂金、青铜等。使用正则匹配匹配目前的星数。如果匹配不上就跳过这个数据
    # 类似于巅峰赛，战力。这里我们只匹配官方的哈，标准的数据，不匹配那些乱七八糟的。
    # TODO:画一个柱状图。描述性统计
    # df['Title', 'Price'].apply(extract_price)
    # 计算平均价格
    for index, row in df.iterrows():
        # print(index, row['Title'], row['Price'])
        extract_price(index, row['Title'], row['Price'])

    # 之前定义了一些数组，这些数组里面存储的只要不是0，就是我们给他赋的值
    def cal_avg_price(lst):
        non_zero_elements = [elem for elem in lst if elem != 0]
        if non_zero_elements:
            return round(sum(non_zero_elements) / len(non_zero_elements), 2)
        else:
            return 0

    # 计算每个列表的非零平均值
    starlight_avg = cal_avg_price(starlight_avg_price)

    # 计算排位的
    king1_avg = cal_avg_price(king1_avg_price)
    king2_avg = cal_avg_price(king2_avg_price)
    king3_avg = cal_avg_price(king3_avg_price)
    king4_avg = cal_avg_price(king4_avg_price)

    # 计算巅峰赛的
    peak_competition_avg0 = cal_avg_price(peak_competition_avg_price0)
    peak_competition_avg1 = cal_avg_price(peak_competition_avg_price1)
    peak_competition_avg2 = cal_avg_price(peak_competition_avg_price2)
    peak_competition_avg3 = cal_avg_price(peak_competition_avg_price3)
    peak_competition_avg4 = cal_avg_price(peak_competition_avg_price4)
    peak_competition_avg5 = cal_avg_price(peak_competition_avg_price5)

    print(f"星耀平均价格为{starlight_avg}元，样本数为{s1}")
    print("-------------------------------------------------------------------")
    print(f"1-26星平均价格为{king1_avg}元,样本数为{k1}")
    print(f"26-51星平均价格为{king2_avg}元,样本数为{k2}")
    print(f"51-76星平均价格为{king3_avg}元,样本数为{k3}")
    print(f"76星以上平均价格为{king4_avg}元,样本数为{k4}")
    print("-------------------------------------------------------------------")
    print(f"1200-1500巅峰赛每分价格为{peak_competition_avg0}元,样本数为{p0}")
    print(f"1500-1800巅峰赛每分价格为{peak_competition_avg1}元,样本数为{p1}")
    print(f"1800-2100巅峰赛每分价格为{peak_competition_avg2}元,样本数为{p2}")
    print(f"2100-2200巅峰赛每分价格为{peak_competition_avg3}元,样本数为{p3}")
    print(f"2200-2300巅峰赛每分价格为{peak_competition_avg4}元,样本数为{p4}")
    print(f"2300以上巅峰赛每分价格为{peak_competition_avg5}元,样本数为{p5}")
    print("-------------------------------------------------------------------")
    print(
        f"星耀类单子统计数为{starlight_count}个，王者类单子统计数为{king_count}个，巅峰赛类单子统计数为{peak_competition_count}个")


ana_heros()
analyze_zone()
get_creater_count()
# 绘制不包括最大值和最小值的描述性统计图表，使用柔和的配色
describe_stat(describe)
cal_price_and_print()

# # 写入到mysql数据库和excel表格
# df.to_excel('./data.xlsx', index=False)
# df.to_sql('drop_duplicates_data', engine, schema='spidertestdb', if_exists='replace')
