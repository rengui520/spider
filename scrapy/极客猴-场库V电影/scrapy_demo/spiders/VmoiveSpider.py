# coding:utf-8

'''
Spider 目录是我们爬虫程序爬取网站以及提取信息的模块。我们首先在目录下新建一个名为 VmoiveSpider 的文件。
同时，该类继承scrapy.Spider。

这里我们用到的scrapy.spider.Spider 是 Scrapy 中最简单的内置 spider。
继承 spider 的类需要定义父类中的属性以及实现重要的方法。
'''
import scrapy
from scrapy_demo.items import ScrapyDemoItem

class VmoiveSpider(scrapy.Spider):
	# 用于区别Spider，必须是唯一的,它是 String 类型.
	name = 'vmovie'
	'''
	name
    这个属性是非常重要的，所以必须定义它。定义 name 目的是为爬虫程序命名。
    因此，还要保持 name 属性是唯一的。它是 String 类型，
    我们在 VmoiveSpider 可以定义：
    '''
	
	allowed_domains = ['vmovier.com']
	'''
	可选字段(可选定义）。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 
	域名不在列表中的URL不会被跟进。根据 V 电影的 url 地址，我们可以这样定义：
	'''
	
	# 启动时爬取入口的URL列表，后续的URL则从初始的URL的响应中主动提取,
	start_urls = ['https://www.vmovier.com/']
	#start_urls 是 Url 列表，也是必须被定义。可以把它理解为存放爬虫程序的主入口 url 地址的容器。
	
	def parse(self, response):
		lists = []
		#self.log('item page url is ==== ' + response.url)
		
		moivelist = response.xpath("//li[@class='clearfix']")
		
		for m in moivelist:
			list = ScrapyDemoItem()
			list['cover'] = m.xpath('./a/img/@src')[0].extract()
			list['title'] = m.xpath('./a/@title')[0].extract()
			list['dec'] = m.xpath("./div/div[@class='index-intro']/a/text()").extract()[0]
			list['playUrl'] = 'https://www.vmovier.com/' + m.xpath('./@data-id').extract()[0] + '?from=index_new_img'
			#print(list)
			#yield item
			lists.append(list)
		return lists
			#'''
			#添加个[0], 因为 xpath() 返回的结果是列表类型。
			#如果不添加，运行结果会返回一个列表，而不是文本信息。
			#'''
			
			
		    #item['playUrl'] = response.xpath("//*[@id='iframeId']/@src")[0].extract()
		    #item['playUrl'] = 'https://www.vmovier.com/' + response.xpath("//*[@id='post-list']/li/@data-id")[0] + '?from=index_new_img'
		
			
		    #为什么要在 [0] 后面添加 extract()方法，这里涉及到内建选择器 Selecter 的知识。
		    # extract()方法的作用是串行化并将匹配到的节点返回一个unicode字符串列表。把html 标签去掉

			# 提取电影详细页面 url 地址
			#urlitem = m.xpath('./a/@href')[0].extract()
			#url = response.urljoin(urlitem)

			#yield scrapy.Request(url, callback=self.parse_moive, meta={
				#'cover': item['cover'],
				#'title': item['title'],
			#	'dec': item['dec'],
			#})
				
	#def parse_moive(self, response):
		#item = ScrapyDemoItem()
		#item['cover'] = response.meta['cover']
		#item['title'] = response.meta['title']
		#item['dec'] = response.meta['dec']
		#item['playUrl'] = response.xpath(".//div[@class='p00b204e980']/p/iframe/@src")[0].extract()	
		#yield item



		    #'''
		    #parse(response)

            #parser 方法是Scrapy处理下载的response的默认方法。它同样必须被实现。
		    #parse 主要负责处理 response 并返回处理的数据以及跟进的URL。
		    #该方法及其他的Request回调函数必须返回一个包含 Request 及(或) Item 的可迭代的对象。
            #'''
			
			
			