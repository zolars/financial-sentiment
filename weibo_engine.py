import time
import datetime as dt

from WeiboScraper import WeiboScraper

from concurrent.futures import ThreadPoolExecutor


def weibo_engine(query):
    print('Scraper beginning...')

    log = open('./log/WeiboScraper{:_%m_%d_%H_%M}.log'.format(
        dt.datetime.now()), 'a', encoding='utf-8')

    executor = ThreadPoolExecutor(max_workers=8)

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


if __name__ == '__main__':
    weibo_engine("NVIDIA")
