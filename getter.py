import os
import config
import json

index = "law"
doc_type = "big_data"
dir_path = "/mnt/new/"

server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

se = set()


def form(x):
    return (x["law_name"], x["tiao_num"], x["kuan_num"])


def add_to_set(res):
    for x in res["hits"]["hits"]["_soucre"]:
        res.append(form(x["FLYJ"]))


if __name__ == '__main__':
    from application import app, initialize

    app.config.from_pyfile(config_file)
    if os.path.exists(local_config_file):
        app.config.from_pyfile(local_config_file)

    from application.elastic import es

    size = 50

    body = {"query": {"match_all": {}}, "_source": ["FLYJ"]}

    res = es.search(index=index, doc_type=doc_type, body=body, scroll="10m")
    add_to_set(res)

    while True:
        res = es.scroll(scroll_id=res["_scroll_id"])
        add_to_set(res)
        print len(se)
