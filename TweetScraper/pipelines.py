# -*- coding: utf-8 -*-
import os
import json
import emoji

# for spider
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import logging

# for mysql
import pymysql

# for sentiment analysis
from textblob import TextBlob

from TweetScraper.items import Tweet, User
from TweetScraper.utils import mkdirs


logger = logging.getLogger(__name__)


"""
+-----------------+------------+------+-----+---------+-------+
| Field           | Type       | Null | Key | Default | Extra |
+-----------------+------------+------+-----+---------+-------+
| mid             | bigint(20) | NO   | PRI | NULL    |       |
| type            | mediumtext | NO   |     | NULL    |       |
| text            | text       | YES  |     | NULL    |       |
| time            | text       | YES  |     | NULL    |       |
| userid          | text       | YES  |     | NULL    |       |
| username        | text       | YES  |     | NULL    |       |
| reposts_count   | int(11)    | YES  |     | NULL    |       |
| comments_count  | int(11)    | YES  |     | NULL    |       |
| attitudes_count | int(11)    | YES  |     | NULL    |       |
| sentiment       | float      | YES  |     | NULL    |       |
+-----------------+------------+------+-----+---------+-------+
"""


class SavetoMySQLPipeline(object):

    ''' pipeline that save data to mysql '''

    def __init__(self):
        settings = get_project_settings()
        # connect to mysql server
        self._table = settings['QUERY']
        db = settings['MYSQL_DB_NAME']
        user = settings['MYSQL_USER']
        passwd = settings['MYSQL_PASSWORD']
        host = 'localhost'
        port = 3306
        self.conn = pymysql.connect(
            host=host,
            port=port,
            db=db,
            user=user,
            passwd=passwd,
            charset='utf8mb4'
        )
        self._cur = self.conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS {} (
                mid BIGINT NOT NULL, 
                type VARCHAR(255) NOT NULL,
                text VARCHAR(255),
                time VARCHAR(255),
                userid VARCHAR(255),
                username VARCHAR(255),
                reposts_count VARCHAR(255),  
                comments_count VARCHAR(255),
                attitudes_count VARCHAR(255),
                sentiment FLOAT,
                PRIMARY KEY ( mid )
            ) DEFAULT CHARSET=utf8mb4;      
            """.format(self._table)
        self._cur.execute(sql)

    def check_vals(self, item):
        ID = item['ID']
        url = item['url']
        datetime = item['datetime']
        text = item['text']
        user_id = item['user_id']
        username = item['usernameTweet']

        if (ID is None):
            return False
        elif (user_id is None):
            return False
        elif (url is None):
            return False
        elif (text is None):
            return False
        elif (username is None):
            return False
        elif (datetime is None):
            return False
        else:
            return True

    def insert_one(self, item):
        ret = self.check_vals(item)

        if not ret:
            return None

        ID = item['ID']
        user_id = item['user_id']
        text = item['text']
        username = item['usernameTweet']
        datetime = item['datetime']
        nbr_retweet = item['nbr_retweet']
        nbr_favorite = item['nbr_favorite']
        nbr_reply = item['nbr_reply']

        # SENTIMENT ANALYSIS
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity * \
                blob.sentiment.subjectivity * int(nbr_favorite)
        except Exception as err:
            print(err)

        insert_query = 'INSERT IGNORE INTO ' + self._table + \
            ' (mid, type, text, time, userid, username, reposts_count, comments_count, attitudes_count, sentiment) '
        insert_query += 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

        try:
            self._cur.execute(insert_query, (
                ID,
                "tweet",
                emoji.demojize(text),
                datetime,
                user_id,
                emoji.demojize(username),
                nbr_retweet,
                nbr_reply,
                nbr_favorite,
                sentiment
            ))
        except Exception as err:
            logger.info(err)
        else:
            self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            self.insert_one(dict(item))
            logger.debug("Add tweet:%s" % item['url'])


class SaveToFilePipeline(object):
    ''' pipeline that save data to disk '''

    def __init__(self):
        settings = get_project_settings()
        self.saveTweetPath = settings['SAVE_TWEET_PATH']
        self.saveUserPath = settings['SAVE_USER_PATH']
        mkdirs(self.saveTweetPath)  # ensure the path exists
        mkdirs(self.saveUserPath)

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            savePath = os.path.join(self.saveTweetPath, item['ID'])
            if os.path.isfile(savePath):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                self.save_to_file(item, savePath)
                logger.debug("Add tweet:%s" % item['url'])

        elif isinstance(item, User):
            savePath = os.path.join(self.saveUserPath, item['ID'])
            if os.path.isfile(savePath):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update user:%s"%dbItem['screen_name'])
            else:
                self.save_to_file(item, savePath)
                logger.debug("Add user:%s" % item['screen_name'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))

    def save_to_file(self, item, fname):
        ''' input: 
                item - a dict like object
                fname - where to save
        '''
        with open(fname, 'w') as f:
            json.dump(dict(item), f)
