from application import app

from elasticsearch import Elasticsearch
from elasticsearch import exceptions
from elasticsearch import helpers
import json

es = Elasticsearch(app.config["ELASTIC_SEARCH_ADDRESS"], port=app.config["ELASTIC_SEARCH_PORT"])

scroll_id = ""


def insert_doc(index, doc_type, doc):
    es.index(index=index, doc_type=doc_type, body=json.dumps(doc), id=doc["doc_name"],
             request_timeout=app.config["ES_TIMEOUT"])


def get_doc_byid(index, doc_type, id):
    return es.get(index=index, doc_type=doc_type, id=id, request_timeout=app.config["ES_TIMEOUT"])['_source']


def search_doc(index, doc_type, body):
    res =  es.search(index=index, doc_type=doc_type, body=body, request_timeout=app.config["ES_TIMEOUT"], scroll="10m")
    for x in res:
        if x!="hits":
            print x,res[x]
    return res["hits"]


def scan_doc(index, doc_type, body):
    print "gg"
    print body
    res = list(helpers.scan(es, request_timeout=app.config["ES_TIMEOUT"], query=body, index=index, doc_type=doc_type,size=1,preserve_order=False))
    print "gg"
    print res
    return res


def get_count(index, doc_type):
    return es.count(index=index, doc_type=doc_type, request_timeout=app.config["ES_TIMEOUT"])


def remove_all(index, doc_type):
    return es.delete_by_query(index=index, doc_type=doc_type, body="{}")


def get_by_id(index, doc_type, id):
    try:
        return es.get(index=index, doc_type=doc_type, id=id, request_timeout=app.config["ES_TIMEOUT"])
    except exceptions.NotFoundError:
        return None


def update_by_id(index, doc_type, id, doc):
    if get_by_id(index, doc_type, id) is None:
        insert_doc(index, doc_type, doc)
    else:
        es.update(index=index, doc_type=doc_type, id=id, body={"doc": doc})


def delete_index(index):
    return es.delete(index=index)
