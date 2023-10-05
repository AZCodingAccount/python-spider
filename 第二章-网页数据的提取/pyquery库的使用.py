# pyquery库选择器跟css类似
# 导包
from pyquery import PyQuery as pq

# 定义要演示的html字符串，接下来的操作就对它做信息提取
html = '''
<div>
    <ul id="container">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html" class="link">second item</a></li>
         <li class="item-2 active"><a href="link3.html" class="link"><span class="bold">third item</span></a></li>
         <li class="item-3 active"><a href="link4.html" class="active" class="link">fourth item</a></li>
         <li class="item-4"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
# 初始化
# 1：使用字符串
doc1 = pq(html)
# print(doc1('li'))
# 2：也可以传入一个url
doc2 = pq(url='http://8.130.167.39/')
# print(doc2('title'))
# 3：读取本地文件
doc3 = pq(filename='test.html')
# print(doc3('li'))

# 使用CSS选择器选择节点，会选择全部
# print(doc1('#container .item-1 a'))
# print(type(doc1('#container .item-1 a')))

# 遍历选择出来的节点调用text方法就可以获得里面的内容
# for item in doc1('#container .item-1 a').items():
# print(item.text())

# TODO:查找节点
# 子节点
# 1：find方法，这个相当于选择器分开写了，但是这个不是遍历每一个，是直接一次拿到符合条件的【字符串】
items = doc1('#container')
lis1 = items.find('.active')
# print(lis1)
# 2：children方法，children会忽略孙子等节点只关心子节点，传入选择器筛选子节点
lis2 = items.children('.active')
# print(lis2)


# 父节点
# 1：parent方法，这个方法只会获取直接父节点
parent = doc1('#container li').parent()
# print(parent)         # 获取到ul节点
# 2：parents方法，获取到祖先节点
parents = doc1('#container li').parents()
# print(parents)        # 获取到div和ul
# 3：进一步筛选祖先节点
parents_checked = doc1('#container li').parents('div')
# print(parents_checked)  # 获取到div

# 兄弟节点
# 1：siblings方法
single_li = doc1('#container .item-0')
siblings_li = single_li.siblings()
# print(siblings_li)        # 获取到所有li
# 使用选择器过滤兄弟节点
second_li = single_li.siblings('.item-1')
# print(second_li)          # 获取到第二个li

# 遍历节点
items_li = doc1('#container li')
# for li in items_li.items():
# print(li.text())  # 打印所有li标签里面的文本

# TODO:提取信息
# 获取属性
# 需求：1：获取第三个li的所有class属性，2：获取第三个li里面的a的href
# 选中这个节点->调用attr方法得到属性值
classes = doc1('#container .item-2').attr('class')
a_href_value = doc1('#container .item-2 a').attr('href')
# print('第三个li的所有属性值为：' + classes + "第三个li的a里面的href属性值为" + str(a_href_value))

# 获取所有class="link"的a节点的href属性（！！！如果使用attr是不能实现的，只会返回节点中第一个的href，这个时候需要借助items这个方法遍历）
a_s = doc1('.link')
print(a_s)
for a in a_s.items():
    print(a.attr('href'))
