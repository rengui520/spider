# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class MongoPipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymongo

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['user'].update({'url_token': item['url_token']}, {'$set': item}, True)     #去重方法
        return item

# 比较重要的一点就在于process_item，在这里使用了update方法，第一个参数传入查询条件，这里使用的是url_token，
# 第二个参数传入字典类型的对象，就是我们的item，第三个参数传入True，这样就可以保证，如果查询数据存在的话就更新，
# 不存在的话就插入。这样就可以保证去重了。

#另外记得开启一下Item Pileline












