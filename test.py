from tweet_engine import catch_pages_history, catch_pages_realtime
from multiprocessing import Process, Queue

if __name__ == '__main__':
    p = Process(target=catch_pages_realtime, args=("Trump", "Trump"))

    p.start()
