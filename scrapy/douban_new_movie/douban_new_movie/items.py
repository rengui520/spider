# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# 首先引入scrapy

#接着创建一个类，继承自scrapy.item，这个是用来储存要爬下来的数据的存放容器，类似ORM的写法，
class DoubanNewMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    moive_name = scrapy.Field()  # 电影的名字，
    moive_star = scrapy.Field()  # 电影的评分，
    moive_url = scrapy.Field()  # 电影的链接
    #pass
