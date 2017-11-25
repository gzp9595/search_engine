from flask import Flask
import os
import MySQLdb

from flask import Flask, redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__)


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
        print e
        return None


def execute_write(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except Exception as e:
        print e
        db.rollback()
        return False


server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

app.config.from_pyfile(config_file)
if os.path.exists(local_config_file):
    app.config.from_pyfile(local_config_file)

result = execute_read("""SELECT log_id,query_parameter FROM log WHERE type_number=2""").fetchall()

import json

for a in result:
    id = a[0]
    par = a[1]
    obj = json.loads(par)
    if obj["search_content"][0] == "u":
        obj["search_content"] = eval('u' + '"' + obj["search_content"].replace('u', '\u') + '"')
    par = json.dumps(obj)
    execute_write("""UPDATE log SET query_parameter="%s" WHERE log_id=%d""" % (par,id))
