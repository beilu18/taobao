# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # goods=scrapy.Field()     #商品名称
    # price=scrapy.Field()    #商品价格
    # goodsUrl=scrapy.Field()     #商品url
    # shopName=scrapy.Field()     #店铺名称
    # shopkeeper=scrapy.Field()   #掌柜
    # shopUrl=scrapy.Field()      #店铺url

    title = scrapy.Field()  #商品名
    link = scrapy.Field()   #商品链接
    price = scrapy.Field()  #商品原价
    # comment = scrapy.Field() #评论数目