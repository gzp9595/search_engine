from application import app

from elasticsearch import Elasticsearch
import json

es = Elasticsearch(app.config["ElASTIC_SEARCH_ADDRESS"], port=app.config["ELASTIC_SEARCH_PORT"])


def insert_doc(index, doc_type, doc):
    es.index(index=index, doc_type=doc_type, body=json.dumps(doc), id=doc["doc_name"])


def get_doc_byid(index, doc_type, id):
    return es.get(index=index, doc_type=doc_type, id=id, request_timeout=app.config["ES_TIMEOUT"])['_source']


def search_doc(index, doc_type, body):
    return es.search(index=index, doc_type=doc_type, body=body, request_timeout=app.config["ES_TIMEOUT"])["hits"]


def get_count(index, doc_type):
    return es.count(index=index, doc_type=doc_type, request_timeout=app.config["ES_TIMEOUT"])


def remove_all(index, doc_type):
    return es.delete_by_query(index=index, doc_type=doc_type, body="{}")


def get_by_id(index, doc_type, id):
    return es.get(index=index, doc_type=doc_type, id=id, request_timeout=app.config["ES_TIMEOUT"])


def delete_index(index):
    return es.delete(index=index)
