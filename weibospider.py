# coding: utf-8
import sys
import re
import json
import time
import emoji
import requests
import pymysql
import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


class Weibospider():
    def __init__(self, query_val):
        self.url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"
        self.query_val = query_val
        self.log = open('weibospider{:_%m_%d_%H_%M}.log'.format(
            datetime.datetime.now()), 'a', encoding='utf-8')

    def clean_text(self, text):
        """clean tags or emoji of texts"""

        dr = re.compile(r'(<)[^>]+>', re.S)
        dd = dr.sub(r'', text)
        dr = re.compile(r'#[^#]+#', re.S)
        dd = dr.sub(r'', dd)
        dr = re.compile(r'@[^ ]+ ', re.S)
        dd = dr.sub(r'', dd)
        dd = emoji.demojize(dd)
        return dd.strip()

    def catch_data(self, query_val, page_id, cur):
        """catch one page's data"""
        resp = requests.get(self.url_template.format(
            query_val, query_val, page_id))

        # print(self.url_template.format(query_val, query_val, page_id))

        card_group = json.loads(resp.text)['data']['cards'][0]['card_group']

        effect_row = 0
        for card in card_group:
            mblog = card['mblog']

            time = mblog['created_at']
            sendtime = datetime.datetime.now()
            delta = datetime.timedelta(seconds=0)
            if '小时' in time:
                delta = datetime.timedelta(hours=int(time.replace('小时前', '')))
            elif '分钟' in time:
                delta = datetime.timedelta(
                    minutes=int(time.replace('分钟前', '')))
            elif '刚刚' in time:
                pass
            else:
                if len(time) is 5:
                    sendtime = datetime.datetime.strptime(
                        "{:%Y-}".format(sendtime) + time, '%Y-%m-%d')
                else:
                    sendtime = datetime.datetime.strptime(time, '%Y-%m-%d')

            time = "{:%Y-%m-%d %H:%M}".format(sendtime - delta)

            # save to mysql
            sql_insert = (
                'insert ignore into result (mid, text, time, userid, username, reposts_count, comments_count, attitudes_count) values ({},"{}","{}","{}","{}",{},{},{}); '.format(
                    mblog['id'],  # weibo id
                    self.clean_text(mblog['text']),  # text
                    time,  # time of posts
                    str(mblog['user']['id']),  # userid
                    mblog['user']['screen_name'],  # username
                    mblog['reposts_count'],  # reposts num
                    mblog['comments_count'],  # comments num
                    mblog['attitudes_count'],  # attitudes num
                )).strip('\n')
            sql_insert = sql_insert.encode("utf8")
            effect_row += cur.execute(sql_insert)

        self.log.write(
            "{:%Y-%m-%d %H:%M:%S} Success: Update {} date at page {}.\tURL: {}\n".format(
                datetime.datetime.now(),
                effect_row,
                page_id,
                self.url_template.format(
                    self.query_val, self.query_val, page_id)
            ))

        return effect_row

    def catch_pages(self, start_page_num, end_page_num, delay):
        """Catch data by keywords and pages"""

        # 连接数据库
        db = pymysql.connect(
            host='localhost',  # mysql server address
            port=3306,  # port num
            user='root',  # username
            passwd='root',  # password
            db='weibo',
            charset='utf8',
        )
        cur = db.cursor()
        effect_row = 0
        for page_id in range(start_page_num, end_page_num):
            try:
                effect_row += self.catch_data(self.query_val, page_id, cur)
                time.sleep(delay)
            except:
                self.log.write(
                    "{:%Y-%m-%d %H:%M:%S} Error: Data not found at page {}.\tURL: {}\n".format(
                        datetime.datetime.now(),
                        page_id,
                        self.url_template.format(
                            self.query_val, self.query_val, page_id)
                    ))
                time.sleep(delay)

        db.commit()
        db.close()


def demo(target):
    print('Spider beginning...')
    weibospiderBig = Weibospider(target)
    executor = ThreadPoolExecutor(max_workers=8)

    while True:
        print('Epoch begin...')
        for i in range(210, 0, -30):
            executor.submit(weibospiderBig.catch_pages, i, i + 15, 0)
            executor.submit(weibospiderBig.catch_pages, i + 15, i + 30, 0)
            time.sleep(10)


if __name__ == '__main__':
    target = '吴亦凡'
    demo(target)
    # stable(target)
