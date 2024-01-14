import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# 指定中文字体，使用 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']
# 为了正常显示负号
plt.rcParams['axes.unicode_minus'] = False


# 分析参与讨论的人们的ip分布
def draw_pie_with_ip(data):
    # 按IP分组并计数
    ip_counts = data['ip_label'].value_counts()

    # 选择前8个最常见的IP
    top_8_ips = ip_counts.head(8)

    # 计算“其他”类别的评论数
    total_comments = ip_counts.sum()  # 计算总的评论数
    top_8_sum = top_8_ips.sum()  # 计算前8个评论数
    other_count = total_comments - top_8_sum

    other_series = pd.Series({'其他': other_count})  # 创建包含“其他”类别的新Series

    all_ips = pd.concat([top_8_ips, other_series])  # 将“其他”类别的Series和前8个的IP合并

    # 绘制饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(all_ips, labels=all_ips.index, autopct='%1.1f%%', startangle=140)
    plt.title('评论分布的地域情况', fontsize=18)
    plt.show()


# 发布评论的时间分布
def draw_pie_with_time(data):
    # 确保 'create_time' 列中的值是数字，并且创建一个副本，不要让他报错以为我要修改原来的对象
    data_clean = data[pd.to_numeric(data['create_time'], errors='coerce').notna()].copy()

    # 将 'create_time' 列从 Unix 时间戳转换为 datetime 对象
    data_clean['create_time'] = pd.to_datetime(data_clean['create_time'].astype(int), unit='s')

    # 从 datetime 中提取日期
    data_clean['date'] = data_clean['create_time'].dt.date

    # 按日期分组并计算每天的评论数
    comments_per_day = data_clean['date'].value_counts().sort_index()

    # 为饼状图准备数据和标签
    pie_labels = [f"{date} ({count}人)" for date, count in comments_per_day.items()]

    # 绘制饼状图
    plt.figure(figsize=(8, 8))
    plt.pie(comments_per_day, labels=pie_labels, autopct='%1.1f%%', startangle=140)
    plt.title('日期的评论分布', fontsize=18)
    plt.show()


# 进行分词，绘制评论的词云图
def draw_word_cloud_with_comment(text):
    # print(text, type(text))
    joined_text = ' '.join(text)  # 转换成字符串
    # 使用jieba进行中文分词，并过滤掉单个字的词和一些不想要的词
    words = jieba.cut(joined_text)
    filtered_words = [word for word in words if
                      len(word) > 1 and word not in '不是 捂脸 黑龙江 河南 东北 我们 你们 什么']

    # 将过滤后的词用空格连接成一个字符串
    filtered_text = ' '.join(filtered_words)
    # 再次生成词云图
    wordcloud_cn = WordCloud(width=800, height=400, background_color='white',
                             font_path='simhei.ttf').generate(filtered_text)

    # 显示词云图
    plt.figure(figsize=(16, 10))
    plt.imshow(wordcloud_cn, interpolation='bilinear')
    plt.axis('off')
    plt.title('词云图分析', fontsize=50, y=1.1)
    plt.show()


# 简单的模式匹配，分析大家评论的倾向频率
def draw_bar_plot_with_comment(comments_df):
    # Define patterns for each category based on the provided criteria
    patterns = {
        1: r"支持河南考生移民|支持河南学生迁户口|赞成河南学生迁移",
        2: r"占用黑龙江考生名额|抢占黑龙江学生的机会|河南考生侵占黑龙江名额|抢教育资源",
        3: r"河南分数线太高|河南高考难|河南分数线高|分数线高",
        4: r"教育不平等|全国统一分数线|统一分数线|教育公平|统一录取率|统一试卷",
        5: r"复读生.*?多|复读生|复读|复读现象严重",
        6: r"河南大学少|河南高校不够多",
        7: r"黑龙江教育资源差|河南教育资源号|河南和黑龙江教育差距|教育资源差异|教育资源",
        8: r"河南人多|河南学生多|河南考生多|河南生的孩子多|人多",
        9: r"这就是河南人|河南人爱钻空子|地图炮",
        10: r"去年西安|之前西安|移民西安|西安",
        11: r"阴谋|国外分子"
    }

    # 判断当前这个评论属于什么分类
    def classify_comment(text):
        for category, pattern in patterns.items():
            if re.search(fr".*?{pattern}.*?", text):
                print(text, category)
                return category
        return 12  # 默认的原因

    # 对每个评论都进行分类
    comments_df['type'] = comments_df['text'].apply(classify_comment)
    print(len(comments_df['text']))

    # 计算分类的数量
    category_counts = comments_df['type'].value_counts().sort_index()

    # 排除分类11
    category_counts = category_counts[category_counts.index != 12]
    top_5_categories = category_counts.nlargest(5)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_5_categories.index.astype(str), top_5_categories.values, color='skyblue')

    # 添加每个柱子的个数标记
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom')

    plt.xlabel('分类')
    plt.ylabel('评论数量')
    plt.title('评论分类的前5个')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


if __name__ == '__main__':
    # 读取CSV文件
    file_path = './comments.csv'
    data = pd.read_csv(file_path)
    draw_pie_with_ip(data)  # 绘制ip分布的饼状图
    draw_pie_with_time(data)  # 绘制时间分布的饼状图
    draw_word_cloud_with_comment(data['text'].tolist())  # 绘制评论分布的词云图
    draw_bar_plot_with_comment(data)        # 绘制评论分布的柱状图
