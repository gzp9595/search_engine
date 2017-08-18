from flask import Flask

app = Flask(__name__, static_folder='static_dist', static_url_path='/static')

def initialize():
    from . import route