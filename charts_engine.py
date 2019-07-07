import sys
import json
import datetime as dt

from flask import Flask, render_template, request
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Page

from sentiment_chart import gen_sentiment_chart
from stock_chart import gen_stock_chart

app = Flask(__name__, static_folder="templates")


@app.route("/")
def index():
    return render_template("charts.html")


@app.route("/charts", methods=['POST', 'GET'])
def get_charts():
    if request.method == 'POST':
        stock_id = request.form['stock_id']

    else:
        stock_id = request.args.get('stock_id')

    sentiment_chart, startdate, enddate = gen_sentiment_chart(stock_id)
    stock_chart = gen_stock_chart(stock_id, startdate, enddate)
    return json.dumps({"sentiment": json.loads(sentiment_chart.dump_options()), "stock": json.loads(stock_chart.dump_options())})


if __name__ == "__main__":
    app.run()
