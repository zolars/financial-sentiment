import sys
import json
import datetime as dt

from flask import Flask, render_template, request
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Page

from tweet_engine import catch_pages_history
from sentiment_chart import gen_sentiment_chart
from stock_chart import gen_stock_chart

from multiprocessing import Process, Queue

app = Flask(__name__, static_folder="templates")
query = ''
stock_id = ''


@app.route("/")
def index():
    return render_template("charts.html")


@app.route("/search", method='GET')
def get_query():
    query = request.args.get('q')


@app.route("/charts", methods=['POST', 'GET'])
def get_charts():
    if request.method == 'POST':
        stock_id = request.form['stock_id']

    else:
        stock_id = request.args.get('stock_id')

    sentiment_chart, startdate, enddate = gen_sentiment_chart(stock_id)
    stock_chart = gen_stock_chart(stock_id, startdate, enddate)
    sentiment_chart.overlap(stock_chart)
    return json.dumps({"chart": json.loads(sentiment_chart.dump_options())})


if __name__ == "__main__":
    app.run(debug=False)
