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
f = open("id.txt", "r")
for line in f:
    content = line[:-1].split(" ")
    if len(content)>3:
        print content
        gg
    #data = get_by_id("law","big_data",content[0])["_source"]["Title"]
    #print content[0]
    arr.append([content[0], int(content[1]), content[2].decode("utf8"),cnt])
    cnt += 1
f.close()


@app.route('/output')
def output():
    f = open("idf.txt", "w")
    for (x, y, z,t) in arr:
        print >> f, x, y, z.encode("utf8")
    f.close()
    return "gg"


num = 50


@app.route('/', methods=['GET', 'POST'])
def index():
    page = 0
    if "page" in request.args:
        page = int(request.args["page"])
    if "score_"+arr[page*num][0] in request.form:
        for a in range(0, num):
            sc = int(request.form["score_" + arr[page*num+a][0]])
            if sc != -1:
                arr[page * num + a][1] = sc

    temp = arr[page * num:min((page + 1) * num,len(arr))]

    return render_template("main.html", arr=temp,page=page)


app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
