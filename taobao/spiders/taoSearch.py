# -*- coding: utf-8 -*-

import scrapy
from taobao.items import TaobaoItem
from scrapy.http import Request
import re
import urllib
import ssl

class TaoSpider(scrapy.Spider):
    name = "reTaobao"
    allowed_domains=["taobao.com"]
    start_urls=['http://taobao.com/']


    def parse(self, response):
        key = '小吃'      #变量key存储关键字
        for i in range(0, 1):   #for循环爬取所有页面
            url = 'https://s.taobao.com/search?q=' + str(key) + '&s=' + str(44*i)
            print(url)
            yield Request(url=url, callback=self.page)  #使用scrapy.http里面的Request 来在parse()函数返回（返回一个生成器（yield））一个网页源代码
        pass

    def page(self, response):
        body=response.body.decode('utf-8','ignore') #获取body，二进制解码
        pattam_id='"nid":"(.*?)"'   #正则表达式，商品id
        all_id=re.compile(pattam_id).findall(body)
        #print(all_id)

        for i in range(0,len(all_id)):
            this_id=all_id[i]
            url='https://item.taobao.com/item.htm?id=' + str(this_id)

            yield Request(url=url,callback=self.next)
            pass

        pass

    def next(self,response):
        #print(response.url)
        item=TaobaoItem()

        url=response.url
        pattam_url='https://(.*?).com'
        subdomain=re.compile(pattam_url).findall(url)
        #print(subdomain)

        item["link"]=response.url   #商品链接


        if subdomain[0]!='item.taobao': #判断域名
            # 天猫或天猫超市
            title=response.xpath("//div[@class='tb-detail-hd']/h1/text()").extract()
            pattam_price='"defaultItemPrice":"(.*?)"'    #正则表达式，商品价格
            price=re.compile(pattam_price).findall(response.body.decode('utf-8','ignore'))  #网页源代码中提取
            pattam_id = 'id=(.*?)&'
            this_id=re.compile(pattam_id).findall(url)[0]       #通过url中提取id
        else:
            # 淘宝
            title=response.xpath("//h3[@class='tb-main-title']/@data-title").extract()
            price=response.xpath("//em[@class='tb-rmb-num']/text()").extract()
            pattam_id = 'id=(.*?)$'
            this_id = re.compile(pattam_id).findall(url)[0]


        #print(this_id)

        item["title"]=title
        item["price"]=price

        # # 构造具有评论数量信息的包的网址
        # comment_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=' + str(this_id)
        #
        # context=ssl._create_unverified_context()
        #
        # comment_data = urllib.request.urlopen(comment_url,context=context).read().decode('utf-8', 'ignore')
        #
        # pattam_comment = '"rateTotal":(.*?),"'
        #
        # comment = re.compile(pattam_comment).findall(comment_data)
        #
        #
        # item["comment"]=comment

        #xpath获取失败
        #item["comment"]=response.xpath("//em[@class='J_ReviewsCount']/text()")  #商品评论数目
        #print(title)



        yield item

        pass