# pylint: disable=E1101

import time
import datetime as dt
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from scrapy.utils.log import configure_logging
from TweetScraper.spiders.TweetCrawler import TweetScraper
from multiprocessing import Process, Queue


def catch_pages_history():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())
    runner.crawl(TweetScraper, lang='en', top_tweet=True)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def catch_pages_realtime():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner(
        get_project_settings().set("CLOSESPIDER_TIMEOUT", 30))
    runner.crawl(TweetScraper, lang='en', top_tweet=False)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def tweet_engine():
    p = Process(target=catch_pages_history)
    p.start()

    while True:
        if not p.is_alive():
            try:
                p.start()
            except Exception as err:
                print(err)
        try:
            p1 = Process(target=catch_pages_realtime)
            p2 = Process(target=catch_pages_realtime)
            p1.start()
            time.sleep(15)
            p2.start()
            p1.join()
            p2.join()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    catch_pages_history()
    # tweet_engine('NYSE:MMM')
