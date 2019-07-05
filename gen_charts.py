import sys
import datetime as dt
from sentiment_charts import sentiment_charts
from stock_charts import stock_charts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(len(sys.argv))
        raise ValueError
    stock_id = sys.argv[1]
    while True:
        startdate, enddate = sentiment_charts(stock_id)
        stock_charts(stock_id, startdate, enddate)
        print(dt.datetime.now(), " Charts update!")
