#coding:utf-8
#构造html下载器。利用 requests 模块下载HTML网页
import requests
import re
import json
from requests.exceptions import RequestException  #捕获异常
from multiprocessing import Pool

def get_one_page(url): #此函数用来获取网页内容
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        reponse = requests.get(url, headers=headers)
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        return None

def parse_one_page(html): #分析解析网页内容,构造html解析器
    # 排名、名称、图片、上映时间、评分
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?<a.*?title="(.*?)".*?>'
                         '.*?<img.*?data-src="(.*?)".*?>'
                         '.*?<p.*?star">(.*?)</p>.*?'
                         '.*?releasetime">(.*?)</p>'
                         '.*?integer">(.*?)</i>'
                         '.*?fraction">(.*?)</i>.*?</dd>', re.S) #匹配一个名称时，起始符，结束符都要匹配一下

    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'src': item[2],
            # 'time': item[3].strip()[5:],
            # 'socre': item[4]+item[5]
            'actor': item[3].strip()[3:], #strip()方法把换行符去掉，后边加[3:]是为了把前边3个字符去掉
			  'time': item[4].strip()[5:],
			  'score': item[5] + item[6]
        }
        '''
                注意：
                在函数中本来该return的地方用yield，如果用return，在第一轮循环就会跳出，结果文件只会有一部电影。如果用yield，函数返回的就是一个生成器，而生成器作为一种特殊的迭代器，可以用for—in方法，一次一次的把yield拿出来；
                re.findall(pattern,string[,flags])：搜索整个string，以列表的形式返回能匹配的全部子串，其中参数是匹配模式。
                在Python的正则表达式中，有一个参数为re.S。它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”。
                '''

def write_to_file(content): #将爬取到的内容写入文件中,构造数据存储器
    with open('E:\wenben\maoyanT100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
        '''
        注意事项：
        1. 为什么ensure_ascii=False？原因是json默认是以ASCII来解析code的，由于中文不在ASCII编码当中，因此就不让默认ASCII生效；
        2. json.dumps() 的作用：用于将dict类型的数据转成str,因为如果直接将dict类型的数据写入json文件中会发生报错，因此在将数据写入时需要用到该函数;

        3. 要写入特定编码的文本文件，请给open()函数传入encoding参数，将字符串自动转换成指定编码。细心的童鞋会发现，以'w'模式写入文件时，如果文件已存在，会直接覆盖（相当于删掉后新写入一个文件）。如果我们希望追加到文件末尾怎么办？可以传入'a'以追加（append）模式写入

        '''

def main(offset):  #分页获取数据,接下来就是构造主函数，初始化各个模块，传入入口URL，按照运行流程执行上面三大模块：
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':  
    pool = Pool()   #在运行中，创建了一个线程池，多线程一起抓取，会让爬虫效率更高
    pool.map(main, [i * 10 for i in range(10)])

    '''
    注意：
    为了提高速度，我们引入Pool模块，用多线程并发抓取。
    如果不怎么清楚，可以先记住这个用法，想具体了解的话可以百度，因为 Pool 模块比较多，这里不好详细展开，见谅！

    本程序中介绍了基础爬虫架构主要的的三个模块（HTML下载器、HTML解析器、数据存储器），无论大型还是小型爬虫都不会脱离这三个模块，也希望大家通过这个小小的练习对整个爬虫有个清晰的认识

    爬取猫眼电影TOP100榜信息，同时大家也可以进行模仿，想想之前我的一篇文章是怎么爬取电影数据，这里的这个方法又有什么好处呢？这将涉及到基础爬虫架构中的HTML下载器、HTML解析器、数据存储器三大模块：
    
    HTML下载器：利用requests模块下载HTML网页;
    HTML解析器：利用re正则表达式解析出有效数据;
    数据存储器：将有效数据通过文件或者数据库的形式存储起来
    '''