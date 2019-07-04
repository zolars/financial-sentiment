# %%
from textblob import TextBlob
import pandas as pd
import pymysql
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line


class MySQL:
    def __init__(self):
        # Connect to MySQL
        self._conn = pymysql.connect(
            host='localhost',  # mysql server address
            port=3306,  # port num
            user='root',  # username
            passwd='root',  # password
            db='finance',
            charset='utf8',
        )
        self._cur = self._conn.cursor()

    def __del__(self):
        self._conn.close()

    def search(self):
        sql = 'select time, sentiment from result'
        df = pd.read_sql(sql, con=self._conn)
        return df


def line_smooth(index, data) -> Line:
    c = (
        Line()
        .add_xaxis(index)
        .add_yaxis("Sentiment value", data, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Sentiment Analysis"))
    )
    return c


def sentiment_charts():
    df = MySQL().search()
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df = df.resample('B').mean()
    data = np.around(np.array(df), decimals=2).tolist()
    index = df.index.tolist()
    line_smooth(index, data).render("chart_sentiment.html")
    return df


if __name__ == "__main__":
    print(sentiment_charts())
