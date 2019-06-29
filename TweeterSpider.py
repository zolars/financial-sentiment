from twitterscraper import query_tweets
from database import MySQL

if __name__ == '__main__':

    # Save to MySQL
    db = MySQL()
    for tweet in query_tweets("Trump OR Clinton", 10):

        sql = "insert ignore into result (mid, type, text, time, userid, username, reposts_count, comments_count, attitudes_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data = [
            tweet.id,  # mid
            "tweeter",  # type
            tweet.text.strip('\n').encode('utf-8'),  # text
            tweet.timestamp,  # time
            tweet.user,  # userid
            tweet.fullname,  # username
            tweet.retweets,  # reposts_count
            tweet.replies,  # comments_count
            tweet.likes  # attitudes_count
        ]
        db.insert(sql, data)

    del(db)
