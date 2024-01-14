import matplotlib.pyplot as plt
import numpy as np

# 指定中文字体，使用 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']
# 为了正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 河南和黑龙江的数据
henan_data = [{'2023年': ['批次\n文科\n理科', '本科一批\n547\n514', '本科二批\n465\n409', '高职专科批\n185\n185',
                          '查看详情\n查看详情']}, {
                  '2022年': ['批次\n文科\n理科', '本科一批\n527\n509', '本科二批\n445\n405', '高职专科批\n190\n190',
                             '查看更多\n查看更多']}, {
                  '2021年': ['批次\n文科\n理科', '一本\n558\n518', '二本\n466\n400', '高职高专\n200\n200',
                             '艺术类\n点击查看\n点击查看', '体育类\n点击查看\n点击查看']},
              {'2020年': ['批次\n文科\n理科', '一本\n556\n544', '二本\n465\n418', '高职高专\n180\n180']},
              {'2019年': ['批次\n文科\n理科', '一批\n536\n502', '二批\n447\n385', '专科\n160\n160']},
              {'2018年': ['批次\n文科\n理科', '一批\n547\n499', '二批\n436\n374', '专科\n200\n200']}]
hlj_data = [{'2023年': ['批次\n文科\n理科', '本科一批\n430\n408', '本科二批\n341\n287', '高职（专科）\n160\n160',
                        '查看详情\n查看详情']}, {
                '2022年': ['批次\n文科\n理科', '本科一批\n463\n429', '本科二批\n365\n308', '高职（专科）\n160\n160',
                           '查看更多\n查看更多']}, {
                '2021年': ['批次\n文科\n理科', '本科一批\n472\n415', '本科二批\n354\n280', '高职专科\n160\n160',
                           '艺术体育类\n点击查看\n点击查看']}, {
                '2020年': ['批次\n文科\n理科', '本科一批\n483\n455', '本科二批\n356\n301', '高职专科\n160\n160',
                           '艺术体育类\n点击查看\n点击查看']}, {
                '2019年': ['批次\n文科\n理科', '一批\n500\n477', '二批\n424\n372', '艺术类本科\n254\n236',
                           '体育类本科\n254\n223', '本科三批\n348\n324', '高职专科\n160\n160']}, {
                '2018年': ['批次\n文科\n理科', '一批\n490\n472', '二批\n406\n353', '高职\n160\n160', '艺术类本科\n-\n-',
                           '体育类本科\n-\n-']}]


# 解析数据的函数
def parse_scores(data):
    scores = {'本科一批': {'文科': [], '理科': []}, '本科二批': {'文科': [], '理科': []}}
    for entry in data:
        # print(entry)
        year_scores = list(entry.values())[0]
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


# 绘制组合条形图的函数
def plot_combined_bar_chart(henan_score, hlj_score, title):
    print(henan_score)
    print(hlj_score)
    years = ['2018年', '2019年', '2020年', '2021年', '2022年', '2023年']
    bar_width = 0.15
    index = np.arange(len(years))

    fig, ax = plt.subplots(figsize=(18, 10))

    # 画henan的本科一批和hlj本科一批
    ax.bar(index - bar_width, henan_score['本科一批']['理科'][::-1], bar_width, label='河南本科一批')
    ax.bar(index, hlj_score['本科一批']['理科'][::-1], bar_width, label='黑龙江本科一批')

    # 画henan的本科二批和hlj二批
    ax.bar(index + 1.5 * bar_width, henan_score['本科二批']['理科'][::-1], bar_width, label='河南本科二批')
    ax.bar(index + 2.5 * bar_width, hlj_score['本科二批']['理科'][::-1], bar_width, label='黑龙江本科二批')

    # 添加文字标注
    for i in index:
        # 河南本科一批
        henan_one = henan_score['本科一批']['理科'][::-1][i]
        ax.text(i - bar_width, henan_one + 1, henan_one, ha='center', va='bottom')

        # 黑龙江本科一批
        hlj_one = hlj_score['本科一批']['理科'][::-1][i]
        ax.text(i, hlj_one + 1, hlj_one, ha='center', va='bottom')

        # 河南本科二批
        henan_two = henan_score['本科二批']['理科'][::-1][i]
        ax.text(i + 1.5 * bar_width, henan_two + 1, henan_two, ha='center', va='bottom')

        # 黑龙江本科二批
        hlj_two = hlj_score['本科二批']['理科'][::-1][i]
        ax.text(i + 2.5 * bar_width, hlj_two + 1, hlj_two, ha='center', va='bottom')

    ax.set_xlabel('年份')
    ax.set_ylabel('分数')
    ax.set_title(title)
    ax.set_xticks(index + bar_width * 0.75)
    ax.set_xticklabels(years)
    ax.legend()

    plt.show()


# 解析并翻转数据
henan_scores = parse_scores(henan_data)
hlj_scores = parse_scores(hlj_data)

# 绘制理科的组合条形图
plot_combined_bar_chart(henan_scores, hlj_scores, '理科本科一批和本科二批分数线对比')
