# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

import pymysql

class MongoPipeline(object):   # 存储至MongoDB
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    # from_crawler()方法是一个类方法，用 @ classmethod标识，是一种依赖注入的方式。
    # 它的参数是crawler，通过crawler对象，我们可以拿到Scrapy的所有核心组件，如全局配置的每个信息，
    # 然后创建一个Pipeline实例。参数cls就是Class，最后返回一个Class实例

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    # open_spider() 方法是在Spider开启的时候被自动调用的。在这里我们可以做一些初始化操作，如开启数据库连接等。
    # 其中，参数 spider 就是被开启的 Spider 对象。

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item
    #1. process_item() 是必须要实现的方法，被定义的 Item Pipeline 会默认调用这个方法对 Item 进行处理。
    # 比如，我们可以进行数据处理或者将数据写入到数据库等操作。它必须返回 Item 类型的值或者抛出一个 DropItem 异常。
    #2. process_item() 方法的参数有如下两个。
    # item，是 Item 对象，即被处理的 Item。
    # spider，是 Spider 对象，即生成该 Item 的 Spider。
    #3. process_item() 方法的返回类型归纳如下。
    # 如果它返回的是Item对象，那么此Item会被低优先级的 Item Pipeline 的 process_item() 方法处理，直到所有的方法被调用完毕。
    # 如果它抛出的是DropItem异常，那么此Item会被丢弃，不再进行处理。

    def close_spider(self, spider):   #当 spider 关掉时这个方法被调用
        self.client.close()
    # close_spider()方法是在Spider关闭的时候自动调用的。在这里我们可以做一些收尾工作，如关闭数据库连接等。其中，参数 spider 就是被关闭的 Spider 对象。



class ImagePipeline(ImagesPipeline):    # 下载图片到本地
    def file_path(self, request, response=None, info=None):   #获得图片的原始名
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
    # file_path()。它的第一个参数request就是当前下载对应的Request对象。这个方法用来返回保存的文件名，
    # 直接将图片链接的最后一部分当作文件名即可。它利用split()函数分割链接并提取最后一部分，返回结果。
    # 这样此图片下载之后保存的名称就是该函数返回的文件名。

#第一个元素表示图片是否下载成功；第二个元素是一个字典
    def item_completed(self, results, item, info):     #图片下载完毕后，处理结果会以二元组的方式返回给 item_completed() 函数。
        image_paths = [x['path'] for ok, x in results if ok]   # 打印图片 path,比如 xx.jpg
        # 等价于
        # for ok, x in results:
        #     if ok:
        #         image_paths = [x['path']]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
    # item_completed()，它是当单个Item完成下载时的处理方法。因为并不是每张图片都会下载成功，
    # 所以我们需要分析下载结果并剔除下载失败的图片。如果某张图片下载失败，那么我们就不需保存此Item到数据库。
    # 该方法的第一个参数results就是该Item对应的下载结果，它是一个列表形式，列表每一个元素是一个元组，
    # 中包含了下载成功或失败的信息。这里我们遍历下载结果找出所有成功的下载列表。如果列表为空，
    # 那么该Item对应的图片下载失败，随即抛出异常DropItem，该Item忽略。否则返回该Item，说明此Item有效。

    def get_media_requests(self, item, info):   #根据 image_urls 中指定的 url 进行爬取。为每个 url 生成一个Request
        yield Request(item['url'])
    # get_media_requests()。它的第一个参数item是爬取生成的Item对象。
    # 我们将它的url字段取出来，然后直接生成Request对象。此Request加入到调度队列，等待被调度，执行下载。

# class MysqlPipeline():
#     def __init__(self, host, database, user, password, port):
#         self.host = host
#         self.database = database
#         self.user = user
#         self.password = password
#         self.port = port
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             host=crawler.settings.get('MYSQL_HOST'),
#             database=crawler.settings.get('MYSQL_DATABASE'),
#             user=crawler.settings.get('MYSQL_USER'),
#             password=crawler.settings.get('MYSQL_PASSWORD'),
#             port=crawler.settings.get('MYSQL_PORT'),
#         )
#
#     def open_spider(self, spider):
#         self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
#         self.cursor = self.db.cursor()
#
#     def close_spider(self, spider):
#         self.db.close()
#
#     def process_item(self, item, spider):
#         data = dict(item)
#         keys = ', '.join(data.keys())
#         values = ', '.join(['%s'] * len(data))
#         sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
#         self.cursor.execute(sql, tuple(data.values()))
#         self.db.commit()
#         return item