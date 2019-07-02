import time
import datetime as dt
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from TweetScraper.spiders.TweetCrawler import TweetScraper
from multiprocessing import Process, Queue


def catch_pages_realtime(query):
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(TweetScraper, query=query)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    query = 'Trump'
    while True:
        try:
            p = Process(target=catch_pages_realtime, args=(query,))
            p.start()
            p.join()
        except Exception as e:
            print(e)
