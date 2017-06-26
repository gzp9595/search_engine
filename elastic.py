from elasticsearch import Elasticsearch
import config

es = Elasticsearch(config.ElASTIC_SEARCH_ADDRESS, port=config.ELASTIC_SEARCH_PORT)


def insert_doc(index, doc_type, doc):
    # print doc
    es.index(index=index, doc_type=doc_type, body=doc)


def get_doc_byid(index, doc_type, id):
    return es.get(index=index, doc_type=doc_type, id=id)['_source']


def search_doc(index, doc_type, body):
    return es.search(index=index, doc_type=doc_type, body=body)["hits"]


def get_count(index, doc_type):
    return es.count(index=index, doc_type=doc_type)


def remove_all(index, doc_type):
    return es.delete_by_query(index=index, doc_type=doc_type, body="{}")


def get_by_id(index, doc_type, id):
    return es.get(index=index, doc_type=doc_type, id=id)


def delete_index(index):
    return es.delete(index=index)
