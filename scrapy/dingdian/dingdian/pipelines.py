# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DingdianPipeline(object):
    def process_item(self, item, spider):
        with open('E:\weixinkaifa\dingdian.txt', 'a') as f:
            f.write('{},,{},{}\n'.format(item['name'],item['img'],item['movie']))
        #return item
        '''
        我们编写 pipelines.py 来处理 spider爬到的内容，这里有几个非常重要的注意事项，
        请大家一定要注意，否则都会导致你的数据无法保存到本地。
        '''
