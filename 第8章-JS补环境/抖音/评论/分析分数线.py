import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt

# 指定中文字体，使用 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']
# 为了正常显示负号
plt.rcParams['axes.unicode_minus'] = False

"""
    抖音分析评论涉及到NLP和LDA，这里简单分析一下。从下面这几个维度分析
    1：根据ip归属地聚类，看看是哪些省的更关注这些问题
    2: 词云图，哪些词最关键
    # 这个其实也不太准确，GPT4还是不够本土化，有的完全看不出来是冷嘲热讽的，还是用模式匹配吧。
    3：调用AI大模型接口，让他帮我们分析这个评论是什么方向。
        1：支持河南考生移民
        2：认为不能抢占黑龙江考生名额

        3：认为河南高考分数太高
        4：认为教育不平等，支持全国统一分数线
        5：认为复读生太多
        6: 认为河南大学少
        7：认为两者教育资源有差距

        8：认为河南生的多
        9：攻击河南人

        10：认为有人搞阴谋论，抹黑黑龙江和河南
        11:其他原因

    至于对分数线的分析就比较简单了。分析分数线最高的4个省和分数线最低的4个省，但是这又衍生出来一个问题，每年没准这8个省不固定呢？那每一年都要画吗？
    事实证明，也不用，因为分数线最高基本也是每一年分数线都是最高，也不可能出现飞上枝头当凤凰这样的出现，所以我取的是平均值

    因此分析结果就可以出来了，就分析本科一批（一批），本科二批（二批）这两类数据，京津沪这些教育改革的快，基本好久都没有本科一二批了，现在好多省份也是新高考，
主选历史和地理那种，这里也不进行分析了。

    筛选完成之后得到15个省份，这里其实还需要考虑全国1卷、2卷、3卷。但是一般用2卷和3卷的分数线近几年也相对比较低，这里就直接跟1卷的一起比了。
    分析完成之后再单独分析一下黑龙江和河南。
"""


# 筛选出那些不是一本二本招生的
def filter_province():
    list1 = []
    for doc in total_list:
        dict1 = {}
        # print(doc, type(doc))
        # 开始筛选，首先是第一轮筛选，筛选出没有本科一批......这些数据
        isContainsDirChar = False
        isDirProvince = True
        for data in doc['data']:
            # data，许多年的数据
            for key, values in data.items():
                # print(key, values)  # 2023:[2023的数据]
                for value in values:  # 遍历每一年的
                    # 使用普通字符串筛选就行
                    if '\n' in value and (
                            '本科一批' == value.split('\n')[0] or '一批' == value.split('\n')[0] or '本科一段' ==
                            value.split('\n')[0]
                            or '本科二批' == value.split('\n')[0] or '本科二段' == value.split('\n')[0] or '二批' ==
                            value.split('\n')[0]):
                        isContainsDirChar = True  # 标记这次通过了
                    if isContainsDirChar:  # 其实这里还有第一批，但是23年都是一本二本的，前几年肯定也是这个制度，直接break
                        break
                if not isContainsDirChar:  # 表明某一年不是一本或二本招生，这个省份直接排除
                    isDirProvince = False
                if not isDirProvince:  # 已经不是符合要求的省份了，没必要再遍历其他年
                    break
            if not isDirProvince:
                break
        if isDirProvince:  # 经过了重重考验，符合条件的省份
            dict1['city'] = doc['city']
            print(dict1['city'], end='、')
            dict1['data'] = doc['data']
            list1.append(dict1)
    return list1


# 绘制过滤完成的所有省份的折线图
def plot_line_chart(datas_y, front_regions, end_regions, title):
    data_x = ['2018年', '2019年', '2020年', '2021年', '2022年', '2023年']

    plt.figure(figsize=(12, 8))
    # 画前4名和后4名
    for region, _ in front_regions + end_regions:
        scores = datas_y[region][::-1]
        plt.plot(data_x, scores, marker='o', label=region)
        # 添加数值标记
        for x, y in zip(data_x, scores):
            plt.text(x, y * 1.002, y, va='bottom', fontsize=10)
    plt.title(title, fontsize=14)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('分数', rotation=360, labelpad=20, fontsize=12)
    # 移动图例到图表外面
    plt.legend(loc='upper left', bbox_to_anchor=(-0.15, 1))

    plt.show()


# 画前四个和后四个，文科本一、文科本二、理科本一、理科本二。
# @params string batch_type:标识是一批还是二批，一为一批、二为二批
# @params int  subject_type：标识是文科还是理科，文科1理科2
def draw_all_scoreline(batch_type, subject_type):
    provinces = []  # 存储所有省份
    datas_y = {}
    for province in list1:
        data_y = []  # 存储每个城市的本科数据的列表
        provinces.append(province['city'])
        for data in province['data']:
            for key, values in data.items():
                for value in values:
                    if ('\n' in value) and (
                            value.split('\n')[0] == f'本科{batch_type}批'
                            or value.split('\n')[0] == f'{batch_type}批'
                            or value.split('\n')[0] == f'第{batch_type}批'
                            or value.split('\n')[0] == f'{batch_type}本'
                            or value.split('\n')[0] == f'本科{batch_type}段'
                            or value.split('\n')[0] == f'汉语言本科{batch_type}批'):
                        data_y.append(int(value.split('\n')[subject_type].replace('分', "")))  # 取的是文科
        datas_y[province['city']] = data_y  # 把每个省的信息存一下，等下要排名

    # 计算每个地区的平均分数
    average_scores = {region: np.mean(scores) for region, scores in datas_y.items()}

    # 根据平均分数排序
    sorted_regions = sorted(average_scores.items(), key=lambda x: x[1])

    # 选择排名前4的和排名后4的
    top_5_regions = sorted_regions[-4:]
    bottom_5_regions = sorted_regions[:4]

    # 这个处理之后是一个列表包含元组，这点要注意 [('河南', 545.1666666666666), ('江西', 549.0), ('贵州', 552.5), ('云南', 560.0)]

    plot_line_chart(datas_y, top_5_regions, bottom_5_regions, f"{'文科' if subject_type == 1 else '理科'}"
                                                              f"{'一本' if batch_type == '一' else '二本'}分数线排名前四和排名后四的省份")


