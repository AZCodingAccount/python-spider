from lxml import etree

# Xpath解析HTML页面只需要三个步骤。
#               1. 构造xpath对象（把html字符串转换成xpath对象）
#               2. 编写选择器（最重要） 这个主要可以通过节点的属性，节点相互之间的层级关系，是否递归的进行匹配这些因素。
#               3. 取出需要的text数据
text = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <div>
      <ul>
        <li class="item-0"><a href="link1.html">first item</a></li>
        <li class="item-1 li" name="li-2">
          <a href="link2.html">second item</a>
        </li>
        <li class="item-inactive"><a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a></li>
      </ul>
    </div>
  </body>
</html>
'''
# 使用HTML可以自动修正html结果，html为bytes类型
html = etree.HTML(text)
result = etree.tostring(html)
# print(result.decode('utf-8'))
# 从外部导入HTML文件并解析
new_html = etree.parse('./test.html', etree.HTMLParser())
# 获取文件调用etree里面的xpath方法就可以解析出节点了，学习xpath的过程就是写选择器的过程
# 1.选取所有节点
result0 = new_html.xpath('//*')

# 2.选取子节点，使用/获取子节点，使用//获取子孙节点。注意层级的关系
result1 = html.xpath('//ul/li')  # 选取ul里面的所有li，只会直接选中，不会跨层级选中
result2 = html.xpath('//ul//a')  # 选取ul里面的所有a，会跨层级选中

# 3.根据子节点的属性选择到父节点，类似于相对路径
result3 = html.xpath('//a[@href="link4.html"]/../@class')  # 根据属性选择器选择到a标签。利用../回到父级获取父级的class属性

# 4.根据节点里面的class类进行选择
result4 = new_html.xpath('//li[@class="item-0"]')

# 5.获取节点中的文本，使用text()函数。
# 如果直接匹配子节点，可能会匹配到其他子节点的数据。/n之类的。这里是因为自动添加了</li>标签，自动换行。
result5 = html.xpath('//li[@class="item-0"]//text()')
result6 = html.xpath('//li[@class="item-0"]/a/text()')

# 6.获取节点的属性，使用@href
result7 = html.xpath('//li/a/@href')  # 获取所有li下面的所有a的href属性

# 7.根据多个属性值进行匹配，采用contains方法.只有包含这个属性就被筛选出来
result8 = html.xpath('//li[contains(@class,"li")]/a/text()')  # 查找li里面class属性下面包含li的a标签的值

# 8.根据多个属性的值进行匹配，利用and运算符
result9 = html.xpath('//li[contains(@class,"li") and @name="li-2"]/a/text()')  # 筛选出类名包含li的，name值为li-2的li，
# 并且求出它下面的text值

# 9.按序选择，匹配到多个节点后，选择多个节点当中的第几个
result10 = html.xpath('//li[1]/a/text()')  # 选择第一个li里面的a的text值
result11 = html.xpath('//li[last()]/a/text()')  # 选择最后一个li里面的a的值
result12 = html.xpath('//li[position()>3]/a/text()')  # 选择3以后的li标签下面的a的值

# 10.选取跟本节点相关的节点

result13 = html.xpath('//li[1]/ancestor::*')  # 获取第一个li的所有父节点，递归获取，会往上继续找
result14 = html.xpath('//li[1]/ancestor::div')  # 获取所有父节点，但是只要div标签的
result15 = html.xpath('//li[1]/attribute::*')  # 获取当前li节点的所有属性值
result16 = html.xpath('//li[1]/child::a[@href="link1.html"]')  # 获取当前li节点的子节点，并且需要满足href=link1.html条件
result17 = html.xpath('//li[1]/descendant::span')  # 获取当前li节点的所有子孙节点，但是只要span标签的
result18 = html.xpath('//li[1]/following::*[2]')  # 获取当前节点之后的所有节点（不是同级的），但是只要第2个。就是a
result19 = html.xpath('//li[1]/following-sibling::*')  # 获取当前节点之后的所有节点（是同级的）。

# for循环专门打印运行结果
for i in range(0, 20):
    print(f'result{i}: {locals()["result" + str(i)]}')
    print('--------------------------')
