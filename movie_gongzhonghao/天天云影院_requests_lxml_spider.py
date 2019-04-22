# -*- coding: utf-8 -*-
import time
import requests
from lxml import etree

def get_html_text(url):
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return ""

def parse_and_asve(url):
    html = get_html_text(url)
    selector = etree.HTML(html)
    infos = selector.xpath('//div[@class="module-content"]/ul//li/a')
    if selector is not None:
        for info in infos:
            try:
                movie_name = info.xpath('./div[2]/p[1]/text()')[0]
                movie_img = info.xpath('./div[1]//img/@data-original')[0]
                # movie_url = 'http://www.ttkyy.net' + info.xpath('@href')[0]
                movie_url = 'http://ttkyy.wx.smsjyy.com' + '/p' + info.xpath('@href')[0][2:-5] + '-0-0.html'
            except:
                print("")
            time.sleep(1)
            with open('E:/wenben/042100.txt', 'a', encoding='utf-8') as f:
                f.write('{},,{},{}\n'.format(movie_name, movie_img, movie_url))

def main():
    url = 'http://www.ttkyy.net/f/1.html'
    parse_and_asve(url)
    urls = ['http://www.ttkyy.net/f/1_{}.html'.format(str(i)) for i in range(2, 99)]
    for a_url in urls:
        parse_and_asve(a_url)
        print(a_url)

main()