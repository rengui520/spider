#import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector

from douban_new_movie.items import DoubanNewMovieItem

class DoubanNewMovieSpider(scrapy.Spider):
    name = 'douban_new_movie_spider'
    allowed_domains = ['www.movie.douban.com']
    start_urls = ['http://movie.douban.com/chart']

    def parse(self, response):
        sel = Selector(response)

        movie_name = sel.xpath("//div[@class='p12']/a/text()").extract()
        movie_url = sel.xpath("//div[@class='p12']/a/@href").extract()
        movie_star = sel.xpath("//div[@class='p12']/div/spen[@class='rating_nums']/text()").extract()
        # 注意：seletor方法的报道查看后一定要用它的extract() 方法，来返回一个列表.

        item = DoubanNewMovieItem()

        item['movie_name'] = response.meta['movie_name']
        item['movie_star'] = response.meta['movie_star']
        item['movie_url'] = response.meta['movie_url']

        yield item

        print(movie_name, movie_star, movie_url)