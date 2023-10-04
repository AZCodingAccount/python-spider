# pyquery库选择器跟css类似
# 导包
from pyquery import PyQuery as pq

# 定义要演示的html字符串，接下来的操作就对它做信息提取
html = '''
<div>
    <ul id="container">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html" class="active">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
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

# 查找节点
# 1：find方法，这个相当于选择器分开写了，但是这个不是遍历每一个，是直接一次拿到符合条件的字符串
items = doc1('#container')
lis = items.find('.active')
# print(lis)
# 2：children方法，children会忽略孙子等节点只关心子节点
items = doc1('#container')
lis = items.children('.active')
# print(lis)