# 解析数据的函数，解析成组合条形图可以识别的数据格式
def parse_scores(data):
    scores = {'本科一批': {'文科': [], '理科': []}, '本科二批': {'文科': [], '理科': []}}
    for entry in data:
        # print(entry.values())
        year_scores = (list(entry.values()))[0]
        # ['批次\n文科\n理科', '本科一批\n547\n514', '本科二批\n465\n409', '高职专科批\n185\n185', '查看详情\n查看详情']
        for score in year_scores:
            # print(score)
            parts = score.split('\n')
            if '本科一批' in parts[0] or '一本' in parts[0] or '一批' in parts[0]:
                scores['本科一批']['文科'].append(int(parts[1]))
                scores['本科一批']['理科'].append(int(parts[2]))
            elif '本科二批' in parts[0] or '二本' in parts[0] or '二批' in parts[0]:
                scores['本科二批']['文科'].append(int(parts[1]))
                scores['本科二批']['理科'].append(int(parts[2]))
    return scores


# 绘制两个组合条形图的函数
# @params type 标识要绘制的是文科还是理科的组合条形图 1文科，2理科
def plot_combined_bar_chart(henan_score, hlj_score, title, type):
    years = ['2018年', '2019年', '2020年', '2021年', '2022年', '2023年']
    bar_width = 0.15
    index = np.arange(len(years))

    fig, ax = plt.subplots(figsize=(18, 10))
    subject = '文科' if type == 1 else '理科'

    # 画henan的本科一批和hlj本科一批
    ax.bar(index - bar_width, henan_score['本科一批'][subject][::-1], bar_width, label='河南本科一批')
    ax.bar(index, hlj_score['本科一批'][subject][::-1], bar_width, label='黑龙江本科一批')

    # 画henan的本科二批和hlj二批
    ax.bar(index + 1.5 * bar_width, henan_score['本科二批'][subject][::-1], bar_width, label='河南本科二批')
    ax.bar(index + 2.5 * bar_width, hlj_score['本科二批'][subject][::-1], bar_width, label='黑龙江本科二批')

    # 添加文字标注
    for i in index:
        # 河南本科一批
        henan_one = henan_score['本科一批'][subject][::-1][i]
        ax.text(i - bar_width, henan_one + 1, str(henan_one) + "分", ha='center', va='bottom', fontsize=10)

        # 黑龙江本科一批
        hlj_one = hlj_score['本科一批'][subject][::-1][i]
        ax.text(i, hlj_one + 1, str(hlj_one) + "分", ha='center', va='bottom', fontsize=10)

        # 河南本科二批
        henan_two = henan_score['本科二批'][subject][::-1][i]
        ax.text(i + 1.5 * bar_width, henan_two + 1, str(henan_two) + "分", ha='center', va='bottom', fontsize=10)

        # 黑龙江本科二批
        hlj_two = hlj_score['本科二批'][subject][::-1][i]
        ax.text(i + 2.5 * bar_width, hlj_two + 1, str(hlj_two) + "分", ha='center', va='bottom', fontsize=10)

    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('分数', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xticks(index + bar_width * 0.75)
    ax.set_xticklabels(years)
    ax.legend()

    plt.show()


# 分析河南和黑龙江两个省份
def analysis_certain_province():
    henan_data = []
    hlj_data = []
    # 获取详细数据
    for province in list1:
        # 注意，这里的data是一个数组包对象的形式
        if province['city'] == '河南':
            henan_data = province['data']
        elif province['city'] == '黑龙江':
            hlj_data = province['data']
    print(henan_data)
    # 解析并翻转数据
    henan_scores = parse_scores(henan_data)
    hlj_scores = parse_scores(hlj_data)

    # 绘制文科的组合条形图
    plot_combined_bar_chart(henan_scores, hlj_scores, '文科两省一本和二本分数线对比', 1)
    # 绘制理科的组合条形图
    plot_combined_bar_chart(henan_scores, hlj_scores, '理科两省本科一批和二本分数线对比', 2)


if __name__ == '__main__':
    # 创建连接
    conn = MongoClient(host="localhost", port=27017)
    collection = conn.test.scoreline

    # 读取数据，不查id
    total_list = collection.find({}, {"_id": 0})  # 不要用关键字命名，找了10分钟才找出来list问题
    list1 = filter_province()
    # # 分别画四个图，对整体的分数线有个大概的认识
    draw_all_scoreline("一", 1)
    draw_all_scoreline("一", 2)
    draw_all_scoreline("二", 1)
    draw_all_scoreline("二", 2)
    # 请出主角，河南和黑龙江的详细对比，绘制组合条形图
    analysis_certain_province()
