# -*- coding:utf-8 -*-

import time
import os
import sys
import random
import logging
import scrapy
from scrapy.selector import Selector
from book.items import BookItem

mode = 2
sleeptime = 10
proxy = 'http://localhost:8080' if mode == 1 else ''
logger = logging.getLogger('BookDouban')


class bookspider(scrapy.Spider):
    name = 'doubanbook'
    domain = 'https://book.douban.com/'
    # 用于创建目录保存book的封面图片
    cur_dir = '/home/joseph/python/douban/book/book'

    tag = '当代文学'

    # User-Agent池
    userAgent = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) ',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.47 (KHTML, like Gecko)',
    'Chrome/48.1.2524.116  Safari/537.36',
    'Chrome/18.0.1025.166  Safari/535.19',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0']

    # 获取当前tag下的每个页面的url
    def getListUrl(self, tag, pagenum):
        url = self.domain + 'tag/' + tag + '?start=' + str(pagenum * 20)
        return url

    # 设置不同的浏览器headers
    def getRandomHds(self):
        hds_index = random.randint(0, len(self.userAgent)-1)
        header = {
            'User-Agent': self.userAgent[hds_index],
            'Referer': 'https://book.douban.com/',
            'Host': 'www.douban.com',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'}
        return header

    # 设置封面图片存储路径
    def getCoverPath(self, dir):
        path = self.cur_dir
        path = os.path.join(path, dir)
        if not os.path.isdir(path):
            os.mkdir(path)
            #os.chdir(path)
        return path

    # 设置随机等待，默认5s内随机
    def randomSleep(self, seconds = 5):
        time.sleep(random.random() * seconds)
        return True

    # 开始爬取tag首页，主要为获取页数
    # handle the first page of 'tag', get the page count of the 'tag'
    def start_requests(self):
        logger.info('----------start Request-----------')
        self.randomSleep(sleeptime)
        yield scrapy.Request(
            url = self.getListUrl(self.tag, 0),
            # url = self.test_url,
            headers = self.getRandomHds(),
            meta = {
                'proxy':proxy,
                'cookiejar':1
            },
            callback = self.start_spider,
            # callback = self.parse_book,
            errback = self.parse_err
        )

    # 轮询每页
    # start the spider, request each page of booklist
    def start_spider(self, response):
        self.randomSleep(sleeptime)
        selector = Selector(response)
        pagecount = int((selector.xpath('//a[contains(@href, "start=")]/text()').extract())[-2])
        for page_number in range(0, pagecount):
        # for page_number in range(0, 1):
            yield scrapy.Request(
                url = self.getListUrl(self.tag, page_number),
                headers = self.getRandomHds(),
                meta = {
                    'proxy':proxy,
                    'cookiejar':1
                },
                callback = self.parse_bklist,
                errback = self.parse_err
            )

    # 对当前tag下的每页进行处理，获取每本book对应的url
    # handle each page of 'tag', and get the url of every book
    def parse_bklist(self, response):
        self.randomSleep(sleeptime)
        selector = Selector(response)
        base = selector.xpath('//ul[@class="subject-list"]')
        bookurllist = base.xpath('.//div[@class="pic"]/a[contains(@href, "book.douban.com/subject")]/@href').extract()
        for bookurl in bookurllist:
            yield scrapy.Request(
                url = bookurl,
                headers = self.getRandomHds(),
                meta = {
                    'proxy':proxy,
                    'cookiejar':1
                },
                callback = self.parse_book,
                errback = self.parse_err
            )

    # 对单个book页面进行处理
    def parse_book(self, response):
        self.randomSleep(sleeptime)
        item = BookItem()
        selector = Selector(response)
        item['cover'] = (selector.xpath('//div[@id="mainpic"]/a/@href').extract())[0]
        # item['cover'] = (selector.xpath('//a[@class = "nbg"]/@href').extract())[0].replace('mpic', 'lpic')
        # mpic为小图， lpic为大图
        # get the cover image url
        item['book_id'] = response.url.split('/')[-2]
        logger.info('-----process book ' + item['book_id'] + ' -----')
        # 吐槽: 渣豆瓣，书名等信息没有标签，使用xpath根本不好提取！
        # WTF, there are no labels for the information of the book!
        info_block = (selector.xpath('//div[@id="info"]').extract()[0].encode('utf-8').split('<br>'))[:-1]
        # info_block最后一项为空，需要删除，否则会报越界错误
        # the last item of 'info_block' is null, it will raise an error unless delete it.
        item['author'] = ''
        item['subtitle'] = ''
        item['publisher'] = ''
        item['price'] = ''
        item['total_page'] = ''
        item['pub_year'] = ''
        item['isbn'] = ''
        for info_item in info_block:
            info_text = Selector(text = info_item).xpath('string(.)').extract()[0]
            info_text = ''.join(info_text.split())
            if('作者'.decode('utf-8') in info_text):
                item['author'] = info_text[3:]
            elif('副标题'.decode('utf-8') in info_text):
                item['subtitle'] = (info_text[4:])
            elif('出版社'.decode('utf-8') in info_text):
                item['publisher'] = (info_text[4:])
            elif('定价'.decode('utf-8') in info_text):
                item['price'] = info_text[3:]
            elif('页数'.decode('utf-8') in info_text):
                item['total_page'] = info_text[3:]
            elif('出版年'.decode('utf-8') in info_text):
                item['pub_year'] = info_text[4:]
            elif('ISBN' in info_text):
                item['isbn'] = info_text[5:]

        item['title'] = selector.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0]
        item['grade'] = selector.xpath('//strong[@property="v:average"]/text()').extract()[0].encode('utf-8')
        item['gradecount'] = selector.xpath('//a[@class="rating_people"]/span/text()').extract()[0].encode('utf-8')

        read_block = selector.xpath('//div[@id="collector"]')
        item['reading_num'] = (read_block.xpath('.//a[contains(@href, "doings")]/text()').extract()[0])[:-3]
        item['readed_num'] = (read_block.xpath('.//a[contains(@href, "collections")]/text()').extract()[0])[:-3]
        item['preread_num'] = (read_block.xpath('.//a[contains(@href, "wishes")]/text()').extract()[0])[:-3]

        # TODO: 整理数据到相关数据库或表格
        # TODO: reform item to the database
        yield item

        # 请求bookid对应的book的封面图片
        # Request the cover image for the book
        yield scrapy.Request(
            url = item['cover'],
            headers = self.getRandomHds(),
            meta = {
                'proxy':proxy,
                'cookiejar':1
            },
            callback = (lambda response, book_id=item['book_id']: self.parse_cover(response, book_id)),
            errback = self.parse_err
        )

    # 获取book的封面，并保存为图片，图片以book_id命名
    # save the response of the request for the cover image and named by book_id
    def parse_cover(self, response, book_id):
        self.randomSleep(sleeptime)
        os.chdir(self.getCoverPath('cover'))
        with open(str(book_id) + '.jpg', 'wb') as fp:
            fp.write(response.body)

    # 处理异常
    # handle errors
    def parse_err(self, response):
        logger.error('crawl {} failed', response.url)
