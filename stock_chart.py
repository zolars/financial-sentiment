import datetime as dt
import pandas as pd
import numpy as np
from tiingo import TiingoClient
from pyecharts import options as opts
from pyecharts.charts import Kline
from pyecharts.globals import ThemeType


def kline_datazoom_slider_position(index, data, name) -> Kline:
    c = (
        Kline(init_opts=opts.InitOpts(
            theme=ThemeType.ROMANTIC,
            width="100%",
            height="500px",
        ))
        .add_xaxis(index)
        .add_yaxis(name + "'s K-line", data, yaxis_index=1)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
            title_opts=opts.TitleOpts(title="Stock K-line Graph : " + name),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="line"),
        )
    )
    return c


def gen_stock_chart(item_id, startdate=dt.datetime(2010, 1, 1), enddate=dt.datetime.now()):

    config = {'api_key': '138fd2efede60c466126add93ebf585fc5492f75'}
    client = TiingoClient(config)

    df = client.get_dataframe(item_id,
                              frequency='weekly',
                              startDate='{:%Y-%m-%d}'.format(startdate),
                              endDate='{:%Y-%m-%d}'.format(enddate))
    df = df.loc[:, ['open', 'close', 'low', 'high']]

    data = np.array(df).tolist()

    index = []
    for i in df.index.tolist():
        index.append("{:%Y-%m-%d}".format(i.to_pydatetime()))
    c = kline_datazoom_slider_position(index, data, item_id)
    return c


def out_stock_excel(item_id, startdate=dt.datetime(2010, 1, 1), enddate=dt.datetime.now()):
    file_path = './out/' + item_id + '_stock.xlsx'
    writer = pd.ExcelWriter(file_path)

    config = {'api_key': '138fd2efede60c466126add93ebf585fc5492f75'}
    client = TiingoClient(config)
    df = client.get_dataframe(item_id,
                              frequency='daily',
                              startDate='{:%Y-%m-%d}'.format(startdate),
                              endDate='{:%Y-%m-%d}'.format(enddate))

    df.to_excel(writer, encoding='utf-8')
    writer.save()


if __name__ == "__main__":
    startdate = dt.datetime(2019, 5, 1)
    enddate = dt.datetime.now()
    gen_stock_chart("NVDA", startdate, enddate).render()
