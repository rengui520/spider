# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 电影名称
    name = scrapy.Field()
    # 电影链接
    movie = scrapy.Field()
    # 电影图片
    img = scrapy.Field()
    #pass
    '''
    现在我们来先编写 items.py ，十分的简单，只需要将希望获取的字段名填写进去，比如我们先要爬取的数据是，
    电影名称，电影图片，电影跳转链接，我们直接写进去就可以了，不用管其他的：
    是不是特别的简单，下面开始重点了哦！编写 spider（就是我们用来提取数据的爬虫了）


    '''
