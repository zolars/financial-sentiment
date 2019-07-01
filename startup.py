import time
import datetime as dt

from WeiboScraper import WeiboScraper
from TwitterScraper import TwitterScraper

from concurrent.futures import ThreadPoolExecutor


def demo(query):
    print('Scraper beginning...')

    log = open('./log/WeiboScraper{:_%m_%d_%H_%M}.log'.format(
        dt.datetime.now()), 'a', encoding='utf-8')

    executor = ThreadPoolExecutor(max_workers=10)
   # Startup tweetScraper
    twitterScraper = TwitterScraper(query)
    executor.submit(twitterScraper.catch_all)

    while True:

        # Startup weiboScraper
        for i in range(1, 180, 20):
            weiboScraper1 = WeiboScraper(query, log)
            executor.submit(weiboScraper1.catch_pages, 1, 5, 0)
            time.sleep(10)

            weiboScraper2 = WeiboScraper(query, log)
            executor.submit(weiboScraper2.catch_pages, i, i + 5, 0)
            time.sleep(10)

            weiboScraper3 = WeiboScraper(query, log)
            executor.submit(weiboScraper3.catch_pages, i + 5, i + 10, 0)
            time.sleep(10)

            executor.submit(twitterScraper.catch_realtime)


if __name__ == '__main__':
    query = 'Billie Eilish'
    demo(query)
