from sentiment_charts import sentiment_charts
from stock_charts import stock_charts

if __name__ == "__main__":
    while True:
        startdate, enddate = sentiment_charts("NYSE:MMM")
        stock_charts("MMM", startdate, enddate)
