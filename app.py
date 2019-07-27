import json
import datetime as dt

from flask import Flask, render_template, request
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts import options as opts
from pyecharts.charts import Page

from tweet_engine import catch_pages_history, catch_pages_realtime
from sentiment_chart import gen_sentiment_chart, out_sentiment_excel
from stock_chart import gen_stock_chart, out_stock_excel

from multiprocessing import Process, Queue

app = Flask(__name__, static_folder="templates")
item_id_set = []
item_type_list = []
query_list = []
pool = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=['GET'])
def get_query():
    query = request.args.get('q')
    return '''
            <body style="background:rgb(212, 213, 236);">
            <br>
            <br>
            <br>
            <h2 align="center">Your query is:</h2>
            <h1 align="center" style="font-family: Yahei">
            ''' + query + '''
            </h1>
            <h2 align="center">Copy this to the text area.</h2>
            </body>
            '''


@app.route("/scrapers", methods=['GET'])
def changeScrapers():
    global item_id_set, query_list

    op = request.args.get('op')

    if op == 'get':
        request_item_type = request.args.get('item_type')
        result = {}
        for (item_id, item_type, query) in zip(item_id_set, item_type_list, query_list):
            if item_type == request_item_type:
                result[item_id] = query
        return json.dumps(result)

    elif op == 'add':
        item_id = request.args.get('item_id')
        query = request.args.get('query')
        item_type = request.args.get('item_type')
        if len(item_id_set) >= 6:
            return 'Error: The amount of scrapers is up to 6.'
        elif item_id in item_id_set:
            return 'Error: The item_id is duplicated.'
        else:
            item_id_set.append(item_id)
            item_type_list.append(item_type)
            query_list.append(query)
            if item_type == 'Stock':
                p = Process(target=catch_pages_history, args=(query, item_id))
                pool.append(p)
            elif item_type == 'Crypto':
                p = Process(target=catch_pages_realtime, args=(query, item_id))
                pool.append(p)
            pool[-1].start()
            return 'success'

    elif op == 'remove':
        item_id = request.args.get('item_id')
        if item_id not in item_id_set:
            return 'Error: The item_id is not existed.'
        else:
            index = item_id_set.index(item_id)
            del item_id_set[index]
            del item_type_list[index]
            del query_list[index]
            pool[index].terminate()
            del pool[index]
            return 'success'


@app.route("/charts", methods=['POST', 'GET'])
def get_charts():
    if request.method == 'POST':
        item_id = request.form['item_id']

    else:
        item_id = request.args.get('item_id')

    sentiment_chart, startdate, enddate = gen_sentiment_chart(item_id)
    stock_chart = gen_stock_chart(item_id, startdate, enddate)
    sentiment_chart.overlap(stock_chart)
    return json.dumps({"chart": json.loads(sentiment_chart.dump_options())})


@app.route("/export", methods=['POST', 'GET'])
def export_charts():
    if request.method == 'POST':
        item_id = request.form['item_id']

    else:
        item_id = request.args.get('item_id')
    out_sentiment_excel(item_id)
    sentiment_chart, startdate, enddate = gen_sentiment_chart(item_id)
    out_stock_excel(item_id, startdate, enddate)
    stock_chart = gen_stock_chart(item_id, startdate, enddate)
    sentiment_chart.overlap(stock_chart)
    return json.dumps({"chart": json.loads(sentiment_chart.dump_options())})


if __name__ == "__main__":
    app.run(debug=False)
