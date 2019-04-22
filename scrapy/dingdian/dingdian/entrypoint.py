from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'dingdian'])
'''
在开始之前给大家一个小技巧，Scrapy 默认是不能在 IDE 中调试的，我们在根目录中新建一个py文件叫：entrypoint.py 在里面写入以下内容：
注意！第二行中代码中的前两个参数是不变的，第三个参数请使用自己的spider 的名字也就是刚才你创建项目的名称，
'''