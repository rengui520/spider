import scrapy

class csdnspider(scrapy.Spider): # 必须继承scrapy.Spider
    name = "csdn" #爬虫名称,这个名称必须是唯一的
    allowed_domains=["csdn.net"] #允许的域名
    start_urls = [
        "https://www.csdn.net/nav/ai"
    ]

    def parse(self, response):
        # 实现网页的解析
     pass