# doubanbook
A spider for book.douban
'豆瓣读书'爬虫

# Introduction(简介)
- Based on Python2 and scrapy
- 基于 Python2 和 scrapy
- Download the book informations from book.douban.com
- 从 book.douban.com 抓取 book 的相关信息
- Output the book informations to a json file
- 输出 book 的相关信息到 json 文件

# Basic Usage(使用)
- Install the python2 and scrapy(make sure those works)
- 安装 python2 和 scrapy (确保它们能够正常工作)
- Reedit the var 'tag' in 'book/spider/bookspider.py' to the tag you want to scrape
- 编辑 'book/spider/bookspider.py' 文件下的 'tag' 变量，替换为你想要抓取的 tag 的名称
- Reedit the var 'cur_dir' in 'book/spider/bookspider.py' to change the dir for saving images
- 编辑 'book/spider/bookspider.py' 文件下的 'cur_dir' 变量，用来保存 book 的封面图片
- Run 'scrapy crawl doubanbook' in terminal at 'book' dir
- 在 'book' 路径下，在终端运行 'scrapy crawl doubanbook'

# [TODOs 2016/05/06]
- Save the data to database
- 保存抓取的数据到数据库
- Change the ip and proxy for not been banned
- 增加代理支持
- Output the results to xls file
- 输出抓取的结果到表格文件
