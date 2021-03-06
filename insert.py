import logging
import os

insert_path = "/mnt/data/"
index = "law_thulac"
doc_type = "big_data"

server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

if __name__ == '__main__':
    from application import app, initialize

    app.config.from_pyfile(config_file)
    if os.path.exists(local_config_file):
        app.config.from_pyfile(local_config_file)

    from application.processor.insert import dfs_insert

    dfs_insert(index,doc_type,insert_path)
