# -*- coding: utf-8 -*-
#import scrapy
import json
from zhihuuser.items import UserItem
from scrapy import Spider, Request

#class ZhihuSpider(scrapy.Spider):
class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'   #用户的 url ，链接在用户名开头的文件里 如allenzhang?include=allow_message...。不过检查第一页的元素时，跳出的是第二页的内容，所以只需点击下一页并点击对应的元素即可跳出相应的文件。
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'  #用户文件名称的 include。

    # 要获取用户的关注列表，.其中user就是该用户的url_token，include是固定的查询参数，offset是分页偏移量，limit是一页取多少个。
    # 要获取用户的详细信息，其中user就是该用户的url_token，include是查询参数。

    start_user = 'stormzhang'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include{include}&offset={offset}&limit={limit}'   #关注列表的 url 。在文件followees?include=data...中。
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include{include}&offset={offset}&limit={limit}'  # 粉丝列表的 url 。在文件followees?include=data...中。
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    # include是一些获取关注的人的基本信息的查询参数，包括回答数、文章数等等。
    #
    # offset是偏移量，我们现在分析的是第3页的关注列表内容，offset当前为40。
    #
    # limit为每一页的数量，这里是20，所以结合上面的offset可以推断，当offset为0时，获取到的是第一页关注列表，当offset为20时，获取到的是第二页关注列表，依次类推。

    # 可以看到有data和paging两个字段，data就是数据，包含20个内容，这些就是用户的基本信息，也就是关注列表的用户信息。
    # paging里面又有几个字段，is_end表示当前翻页是否结束，next是下一页的链接，所以在判读分页的时候，我们可以先利用is_end判断翻页是否结束，然后再获取next链接，请求下一页。
    #
    # 这样我们的关注列表就可以通过接口获取到了。

    def start_requests(self):
        #url = 'https://www.zhihu.com/api/v4/members/han-dong-ran/publications?include=data%5B*%5D.cover%2Cebook_type%2Ccomment_count%2Cvoteup_count&offset=0&limit=5'
        #url = 'https://www.zhihu.com/api/v4/members/stormzhang/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=40&limit=20'
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query ), self.parse_user)  #回调函数 。获取用户的基本信息，即本身
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20), callback=self.parse_follows)  #获取关注列表
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20), callback=self.parse_followers)  #获取粉丝列表

    def parse_user(self, response):   #解析 user 自己的详细信息。
        #pass
        result = json.loads(response.text)  #所以在解析方法里面我们解析得到的response内容，然后转为json对象，然后依次判断字段是否存在，赋值就好了。
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item   #得到item后通过yield返回

        #再进行层层选取。再获取关注人所关注的 用户列表 和 粉丝列表 。所以我们需要再重新发起一个获取 关注/粉丝 列表的request
        yield Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query, limit=20, offset=0),self.parse_follows)
        yield Request(self.followers_url.format(user=result.get('url_token'), include=self.followers_query, limit=20, offset=0),self.parse_followers)

    def parse_follows(self, response):  #完成递归函数的实现。两件事，1.对关注列表进行解析，解析完后获取用户的 url_token，再重新对用户发起请求，解析用户的url，再进行调用。
        results = json.loads(response.text)  #2.处理分页，判断paging内容，获取下一页关注列表。判断分页是否已经结束，如果没有结束，继续获取下一页。（next信息）

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:   #判断是否是最后一页
            next_page = results.get('paging').get('next')  #获取下一页链接
            yield Request(next_page, self.parse_follows)  #回调函数


    def parse_followers(self, response):  #完成递归函数的实现
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_query), self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:   #判断是否是最后一页
            next_page = results.get('paging').get('next')  #获取下一页链接
            yield Request(next_page, self.parse_followers)  #回调函数



# 通过以上的spider，我们实现了如上逻辑：
#
# start_requests方法，实现了第一个大V用户的详细信息请求还有他的粉丝和关注列表请求。
#
# parse_user方法，实现了详细信息的提取和粉丝关注列表的获取。
#
# paese_follows，实现了通过关注列表重新请求用户并进行翻页的功能。
#
# paese_followers，实现了通过粉丝列表重新请求用户并进行翻页的功能。






















