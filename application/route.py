import json
import os
import uuid

from flask import request, render_template, make_response, send_from_directory

import config
import elastic
import util
from application.processor import formatter
from application.reranking import ranking
from application.reranking.classifer import train_new_model
from application.util import print_time
from application.expander import expand
from . import app
from matcher import get_best
from application.cutter import cut
from application.counter import get_info

import urllib2
import urllib

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


@app.route('/search', methods=["POST", "GET"])
def search():
    print "Mission Start"
    result = []
    for x in request.form:
        request.args[x] = request.form[x]

    if "doc_type" in request.args and "index" in request.args:
        body = []

        args = request.args
        for x in args:
            print x,args[x]

        search_type = "content"
        expanded = ""
        # body.append({"match": {search_type: expand(args["search_content"])}})

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
            expanded = expand(args["search_content"])
            body.append({"match": {search_type: expanded}})

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

        size = 25
        from_id = 0
        if "from" in request.args:
            from_id = int(request.args["from"])
            if "to" in request.args:
                size = int(request.args["to"]) - int(request.args["from"]) + 1
        real_size = size + from_id

        print "Begin to search"
        print_time()
        query_string = json.dumps({"query": {"bool": {"must": body}}})
        print query_string
        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"], query_string, real_size,
                                          from_id)
        print "Begin to reranking"
        print_time()
        query_result["hits"] = ranking.reranking(query_result["hits"], args)
        print "Reranking Done"
        print_time()

        temp = []
        for x in query_result["hits"][from_id:]:
            temp.append(x["_source"])

        print "Cut begin"
        print_time()
        need_to_cut = [expanded]
        print expanded
        for x in temp:
            need_to_cut.append(x["content"])
        cutted = cut(need_to_cut)
        print cutted[0]

        print "Tfidf begin"
        print_time()
        for a in range(0, len(temp)):
            res = {"id": temp[a]["doc_name"], "title": temp[a]["Title"],
                   "shortcut": get_best(cutted[0], cutted[a + 1])}
            result.append(res)
        print "All over again"
        print_time()

    args = dict(request.args)
    if not ("search_content" in request.args):
        args["search_content"] = ""
    if not ("where_to_search" in request.args):
        args["where_to_search"] = ""
    if not ("index" in request.args):
        args["index"] = ""
    if not ("doc_type" in request.args):
        args["doc_type"] = ""
    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/search_new', methods=["POST", "GET"])
def search_new():
    print "Mission Start"

    result = []
    print request.args
    if len(request.args) == 0:
        request.args = {}
    for x in request.form:
        request.args[x] = request.form[x]

    if "doc_type" in request.args and "index" in request.args:
        body = []

        args = request.args

        search_type = "content"
        body.append({"match": {search_type: expand(args["search_content"])}})

        size = 25
        from_id = 0
        if "from" in request.args:
            from_id = int(request.args["from"])
            if "to" in request.args:
                size = int(request.args["to"]) - int(request.args["from"]) + 1

        size = 25
        from_id = 0
        if "from" in request.args:
            from_id = int(request.args["from"])
            if "to" in request.args:
                size = int(request.args["to"]) - int(request.args["from"]) + 1
        real_size = size + from_id

        print "Begin to search"
        print_time()
        query_string = json.dumps({"query": {"bool": {"must": body}}})
        print query_string
        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"], query_string, real_size,
                                          from_id)
        print "Begin to reranking"
        print_time()
        query_result["hits"] = ranking.reranking(query_result["hits"], args)
        print "Reranking Done"
        print_time()

        temp = []
        tempg = []
        for x in query_result["hits"][from_id:]:
            temp.append(x["_source"])
            tempg.append(json.loads(elastic.get_by_id("law_meta", "meta", x["_id"])["_source"]["content"]))

        meta = get_info(tempg)
        print meta

        print "Cut begin"
        print_time()
        need_to_cut = [args["search_content"]]
        for x in temp:
            need_to_cut.append(x["content"])
        cutted = cut(need_to_cut)

        print "Tfidf begin"
        print_time()
        for a in range(0, len(temp)):
            res = {"id": temp[a]["doc_name"], "title": temp[a]["Title"],
                   "shortcut": get_best(cutted[0], cutted[a + 1])}
            result.append(res)
        print "All over again"
        print_time()

    args = dict(request.args)
    if not ("search_content" in request.args):
        args["search_content"] = ""
    if not ("where_to_search" in request.args):
        args["where_to_search"] = ""
    if not ("index" in request.args):
        args["index"] = ""
    if not ("doc_type" in request.args):
        args["doc_type"] = ""
    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return render_template("search_new.html", args=request.args, result=result, query=request.args)


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
    if "id" in request.args:
        query_result = elastic.get_by_id("law_meta", "meta", request.args["id"])
        data = {"_source": json.loads(query_result["_source"]["content"])}
        data["_source"]["FLYJ"].sort()
        data = json.dumps(data)
        response = make_response(data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response
        return json.dumps(query_result["_source"])
        # print query_result["_source"]["content"]
        return render_template("news.html", content=unicode(query_result["_source"]["content"]),
                               Title=query_result["_source"]["Title"],
                               PubDate="0000-00-00",  # query_result["_source"]["PubDate"],
                               origin=query_result["_source"]["doc_name"]) \
            .replace('\\b', '<br/>')

    return "Error"


@app.route('/doc_new')
def get_doc_byid_new():
    if "id" in request.args:
        query_result = {
            "_source": json.loads(elastic.get_by_id("law_meta", "meta", request.args["id"])["_source"]["content"])}
        response = make_response(render_template("news.html", content=unicode(query_result["_source"]["content"]),
                                                 Title=query_result["_source"]["Title"],
                                                 PubDate="0000-00-00",  # query_result["_source"]["PubDate"],
                                                 origin=query_result["_source"]["doc_name"]) \
                                 .replace('\\b', '<br/>'))
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

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


@app.route("/")
def main():
    return render_template("main.html")


@app.route('/static/<path:filetype>/<path:filename>')
def serve_static(filetype, filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, app.config["WORK_DIR"], 'application', 'static', filetype),
                               filename)


@app.route('/document')
def get_document():
    return render_template("document.html", id=request.args["id"])


@app.route('/search_new2')
def search_new2():
    url = "http://bc2.citr.me:8000/search"
    first = True
    for x in request.args:
        if first:
            url += "?"
        else:
            url += "&"
        url += x + "=" + request.args[x]
        first = False
    result = json.loads(urllib2.urlopen(url=url.encode('utf8'), timeout=1000000).read())

    return render_template("search_new2.html", result=result, s=len(result), args=request.args)
