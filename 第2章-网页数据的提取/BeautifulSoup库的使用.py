import re
from bs4 import BeautifulSoup

"""
     BeautifulSoup这个选择器可以选择很多解析器，html.parser,lxml等等。
     就是根据标签名和属性值获取，获取多了就是一个列表再遍历，还想再往下获取就再find。
     可以使用css选择器 （select方法）。个人比较习惯用pyquery，这个感觉没啥特点
"""
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><a><b>The Dormouse's story</b></a></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
# 解析html页面
soup = BeautifulSoup(html, 'lxml')
# 把html标准化输出
# print(soup.prettify())
print("--------------------------------")

# 1.节点选择器，相较于xpath更加简洁，直接选取节点
print(type(soup.title))  # 打印title标签的类型
print(soup.title)  # 打印title标签
print(soup.head)  # 会嵌套获取标签
print(soup.p)  # 只会选中相同标签的第一个
print(soup.title.string)  # 取出html中的title标签里面的内容，如果是父标签且没内容，就是None
print("--------------------------------")

# 2.获取名称或者属性
print(soup.p.attrs)  # 获取第一个p节点的所有属性
print(soup.title.name)  # 获取当前节点的名称
print(soup.p['name'])  # 获取当前节点的name属性的值，可能返回的是一个列表
print("--------------------------------")

# 3.嵌套进行获取。直接往下.就好了
print(soup.html.p)  # 获取html标签下的第一个p标签
print("--------------------------------")

# 4.进行节点之间的关联选择
# 子节点
print(soup.p.contents)  # 获取第一个p节点的直接子节点，会选择里面的内容
print(soup.p.children)  # 获取子节点，返回一个可迭代的对象
for i, child in enumerate(soup.p.children):
    print(i, child)  # 获取的跟直接子节点一样，但是这个是迭代器对象

print(soup.p.descendants)
for i, child in enumerate(soup.p.descendants):
    print(i, child)  # 这个会把孙子（重孙子...）节点也遍历出来，甚至还有最后节点的内容
# 父节点
print(soup.a.parent)  # 获取第一个a标签的父节点，应该是第一个p
print(soup.a.parents)  # 往上递归寻找父节点。
# print(list(enumerate(soup.a.parents)))
# 兄弟节点。BS4会把空格，换行符和普通文本都当成节点，这个需要注意，因此第一个就是/n
print('下一个兄弟:', soup.p.next_sibling)
print('上一个兄弟:', soup.p.next_sibling.previous_sibling)
print('下一个兄弟们:', soup.p.next_siblings)
print('下一个兄弟们:', soup.p.next_sibling.next_sibling.previous_siblings)
print("--------------------------------")

# 调用方法进行查询
html2 = '''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''
soup2 = BeautifulSoup(html2, 'lxml')
# 根据节点名查询
print(soup2.find_all(name='ul'))  # 查找所有标签为ul的节点，返回一个列表
print(type(soup2.find_all(name='ul')[0]))  # 查找第一个ul标签的节点
# 根据属性查询。如果class有多个值也可以筛选出来（选择其中任意一个）
# 查询id为list-1，且class为list的元素
print(soup2.find_all(attrs={
    'id': 'list-1',
    'class': 'list'
}))
# 根据文本查询
print(soup2.find_all(string=re.compile('ar')))  # 查找所有包含ar字符串的文本，返回一个列表
print("--------------------------------")

# find方法查找第一个匹配的元素。
print(soup2.find(class_='list'))
print("--------------------------------")

# 使用CSS选择器
tag = soup2.select('#list-2 .element:first-child')  # 选择id为list-2下的类为element下的第一个节点，返回的是一个列表
print(tag)
# 选取到节点之后就可以获取一系列属性，属性名，string文本，标签名
print(tag[0].attrs)  # 获取当前标签所有属性，返回的是一个字典
print(tag[0].string)  # 获取标签里面的文本
print(tag[0].name)  # 获取当前标签名
