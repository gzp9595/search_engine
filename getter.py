#  -*- coding:utf-8 -*-
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
    for x in res["hits"]["hits"]:
        for y in x["_source"]["FLYJ"]:
            if form(y)==(u"中华人民共和国刑法",0,2):
                print x
                gg


if __name__ == '__main__':
    from application import app, initialize

    app.config.from_pyfile(config_file)
    if os.path.exists(local_config_file):
        app.config.from_pyfile(local_config_file)

    from application.elastic import es

    size = 50

    body = {"query": {"match_all": {}}, "_source": ["FLYJ"]}
    cnt = 0

    res = es.search(index=index, doc_type=doc_type, body=body, scroll="20s")
    add_to_set(res)

    while True:
        cnt += 1
        if cnt%100==0:
            print cnt,len(se)
        res = es.scroll(scroll_id=res["_scroll_id"],scroll="20s")
        add_to_set(res)
        if len(res["hits"]["hits"])==0:
            break


    se = list(se)
    se.sort()

