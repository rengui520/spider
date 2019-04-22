# -*- coding: utf-8 -*-
import scrapy

from quotetutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'   #spiser 的唯一标识
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):   #解析单页网页
        #pass
        #print(response.text)
        quotes = response.css('.quote')
        for quotes in quotes:
            item = QuoteItem()
            text = quotes.css('.text::text').extract_first()  #传入CSS 选择器。只有一个元素时用extract_first()
            author = quotes.css('.author::text').extract_first()
            tags = quotes.css('.tags .tag::text').extract()   #多个元素时用extract(),会以列表的形式返回结果。
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item   #生成字典类型数据

        #实现翻页循环
        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)   #urljoin获取绝对url
        yield scrapy.Request(url=url, callback=self.parse)   #相当于重新发起一次请求。回绝函数callback递归调用自己，parse是处理索引页函数





