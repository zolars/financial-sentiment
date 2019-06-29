# coding: utf-8
import sys
import gc
import re
import json
import time
import emoji
import requests
import random
import chartify
import datetime
from database import MySQL
from tqdm import tqdm


class WeiboSpider():
    def __init__(self, query_val, log):

        # link and user-agent setting
        # ?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}
        self._url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"
        self._query_val = query_val
        self._log = log

        self.user_agents = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                            'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                            'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                            'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                            'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                            'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

        self._db = MySQL()

    def __del__(self):
        del(self._db)

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

    def catch_data(self, page_id):
        """catch one page's data"""
        headers = {'User-Agent': self.user_agents[random.randrange(
            0, len(self.user_agents))]}
        resp = requests.get(
            url=self._url_template.format(
                self._query_val,
                self._query_val,
                page_id),
            headers=headers)

        card_group = json.loads(resp.text)['data']['cards'][0]['card_group']

        effect_rows = 0
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
            result = [
                mblog['id'],  # weibo id
                "weibo",  # type
                self.clean_text(mblog['text']).strip(
                    '\n').encode("utf8"),  # text
                time,  # time of posts
                str(mblog['user']['id']),  # userid
                mblog['user']['screen_name'],  # username
                mblog['reposts_count'],  # reposts num
                mblog['comments_count'],  # comments num
                mblog['attitudes_count'],  # attitudes num
            ]

            # save to mysql
            try:
                sql = 'insert ignore into result (mid, type, text, time, userid, username, reposts_count, comments_count, attitudes_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);'
                effect_rows += self._db.insert(sql, result)

            except Exception as e:
                print("MySQL ERROR: \t", e)
        try:
            self._log.write(
                "{:%Y-%m-%d %H:%M:%S} Success: Update {} date at page {}.\tURL: {}\n".format(
                    datetime.datetime.now(),
                    effect_rows,
                    page_id,
                    self._url_template.format(
                        self._query_val,
                        self._query_val,
                        page_id)))
        except Exception as e:
            print("Log ERROR: \t", e)

        return effect_rows

    def catch_pages(self, start_page_num, end_page_num, delay):
        """Catch data by keywords and pages"""

        page_id = start_page_num
        effect_rows = 0
        error_list = []
        with tqdm(total=end_page_num - start_page_num) as pbar:
            while page_id <= end_page_num:
                try:
                    effect_rows += self.catch_data(page_id)
                    page_id += 1
                    pbar.update(1)
                    time.sleep(delay)
                except:
                    if page_id not in error_list:
                        error_list.append(page_id)
                        time.sleep(delay)
                    else:
                        try:
                            self._log.write(
                                "{:%Y-%m-%d %H:%M:%S} Error: Data not found at page {}.\tURL: {}\n".format(
                                    datetime.datetime.now(),
                                    page_id,
                                    self._url_template.format(
                                        self._query_val,
                                        self._query_val,
                                        page_id)))
                        except Exception as e:
                            print("Log ERROR: \t", e)
                            page_id += 1
                            pbar.update(1)
