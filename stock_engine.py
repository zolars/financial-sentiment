import datetime as dt
import pandas as pd
import numpy as np
import pandas_datareader as pdr
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
            title_opts=opts.TitleOpts(title="Kline-DataZoom-slider-Position"),
        )
    )
    return c


def stock_engine(query):
    df = pdr.get_data_tiingo(query,
                             api_key='138fd2efede60c466126add93ebf585fc5492f75')
    df = df.loc[:, ['open', 'close', 'low', 'high']]
    data = np.array(df).tolist()
    index = df.index.tolist()

    kline_datazoom_slider_position(index, data).render()


if __name__ == "__main__":
    stock_engine("FB")
