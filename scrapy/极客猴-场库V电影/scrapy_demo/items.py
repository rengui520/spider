# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	#封面
	cover = scrapy.Field()
	# 标题
	title = scrapy.Field()
	# 简述
	dec = scrapy.Field()
	# 播放地址
	playUrl = scrapy.Field()
    # pass
	'''
	为什么将爬取信息定义清楚呢？因为接下来 Item 需要用到。在 Item.py 文件中，我们以类的形式以及 Field 对象来声明。
	其中 Field 对象其实是一个字典类型，用于保存爬取到的数据。而定义出来的字段，可以简单理解为数据库表中的字段，
	但是它没有数据类型。Item 则复制了标准的 dict API，存放以及读取跟字典没有差别。
	'''
