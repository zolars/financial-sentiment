import sys
import datetime as dt
from sentiment_chart import sentiment_chart
from stock_chart import stock_chart

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(len(sys.argv))
        raise ValueError
    stock_id = sys.argv[1]
    while True:
        startdate, enddate = sentiment_chart(stock_id)
        stock_chart(stock_id, startdate, enddate)
        print(dt.datetime.now(), " Charts update!")
