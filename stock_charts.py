import datetime as dt
import pandas as pd
import numpy as np
from tiingo import TiingoClient
from pyecharts import options as opts
from pyecharts.charts import Kline


def kline_datazoom_slider_position(index, data) -> Kline:
    c = (
        Kline()
        .add_xaxis(index)
        .add_yaxis("kline", data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
            title_opts=opts.TitleOpts(title="Stock K-line Graph"),
        )
    )
    return c


def stock_charts(query, startdate=dt.datetime(2010, 1, 1), enddate=dt.datetime.now()):

    config = {'api_key': '138fd2efede60c466126add93ebf585fc5492f75'}
    client = TiingoClient(config)

    df = client.get_dataframe(query,
                              frequency='daily',
                              startDate='{:%Y-%m-%d}'.format(startdate),
                              endDate='{:%Y-%m-%d}'.format(enddate))
    df = df.loc[:, ['open', 'close', 'low', 'high']]

    data = np.array(df).tolist()
    index = df.index.tolist()

    kline_datazoom_slider_position(index, data).render(
        query + "_chart_stock.html")


if __name__ == "__main__":
    startdate = dt.datetime(2019, 5, 1)
    enddate = dt.datetime.now()
    stock_charts("NVDA", startdate, enddate)
