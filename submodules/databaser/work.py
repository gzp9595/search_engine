from flask import Flask
import os

from flask import Flask, redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "233"


class User(UserMixin):
    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id


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


@app.route('/')
@login_required
def index():
    return "login success"


server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

app.config.from_pyfile(config_file)
if os.path.exists(local_config_file):
    app.config.from_pyfile(local_config_file)

app.secret_key = app.config["SECRET"]

app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
