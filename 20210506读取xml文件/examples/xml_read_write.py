# -*- coding = utf-8 -*-
# @time:2021/5/6 21:07
# Author:wmj
# @File:xml_read_write.py
# @Software:PyCharm
# @Function:读取和修改.xml文件:https://www.jb51.net/article/182025.htm

# coding=utf-8
import xml.dom.minidom
# 打开xml文档
dom = xml.dom.minidom.parse('test.xml')

# 得到文档元素对象
root = dom.documentElement
print(root)
print(root.nodeName)
print(root.nodeValue)
print(root.nodeType)
print(root.ELEMENT_NODE)

# 1.获取maxid这一node名字(没有属性值),如何获取里面的文本?
bb = root.getElementsByTagName('maxid')
b = bb[0]
print("111")
# print(b.documentElement)

# 2.获取login 这一node名字及相关属性值
login = root.getElementsByTagName('login')
login = login[0]  # 获取login的相关属性值
un = login.getAttribute("username")
print(un)
pd = login.getAttribute("passwd")
print(pd)
# 修改先关属性值

# 3.获取节点名为item的相关属性值
item = root.getElementsByTagName('item')  # 获取了所有名字为item的node
item = item[0]  # 拿到第一个item,获取相关属性值
i = item.getAttribute("id")  # 获取id的值
print(i)  # 获得节点下所有元素的列表

# 4.获取标签对之间的数据,并修改为新的值
caption = root.getElementsByTagName('caption')
c0 = caption[0]
print(c0.firstChild.data)  # firstChild属性返回被选节点的第一个子节点,.data表示获取该节点数据

c2 = caption[2]  # caption节点有三个!!!
print(c2.firstChild.data)
# 修改标签对之间的数据,直接对节点数据赋值
c2.firstChild.data = 'dhhdlh'
print(c2.firstChild.data)
