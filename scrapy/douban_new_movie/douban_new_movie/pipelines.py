# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
'''
我想把这些保存成JSON格式的数据。怎么做呢？当然是处理我们的数据啦，在哪里处理呢？当然是在我们的管道（pipelines）里处理啦，好我们来写一个处理程序 - pipelines.py：
'''
import json
import codecs
import sys
# 首先，我们把我们的JSON包和编解码器包引进，编解码器包使用来处理中文的
import importlib
importlib.reload(sys)


class DoubanNewMoviePipeline(object):

    def __init__(self):
        self.file = codecs.open('douban_new_movie.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = 'the new movie list:'+'\n'

        for i in range(len(item['movie_star'])):
            movie_name = {'movie_name':str(item['movie_name'][i]).replace('','')}
            movie_star = {'movie_star':item['movie_star'][i]}
            movie_url = {'movie_url':item['movie_url'][i]}
            line = line + json.dumps(movie_name, ensure_ascii=False)
            line = line + json.dumps(movie_star, ensure_ascii=False)
            line = line + json.dumps(movie_url, ensure_ascii=False) + '\n'

        self.file.write(line)

    def close_spider(self, spider):
        self.file.close()

        #return item
