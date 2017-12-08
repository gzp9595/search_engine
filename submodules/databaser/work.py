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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "233"

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


class User(UserMixin):
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id


def execute_read(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    try:
        cursor.execute(sql)
        return cursor
    except Exception as e:
        print(e)
        return None


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.set_id(user_id)
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        pwd = request.form.get("pwd")
        if name != app.config["NAME"] or pwd != app.config["PWD"]:
            flash('GG')
        else:
            user = User()
            user.set_id(name)
            login_user(user, remember=True)
            return redirect("/")
    return render_template("login.html")


column_name = {}
column_name["user"] = ["user_id", "username", "nickname", "rest_money", "phone_number", "mail", "user_type",
                       "user_photo", "user_org", "user_identity", "user_code", "create_time", "last_modified"]
column_name["log"] = ["log_id", "username", "create_time", "type_number", "doc_id", "query_paramenter", "user_ip"]
column_name["code"] = ["code", "leveltype", "create_time"]
column_name["usertype"] = ["type_id", "search_perminute", "search_perday", "view_perminute", "view_perday"]
column_name["favorite"] = ["favoite_id", "create_time", "usernmae", "favorite_name"]
column_name["favorite_item"] = ["item_id", "favorite_id", "doc_id", "create_time"]


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        where_to_search = request.form.get("where_to_search")
        condition = ""
        if "condition" in request.form:
            condition = request.form.get("condition")
        sql = """SELECT * FROM %s""" % where_to_search
        if condition != "":
            sql = sql + " WHERE " + condition
        print(sql)

        cursor = execute_read(sql)
        if cursor is None:
            return render_template("main.html", error=True, args=request.form)
        result = cursor.fetchall()
        if where_to_search == "user":
            gg_result = []
            for a in range(0, len(result)):
                ff_result = []
                for b in result[a]:
                    ff_result.append(b)
                gg_result.append(ff_result[0:2] + ff_result[3:len(result[a])])
            result = gg_result
        if True:
            gg_result = []
            for a in range(0, len(result)):
                ff_result = []
                for b in result[a]:
                    if isinstance(b, str):
                        b = b.decode("utf8")
                    ff_result.append(b)
                gg_result.append(ff_result)
            result = gg_result

        if where_to_search == "log":
            for a in range(0, len(result)):
                if result[a][3] == 2:
                    gg_result = get_by_id("law","big_data",result[a][4])
                    if gg_result is None:
                        continue
                    result[a][4] = """
                        <a href="powerlaw.ai:8888/document?id=%s" target="_blank?">%s</a>
                    """ % (result[a][4],gg_result["_source"]["Title"])

        return render_template("main.html", result=result, column_name=column_name[where_to_search], args=request.form)

    else:
        return render_template("main.html", args={"where_to_search": "user", "condition": ""})



app.secret_key = app.config["SECRET"]

app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
