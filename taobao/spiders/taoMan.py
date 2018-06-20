# -*- coding: utf-8 -*-
import scrapy
from taobao.items import TaobaoItem

class GoodsSpider(scrapy.Spider):
    name = 'mWear'

    allowed_domains=["taobao.com/"]
    start_urls=('https://s.taobao.com/list?spm=a21bo.2017.201867-links-0.38.2c2a11d9Cz8zU3&q=T%E6%81%A4&cat=50344007&style=grid&seller_type=taobao&sort=sale-desc')

    #统计数目
    count=0

    def parse(self, response):

        GoodsSpider.count+=1

        divs=response.xpath("//*[@id='listsrp-itemlist']/div/div/div[1]/div")  #商品列表xpath
        if not divs:    #判断是否在这divs中，不在记录url
            self.log("list page error--%s"%response.url)


        for div in divs[1:59]:

            item=TaobaoItem()
            #商品价格
            item["price"]=div.xpath("div[3]/div[1]/div[1]/strong")[0].extract()
            #商品链接url
            pre_goods_url=div.xpath("div[3]/div[2]/a/@href")[0].extract()

            #判断url中是否有https，没有就补上
            item["goodsUrl"]=pre_goods_url if "https:" in pre_goods_url else ("https:"+pre_goods_url)

            yield scrapy.Request(url=item["goodsUrl"],meta={'item':item},callback=self.parse_detail(),dont_filter=True)

    def parse_detail(self,response):
        div=response.xpath("//*[@id='J_ShopInfo']")

        if not div:
            self.log('detail page serror --%s'%response.url)

        item=response.meta['item']

        #店铺名称
        item['shopName']=div.xpath("div/div[1]/div[1]/dl/dd/strong/a")[0].extract().strip()
        #掌柜
        item['shopkeeper']=div.xpath("div/div[1]/div[3]/dl/dd/a")[0].extract().strip()
        #店铺url
        item['shopUrl']=div.xpath("div/div[3]/a[1]/@href")[0].extract()

        #商品名称
        item['goods']=response.xpath("//*[@id='J_Title']/h3")[0].extract().strip()

        yield item
