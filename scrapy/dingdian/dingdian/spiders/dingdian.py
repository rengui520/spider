# coding:utf-8
import scrapy
from dingdian.items import DingdianItem # 将 item 导入进来，这样数据才能在各个模块之间流转（导入 dingdian 项目中 items 文件中的 DingdianItem 类）

class Myspider(scrapy.Spider):
    name = 'dingdian' # 请注意，这name就是我们在 entrypoint.py 文件中的第三个参数！
    base_url = 'http://nlook1.cn/index.php?s=/vod-type-id-1-type--area--year--star--state--order-addtime-p-'
    baseurl = '.html' # 这两个 url 是为了之后的爬虫翻页处理
    start_urls = [] # 建立需要爬取信息的 url 列表
    for i in range(160): # 从第一页开始到 160 页，使用字符串拼接的方式实现了我们需要的全部 URL
        url = base_url + str(i) + baseurl
        start_urls.append(url)

# 刚上路的新手可能会想，这个函数到底是干嘛的，这个函数其实是 Scrapy 处理下载的 response 的默认方法，我们直接用就好了
    def parse(self, response):
        lists = []         #  先建立一个列表，用来保存每一页的信息
       
       # 通过观察我们看到该页面所有影片的信息都位于一个class属性为list-unstyled vod-item-img ff-img-215的 ul 标签内的 li 标签内。
        movies = response.xpath('//ul[@class="list-unstyled vod-item-img ff-img-215"]/li')      
        for movie in movies:
            list = DingdianItem() # 申请一个weatheritem 的类型来保存结果
           # 为什么要用.extract()[0],是因为.xpath 返回的是一个列表,我们是获取里面的内容
            list['name'] = movie.xpath('.//p[@class="image"]//img/@alt').extract()[0]
            list['img'] = movie.xpath('.//p[@class="image"]//img/@data-original').extract()[0]
            list['movie'] = 'http://nlook1.cn' + movie.xpath('.//p[@class="image"]/a/@href').extract()[0]
            lists.append(list)  # 添加到 lists 列表中
        return lists # 一定要有这个返回 lists ，因为之后我们要将数据下载到本地，没有的话，就下载保存不了的
        
        #爬虫文件 parse() 函数一定要有 return 语句 