from scrapy import cmdline
import datetime as dt


class TwitterScraper():
    def __init__(self, query):
        self.query = query

    def catch_all(self):
        args = ['scrapy', 'crawl', 'TweetScraper',
                '-a', 'query={}'.format(self.query)]
        cmdline.execute(args)

    def catch_realtime(self):
        args = ['scrapy', 'crawl', 'TweetScraper', '-a', 'query={}, since:{:%Y-%m-%d}'.format(
            self.query, dt.datetime.now() - dt.timedelta(days=1))]
        cmdline.execute(args)
