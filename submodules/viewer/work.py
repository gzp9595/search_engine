from flask import Flask
import os
import MySQLdb

from flask import Flask, redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__)

server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

app.config.from_pyfile(config_file)
if os.path.exists(local_config_file):
    app.config.from_pyfile(local_config_file)

from elasticsearch import Elasticsearch
from elasticsearch import exceptions
from elasticsearch import helpers
from elasticsearch_dsl import Search
import json

es = Elasticsearch(app.config["ELASTIC_SEARCH_ADDRESS"], port=app.config["ELASTIC_SEARCH_PORT"],
                   http_auth=(app.config["ELASTIC_USER"], app.config["ELASTIC_PASS"]))


def get_by_id(index, doc_type, id):
    try:
        return es.get(index=index, doc_type=doc_type, id=id, request_timeout=app.config["ES_TIMEOUT"])
    except exceptions.NotFoundError:
        return None


arr = []
cnt = 0
f = open("list.json", "r")
arr = json.loads(f.readline())
f.close()
for a in range(0, len(arr)):
    data = get_by_id("law", "big_data", arr[a])
    arr[a] = (arr[a], data["_source"]["Title"],len(arr)-a-1)
arr.reverse()

num = 50


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template("main.html", arr=arr)


app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
