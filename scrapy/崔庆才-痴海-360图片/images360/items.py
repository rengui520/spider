# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class Images360Item(scrapy.Item):
    collection = table = 'images'
    # 设置MongoDB的表名为 images。两个属性 collection 和 table，都定义为 images 字符串，代表 MongoDB 存储的 Collection 名称。
    id = Field()    #图片的 ID
    url = Field()    #链接
    title = Field()   #标题
    thumb = Field()   #缩略图


