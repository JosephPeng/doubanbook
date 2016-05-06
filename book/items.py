# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    # define the fields for your item here like:
    book_id = scrapy.Field()         # 豆瓣id
    title = scrapy.Field()           # 书名
    subtitle = scrapy.Field()        # 副标题
    cover = scrapy.Field()           # 封面图片
    author = scrapy.Field()          # 作者
    isbn = scrapy.Field()            # ISBN号
    publisher = scrapy.Field()       # 出版社
    price = scrapy.Field()           # 定价
    pub_year = scrapy.Field()        # 出版日期
    total_page = scrapy.Field()      # 总页数
    grade = scrapy.Field()           # 豆瓣评分
    gradecount = scrapy.Field()      # 评分人数
    reading_num = scrapy.Field()     # 正在读人数
    readed_num = scrapy.Field()      # 已读人数
    preread_num = scrapy.Field()     # 想读人数
