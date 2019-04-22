# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#保存之前，对item进行处理。如有一些 item 不是想要的，或者想保存到数据库中，在下边修改
#class QuotetutorialPipeline(object):
import pymongo
from scrapy.exceptions import DropItem


class TextPipeline(object):

    def __init__(self):
        self.limit = 50    #长度限制


    def process_item(self, item, spider):
        #return item
        if item['text']:   #如果名言太长，进行截断
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')

class MongoPipeline(object):   #声明函数保存到数据库

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri  #声明全局变量
        self.mongo_db = mongo_db

    #返回构造函数的调用
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),  #返回结果为在settings.py 定义的变量
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):  #open_spider爬虫刚要启动的时候执行的操作.完成mongodb的初始化对象的声明。
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__   #改  的名称，
        self.db[name].insert(dict(item))          #存入 MongoDB的判断。item叫什么名，  就叫什么名
        return item

    def close_spider(self, spider):  #关闭spider
        self.client.close()

