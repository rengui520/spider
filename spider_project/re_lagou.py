#coding:utf-8
#构造 html下载器，利用 requests 模块下载HTML网页
import requests
from requests.exceptions import RequestException  #捕获异常
import re
import json

def get_one_page(url):
	try:
		headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
		response = requests.get(url,headers=headers)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

#构造 html 解析器，利用 re 正则表达式解析出有效数据
def parse_one_page(html):
	pattern = re.compile(
       '<li.*?data-positionname="(.*?)".*?<em>(.*?)'
   +'</em>.*?money">(.*?)</span>(.*?)</div>.*?'
   +'company.*?<a.*?>(.*?)</a>.*?industry">(.*?)</div>.*?</li>',
       re.S)  # 起始符，结束符都要匹配一下
	items = re.findall(pattern, html)
	for item in items:
		yield {
     'title': item[0],
     'site': item[1],
     'money': item[2],
     'experience': item[3].strip()[14:], #strip()方法把换行符去掉，然后构造切片把前边14个字符去掉
     'name': item[4],
     'assets': item[5].strip()
   }
#在函数中本来该 return 的地方用 yield ，如果用 return ，在第一轮循环就会跳出，结果文件只会有一部电影。
#如果用 yield ，函数返回的就是一个生成器，而生成器作为一种特殊的迭代器，可以用 for—in 方法，一次一次的把 yield 拿出来；

#构造数据存储器，将有效数据通过文件或者数据库的形式存储起来
def write_to_file(content):
	with open('E:/wenben/20190123.txt', 'a', encoding='utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n')
		f.close()
# 为什么 ensure_ascii=False 原因是 json 默认是以 ASCII 来解析 code 的，由于中文不在 ASCII 编码当中，因此就不让默认 ASCII 生效；
# json.dumps() 的作用：用于将 dict 类型的数据转成 str ,因为如果直接将 dict 类型的数据写入 json 文件中会发生报错，因此在将数据写入时需要用到该函数;
# 要写入特定编码的文本文件，请给 open() 函数传入 encoding 参数，将字符串自动转换成指定编码。

#接下来就是构造主函数，初始化各个模块，传入入口 URL ，按照运行流程执行上面三大模块
def main():
	url = 'https://www.lagou.com/zhaopin/Python/1/?city=深圳'
	urls = ['https://www.lagou.com/zhaopin/Python/{}/?city=深圳'.format(str(i)) for i in range(1,31)]
	for url in urls:
		html = get_one_page(url)
		for item in parse_one_page(html):
			print(item)
			write_to_file(item)

if __name__ == '__main__':
	main()

#本程序中介绍了基础爬虫架构主要的的三个模块（HTML下载器、HTML解析器、数据存储器），
#无论大型还是小型爬虫都不会脱离这三个模块，通过这个小小的练习对整个爬虫有个清晰的认识
