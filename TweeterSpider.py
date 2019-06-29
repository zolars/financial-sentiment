from twitterscraper import query_tweets
import emoji
from database import MySQL


class TweeterSpider():
    def __init__(self):
        # Connect to database
        self._db = MySQL()

    def catch_pages(self):
        for tweet in query_tweets("Trump", 100000):
            sql = "insert ignore into result (mid, type, text, time, userid, username, reposts_count, comments_count, attitudes_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = [
                tweet.id,  # mid
                "tweeter",  # type
                emoji.demojize(tweet.text).strip('\n').encode('utf-8'),  # text
                tweet.timestamp,  # time
                tweet.user,  # userid
                emoji.demojize(tweet.fullname),  # username
                tweet.retweets,  # reposts_count
                tweet.replies,  # comments_count
                tweet.likes  # attitudes_count
            ]
            self._db.insert(sql, data)

        del(self._db)


if __name__ == "__main__":
    try:
        TweeterSpider().catch_pages()
    except:
        pass
