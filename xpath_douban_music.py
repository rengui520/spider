# coding:utf-8
from lxml import etree
import requests
import json

#获取页面地址
def getUrl():
    for i in range(10):   #遍历i，从1到10
      url = 'https://music.douban.com/top250?start={}'.format(i*25)
      scrapyPage(url)

#保存数据	  
def write_to_file(content):
    with open('E:/wenben/2019042101.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

#爬取每页数据
def scrapyPage(url):
    html = requests.get(url).text
    s = etree.HTML(html)  # 将源码转化为能被XPath匹配的格式
    trs = s.xpath('//*[@id="content"]/div/div[1]/div/table/tr')  #xpath表达式， 返回为一列表所有信息共有路径

    for tr in trs: #tr信息为一列表，遍历一下
        href = tr.xpath('./td[2]/div/a/@href')[0]   #链接在标题标签href属性中
        title = tr.xpath('./td[2]/div/a/text()')[0]   #注意新节点是tr下的节点。「.」选取当前节点
        '''
        /tbody 标签删除.因为要获取标题，所以我需要这个当前路径下的文本，所以使用/text().
        又因为这个s.xpath返回的是一个列表，且列表中只有一个元素，所以构造索引[0]将信息提取出来
        '''
        score = tr.xpath('./td[2]/div/div/span[2]/text()')[0].strip()
        number = tr.xpath('./td[2]/div/div/span[3]/text()')[0].strip()[30:-22]
        img = tr.xpath('./td[1]/a/img/@src')[0].strip()
    #对比他们的xpath，发现只有table序号不一样，我们可以就去掉序号，得到通用的xpath信息：
        items = (href.strip(), title.strip(), score, number, img)
        for item in items:
            print(item)
            write_to_file(item)

if '__main__':
    getUrl()

"""
/    #从当前节点选取直接子节点
//  #从当前节点选取子孙节点
.  #选取当前节点
..   #选取当前节点的父节点
@  #选取属性

//title[@lang='eng']   #选择所有名称为 title ，同时属性 lang 的值为 eng 的节点
//*[@lang='eng']       #选择属性 lang 的值为 eng 的节点
"""