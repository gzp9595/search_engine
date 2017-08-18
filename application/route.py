import json
import os
import uuid

from flask import request, render_template

import config
import elastic
import util
from application.processor import formatter
from application.reranking import ranking
from application.reranking.classifer import train_new_model
from . import app


@app.route('/')
def hello_world():
    return 'Hello World!'


cnt = 0
count = 0


@app.route('/insert_all')
def insert_all():
    return "Disabled"
    if not ("index" in request.args) or not ("doc_type" in request.args):
        return "No specific data"
    global count
    global cnt
    count = 0
    cnt = 0
    index = request.args["index"]
    doc_type = request.args["doc_type"]
    dfs_insert(index, doc_type, config.DATA_DIR + index + "/" + doc_type + "/")
    return "Failed:" + str(count)


@app.route('/get_count')
def get_count():
    return str(elastic.get_count(request.args["index"], request.args["doc_type"])["count"])


@app.route('/remove_all')
def remove_all():
    return "I won't allow you to do this"
    return "Succeed delete " + str(elastic.remove_all(request.args["index"], request.args["doc_type"])["deleted"])


@app.route('/search_new')
@app.route('/search')
def search():
    result = []

    if "doc_type" in request.args and "index" in request.args:
        body = []

        args = request.args

        search_type = "content"
        if "where_to_search" in args and args["search_content"] != "":
            match_type = {
                "0": "content",
                "1": "WBSB",
                "2": "AJJBQK",
                "3": "CPYZ",
                "4": "PJJG",
                "5": "WBWB"
            }
            search_type = match_type[args["where_to_search"]]

            body.append({"match": {search_type: args["search_content"]}})

        if "name_of_case" in args and args["name_of_case"] != "":
            body.append({"match": {"Title": args["name_of_case"]}})

        if "case_number" in args and args["case_number"] != "":
            body.append({"match": {"AJAH": args["case_number"]}})

        if "name_of_court" in args and args["name_of_court"] != "":
            body.append({"match": {"FYMC": args["name_of_court"]}})

        if "level_of_court" in args and args["level_of_court"] != "0":
            try:
                value = int(args["level_of_court"])
                body.append({"term": {"FYCJ": value}})
            except ValueError:
                pass

        if "type_of_case" in args and args["type_of_case"] != "0":
            try:
                value = int(args["type_of_case"])
                body.append({"term": {"AJLX": value}})
            except ValueError:
                pass

        if "type_of_doc" in args and args["type_of_doc"] != "0":
            try:
                value = int(args["type_of_doc"])
                body.append({"term": {"WSLX": value}})
            except ValueError:
                pass

        if "caipan_from_year" in args and "caipan_from_month" in args and "caipan_from_day" in args and util.check_date(
                args["caipan_from_year"], args["caipan_from_month"], args["caipan_from_day"]):
            body.append({"range": {"CPRQ": {"gte": args["caipan_from_year"] + "-" + args[
                "caipan_from_month"] + "-" + args["caipan_from_day"]}}})

        if "caipan_to_year" in args and "caipan_to_month" in args and "caipan_to_day" in args and util.check_date(
                args["caipan_to_year"], args["caipan_to_month"], args["caipan_to_day"]):
            body.append({"range": {"CPRQ": {"lte": args["caipan_to_year"] + "-" + args[
                "caipan_to_month"] + "-" + args["caipan_to_day"]}}})

        if "judgement" in args and args["judgement"] != "":
            body.append({"match": {"WBWB": args["judgement"]}})

        if "fabu_from_year" in args and "fabu_from_month" in args and "fabu_from_day" in args and util.check_date(
                args["fabu_from_year"], args["fabu_from_month"], args["fabu_from_day"]):
            body.append({"range": {"PubDate": {"gte": args["fabu_from_year"] + "-" + args[
                "fabu_from_month"] + "-" + args["fabu_from_day"]}}})

        if "fabu_to_year" in args and "fabu_to_month" in args and "fabu_to_day" in args and util.check_date(
                args["fabu_to_year"], args["fabu_to_month"], args["fabu_to_day"]):
            body.append({"range": {"PubDate": {"lte": args["fabu_to_year"] + "-" + args[
                "fabu_to_month"] + "-" + args["fabu_to_day"]}}})

        if "name_of_law" in args and args["name_of_law"] != "":
            new_body = [{"match": {"FLYJ.law_name": args["name_of_law"]}}]
            if "num_of_tiao" in args and args["num_of_tiao"] != "":
                new_body.append({"match": {"FLYJ.tiao_num": args["num_of_tiao"]}})
            if "num_of_kuan" in args and args["num_of_kuan"] != "":
                new_body.append({"match": {"FLYJ.kuan_num": args["num_of_kuan"]}})
            body.append({"nested": {"path": "FLYJ", "query": {"bool": {"must": new_body}}}})

        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"],
                                          json.dumps({"query": {"bool": {"must": body}}, "size": 100}))
        query_result["hits"] = ranking.reranking(query_result["hits"], args)

        for x in query_result["hits"]:
            res = {"id": x["_id"], "score": x["_source"]["score"]}
            for y in x["_source"]:
                res[y] = x["_source"][y]
            result.append(res)

    args = dict(request.args)
    if not ("search_content" in request.args):
        args["search_content"] = ""
    if not ("where_to_search" in request.args):
        args["where_to_search"] = ""
    if not ("index" in request.args):
        args["index"] = ""
    if not ("doc_type" in request.args):
        args["doc_type"] = ""
    return render_template("search.html", args=request.args, result=result, query=request.args)


@app.route('/adddata', methods=["POST", "GET"])
def add_data():
    print "GG"
    print request.form
    query = json.loads(request.form["query"])
    obj = elastic.get_by_id(query["index"], query["doc_type"], request.form["id"])
    score = int(request.form["score"])
    print request.form["id"], score
    ranking.add_data(obj["_source"], query, score)
    return ""


@app.route('/doc')
def get_doc_byid():
    if "doc_type" in request.args and "index" in request.args and "id" in request.args:
        query_result = elastic.get_by_id(request.args["index"], request.args["doc_type"], request.args["id"])
        # print query_result["_source"]["content"]
        return render_template("news.html", content=unicode(query_result["_source"]["content"]),
                               Title=query_result["_source"]["Title"],
                               PubDate=query_result["_source"]["PubDate"],
                               origin=query_result["_source"]["doc_name"]) \
            .replace('\b', '<br/>')

    return "Error"


@app.route("/addclickdata", methods=["POST", "GET"])
def addclickdata():
    print request.form
    file_name = str(uuid.uuid4())
    f = open(config.CLICK_DIR + file_name + ".json", "w")
    print >> f, json.dumps(request.form)
    f.close()


@app.route("/train_model")
def train_model():
    train_new_model()
