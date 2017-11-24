from flask import Flask
import os

from flask import Flask, redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__, static_folder='static_dist', static_url_path='/static')

login_manger = LoginManager()
login_manger.init_app(app)
login_manger.login_view = "login"
login_manger.login_message = "233"


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


app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
