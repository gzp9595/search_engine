from flask import Flask
import os

from flask import Flask, redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)

login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = "login"
login_manger.login_message = "233"

@app.route('/login/', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        pwd = request.form.get("pwd")
        if name != app.config["NAME"] or pwd != app.config["PWD"]:
            flash('GG')
        else:
            login_user(name, remember=True)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('login_success'))
    return render_template("login.html")

@app.route('/')
@login_required
def index():
    return "gg"


server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

app.config.from_pyfile(config_file)
if os.path.exists(local_config_file):
    app.config.from_pyfile(local_config_file)


app.secret_key = app.config["SECRET"]


app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
