# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
#from scrapy_demo import settings


class ScrapyDemoPipeline(object):

    #def __init__(self,):
        #self.conn = pymysql.connect(
        #    host = settings.MYSQL_HOST,
        #    db = settings.MYSQL_DBNAME,
        #    user = settings.MYSQL_USER,
        #    passwd = settings.MYSQL_PASSWORD,
        #    charset = 'utf8',
        #    use_unicode = False
        #)
        #self.cursor = self.conn.cursor()

    #def process_item(spider):
    #def process_item(self, item, spider):
        #with open('E:/weixinkaifa/vmoviespider.txt', 'a') as f:
            #f.write('{},,{},{},{}\n'.format(item['cover'],item['title'],item['dec'],item['playUrl']))
        #
        #self.insertData(item)
        #return item

    def insertData():
    #def insertData(self, item):
        #sql = "INSERT INTO vmovie(cover, title, mdec, playUrl) VALUES(%s, %s, %s, %s)"
        #params = (item['cover'], item['title'], item['dec'], item['playUrl'])
        #self.cursor.execute(sql, params)
        #self.conn.commit()
        db = pymysql.connect(host='localhost', user='root', password='xuujii123456', port=3306, db='spiders')
        cursor = db.cursor()
        sql = 'INSERT INTO vmovie(cover, title, dec, playUrl) values(%s, %s, %s, %s)'
        try:
            cursor.execute(cover, title, dec, playUrl)
            db.commit()
        except:
            db.rollback()
        db.close()



