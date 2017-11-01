import logging
import os

if __name__ == '__main__':
    from application import app, initialize

    initialize()

    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], threaded=True)
