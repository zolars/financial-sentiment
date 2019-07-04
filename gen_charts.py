from sentiment_charts import sentiment_charts
from stock_charts import stock_charts

if __name__ == "__main__":
    startdate, enddate = sentiment_charts("Tesla")
    stock_charts("TSLA", startdate, enddate)
