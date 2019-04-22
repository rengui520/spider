# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import urlencode
import json
from images360.items import Images360Item

class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self): # start_requests() 这个函数用来构造最开始的请求，用来生成 50 次请求。
        # data = {'ch': 'photogtaphy', 'listtype': 'new'}
        data = {'ch': 'wallpaper'}
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):   #首先解析JSON，遍历其list字段，取出一个个图片信息，然后再对ImageItem赋值，生成Item对象。
        result = json.loads(response.text)   # 字符串转dict类型
        for image in result.get('list'):
            item = Images360Item()
            item['id'] = image.get('imageid')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item