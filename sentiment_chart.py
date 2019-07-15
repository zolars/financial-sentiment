from textblob import TextBlob
import pandas as pd
import pymysql
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType

from stock_chart import gen_stock_chart


class MySQL:
    def __init__(self, table):
        # Connect to MySQL
        self._conn = pymysql.connect(
            host='localhost',  # mysql server address
            port=3306,  # port num
            user='root',  # username
            passwd='123456',  # password
            db='finance',
            charset='utf8mb4',
        )
        self._cur = self._conn.cursor()
        self._table = table

    def __del__(self):
        self._conn.close()

    def searchSentiment(self):
        sql = 'select time, sentiment from ' + self._table   # + ' where sentiment!=0'
        df = pd.read_sql(sql, con=self._conn)
        return df

    def searchTweets(self):
        sql = 'select time, sentiment from ' + self._table + ' where sentiment!=0'
        df = pd.read_sql(sql, con=self._conn)
        return df


def line_smooth(index, data, name) -> Line:
    c = (
        Line(init_opts=opts.InitOpts(
            theme=ThemeType.ROMANTIC,
            # width="100%",
            height="500px",
        ))
        .add_xaxis(index)
        .add_yaxis("Sentiment value", data, is_smooth=True, is_connect_nones=True, yaxis_index=0)
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="Stock K-line",
                is_scale=True,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                name="Sentiment Value",
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1))),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
            title_opts=opts.TitleOpts(title="Sentiment Analysis : " + name),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="line"),
        )
    )
    return c


def gen_sentiment_chart(table):
    df = MySQL(table).searchSentiment()
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df = df.resample('w').mean()
    df = df.fillna(0)
    data = np.around(np.array(df), decimals=2).tolist()
    index = []
    for i in df.index.tolist():
        index.append("{:%Y-%m-%d}".format(i.to_pydatetime()))
    sentiment_chart = line_smooth(index, data, table)
    return sentiment_chart, df.index[0].to_pydatetime(), df.index[-1].to_pydatetime()


def getTweets():
    pass


if __name__ == "__main__":
    sentiment_chart, startdate, enddate = gen_sentiment_chart("mmm")
    stock_chart = gen_stock_chart("mmm", startdate, enddate)
    sentiment_chart.overlap(stock_chart)
    sentiment_chart.render()
