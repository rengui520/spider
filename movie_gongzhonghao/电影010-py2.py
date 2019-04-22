#*-*-coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from bs4 import BeautifulSoup
import requests
import time
import io
with io.open('kaifa01.txt','w',encoding='utf-8') as f:
        url = 'http://wx.hyb3333.com/lists/1.html'
        urls = ['http://wx.hyb3333.com/lists/1-{}.html'.format(str(i)) for i in range(1,4)]

        def get_attactions(url,date=None):
                wb_date = requests.get(url)
                soup = BeautifulSoup(wb_date.text,'lxml')
                titles = soup.select('div.img > p')
                imgs = soup.select('div.img > img')
                movies = soup.select('li.listfl > a')
                time.sleep(1)
                for title,img,movie in zip(titles,imgs,movies):
                        f.write("{},,{},{}\n".format(title.get_text().decode('unicode_escape'),img.get('data-original').decode('unicode_escape'),'http://wx.hyb3333.com/play'+ movie.get('href')[6:13]+'-0-0.html').decode('unicode_escape'))
        for single_url in urls:
                get_attactions(single_url)
                print(single_url)