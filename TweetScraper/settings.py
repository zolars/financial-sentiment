# -*- coding: utf-8 -*-

QUERY = 'Apple Inc'
MYSQL_TABLE_NAME = 'AAPL'

# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = '1181689671@qq.com'

# settings for spiders
BOT_NAME = 'TweetScraper'
LOG_LEVEL = 'INFO'
DOWNLOAD_HANDLERS = {'s3': None, }

# Addition timeout
# CLOSESPIDER_TIMEOUT = 30

SPIDER_MODULES = ['TweetScraper.spiders']
NEWSPIDER_MODULE = 'TweetScraper.spiders'

MYSQL_DB_NAME = 'finance'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
ITEM_PIPELINES = {
    # 'TweetScraper.pipelines.SaveToFilePipeline': 100,

    # replace `SaveToFilePipeline` with this to use MySQL
    'TweetScraper.pipelines.SavetoMySQLPipeline': 100,
}

# settings for where to save data on disk
SAVE_TWEET_PATH = './Data/tweet/'
SAVE_USER_PATH = './Data/user/'


# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'TweetScraper.middlewares.ProxyMiddleware': 100,
}
