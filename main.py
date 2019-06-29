import time
import datetime
from WeiboSpider import WeiboSpider
from concurrent.futures import ThreadPoolExecutor


def demo(target):
    print('Spider beginning...')

    log = open('./log/spider{:_%m_%d_%H_%M}.log'.format(
        datetime.datetime.now()), 'a', encoding='utf-8')

    executor = ThreadPoolExecutor(max_workers=8)

    while True:
        for i in range(0, 180, 20):

            weiboSpider1 = WeiboSpider(target, log)
            executor.submit(weiboSpider1.catch_pages, 0, 5, 0)
            time.sleep(3)

            weiboSpider2 = WeiboSpider(target, log)
            executor.submit(weiboSpider2.catch_pages, i, i + 5, 0)
            time.sleep(3)

            weiboSpider3 = WeiboSpider(target, log)
            executor.submit(weiboSpider3.catch_pages, i + 5, i + 10, 0)
            time.sleep(15)


def stable(target):
    print('Spider beginning...')
    log = open('./log/weibospider{:_%m_%d_%H_%M}.log'.format(
        datetime.datetime.now()), 'a', encoding='utf-8')
    weibospiderBig = WeiboSpider(target, log)
    while True:
        weibospiderBig.catch_pages(0, 5, 0)


if __name__ == '__main__':
    target = '李鑫一'
    demo(target)
