# taobao
爬取taobao部分字段信息


1、items文件
记录爬取字典字段信息

2、spiders下新建蜘蛛文件
用来爬取网站，字段爬取用到的方法
这里主要用到正则和xpath

3、pipelines文件
爬取到的数据插入数据库

4、dbDelete文件
读取IPdaili爬取到数据ip，判断ip是否可用，删除无效ip代理


爬虫使用的是scrapy框架

创建项目：scrapy startproject 项目名

启动项目：scrapy crawl 项目
