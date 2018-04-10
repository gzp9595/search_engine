#  -*- coding:utf-8 -*-
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
from application.util import print_time, form_date, merge_dict
from application.expander import expand
from . import app
from matcher import get_best
from application.cutter import cut
from application.counter import get_info
from application.databaser import database

import urllib2
import urllib


@app.route('/search', methods=["POST", "GET"])
def search():
    print "Mission Start"
    result = []
    request.args = merge_dict([request.args, request.form])
    for x in request.args:
        print x, request.args[x]

    if "doc_type" in request.args and "index" in request.args:
        log_id = -1
        if "username" in request.args:
            gg_id = 0
            if "from" in request.args:
                gg_id = int(request.args["from"])
            if gg_id == 0:
                res_check = database.check_searchable(request.args)
                if res_check["code"] != 0:
                    response = make_response(json.dumps(res_check))
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'GET'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                    return response
                res_add = database.add_search_log(request.args)
                if res_add["code"] != 0:
                    response = make_response(json.dumps(res_add))
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'GET'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                    return response
                log_id = res_add["msg"]
        else:
            return json.dumps(util.create_error(666, u"用户未登录"), cls=util.CJsonEncoder)

        body = []

        args = request.args
        for x in args:
            print x, args[x]

        search_type = "content"
        expanded = ""
        # body.append({"match": {search_type: expand(args["search_content"])}})

        ratio1 = app.config["EXPAND_RATIO"][0]
        ratio2 = app.config["EXPAND_RATIO"][1]

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
            # expanded = expand(args["search_content"])
            body.append({"match": {search_type: {"query": args["search_content"]}}})

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
            body.append({"range": {"CPRQ": {
                "gte": form_date(args["caipan_from_year"], args["caipan_from_month"], args["caipan_from_day"])}}})

        if "caipan_to_year" in args and "caipan_to_month" in args and "caipan_to_day" in args and util.check_date(
                args["caipan_to_year"], args["caipan_to_month"], args["caipan_to_day"]):
            body.append({"range": {
                "CPRQ": {"lte": form_date(args["caipan_to_year"], args["caipan_to_month"], args["caipan_to_day"])}}})

        if "judgement" in args and args["judgement"] != "":
            body.append({"match": {"WBWB": args["judgement"]}})

        if "fabu_from_year" in args and "fabu_from_month" in args and "fabu_from_day" in args and util.check_date(
                args["fabu_from_year"], args["fabu_from_month"], args["fabu_from_day"]):
            body.append({"range": {
                "PubDate": {"gte": form_date(args["fabu_from_year"], args["fabu_from_month"], args["fabu_from_day"])}}})

        if "fabu_to_year" in args and "fabu_to_month" in args and "fabu_to_day" in args and util.check_date(
                args["fabu_to_year"], args["fabu_to_month"], args["fabu_to_day"]):
            body.append({"range": {
                "PubDate": {"lte": form_date(args["fabu_to_year"], args["fabu_to_month"], args["fabu_to_day"])}}})

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
        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"], query_string, 250,
                                          from_id)

        if "where_to_search" in args and args["search_content"] != "":
            print "Begin second round search"
            print_time()
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
            body[0] = {"match": {search_type: {"query": expanded}}}
            query_string = json.dumps({"query": {"bool": {"must": body}}})
            print query_string
            new_result = elastic.search_doc(request.args["index"], request.args["doc_type"], query_string, 250,
                                            from_id)
            id_list = set()
            for x in query_result["hits"]:
                id_list.add(x["_id"])
            for x in new_result["hits"]:
                if x["_id"] in id_list:
                    continue
                id_list.add(x["_id"])
                x["_score"] *= float(ratio2) / ratio1
                query_result["hits"].append(x)
        print "Results return:"
        print len(query_result["hits"])
        inf = {}
        if from_id == 0:
            inf = get_info(query_result["hits"])

        print "Begin to reranking"
        print_time()
        query_result["hits"] = ranking.reranking(query_result["hits"], args)
        print "Reranking Done"
        print_time()

        temp = []
        for x in query_result["hits"][from_id:min(len(query_result["hits"]), from_id + size)]:
            temp.append(x["_source"])

        print "Cut begin"
        print_time()
        need_to_cut = [args["search_content"] + "," + expanded]
        print expanded
        for x in temp:
            need_to_cut.append(x["content"])
        filter_list = [65292, 12290, 65311, 65281, 65306, 65307, 8216, 8217, 8220, 8221, 12304, 12305,
                       12289, 12298, 12299, 126, 183, 64, 124, 35, 65509, 37, 8230, 38, 42, 65288,
                       65289, 8212, 45, 43, 61, 44, 46, 60, 62, 63, 47, 33, 59, 58, 39, 34, 123, 125,
                       91, 93, 92, 124, 35, 36, 37, 94, 38, 42, 40, 41, 95, 45, 43, 61, 9700, 9734, 9733]
        cutted = cut(need_to_cut)
        for x in filter_list:
            for y in range(0, len(cutted[0])):
                cutted[0][y] = cutted[0][y].replace(unichr(x), '')
        fs = []
        for a in range(0, len(cutted[0])):
            # print cutted[0][a], len(cutted[0][a].decode("utf8"))
            if len(cutted[0][a].decode("utf8")) > 1:
                fs.append(cutted[0][a])
        cutted[0] = fs
        # print cutted[0]
        # for x in cutted[0]:
        #    print x,len(x)
        for a in range(0, len(cutted)):
            for b in range(0, len(cutted[a])):
                cutted[a][b] = cutted[a][b].lower()

        print "Tfidf begin"
        print_time()
        for a in range(0, len(temp)):
            res = {"id": temp[a]["doc_name"], "title": temp[a]["Title"],
                   "shortcut": get_best(cutted[0], cutted[a + 1])}
            result.append(res)
        print "All over again"
        print_time()
        result = {"code": 0, "document": result, "information": inf}
        if log_id != -1:
            result["log_id"] = log_id

    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/search_temp', methods=["POST", "GET"])
def search_temp():
    print "Mission Start"
    result = []
    request.args = merge_dict([request.args, request.form])
    for x in request.args:
        print x, request.args[x]

    if True:
        body = []

        args = request.args
        for x in args:
            print x, args[x]

        if args["search_content"] != "":
            match_type = {
                "0": "content",
                "1": "WBSB",
                "2": "AJJBQK",
                "3": "CPYZ",
                "4": "PJJG",
                "5": "WBWB"
            }
            search_type = match_type["0"]
            # expanded = expand(args["search_content"])
            body.append({"match": {search_type: {"query": args["search_content"]}}})
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
        print real_size
        query_result = elastic.search_doc("law","big_data", query_string, real_size,
                                          from_id)

        print "Begin to reranking"
        print_time()
        args["type_of_model"]=-2
        query_result["hits"] = ranking.reranking(query_result["hits"], args)
        print "Reranking Done"
        print_time()

        temp = []
        for x in query_result["hits"][from_id:min(len(query_result["hits"]), from_id + size)]:
            temp.append(x["_source"])

        print "Tfidf begin"
        print_time()

        result = []
        for a in range(0, len(temp)):
            res = temp[a]["doc_name"]
            result.append(res)

    response = make_response(json.dumps(result, ensure_ascii=False))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


@app.route('/search_new', methods=["POST", "GET"])
def search_new():
    print "Mission Start"
    result = []
    request.args = merge_dict([request.args, request.form])

    if "doc_type" in request.args and "index" in request.args:
        body = []

        args = request.args

        search_type = "content"
        # body.append({"match": {search_type: expand(args["search_content"])}})

        if True:
            match_type = {
                "0": "content",
                "1": "WBSB",
                "2": "AJJBQK",
                "3": "CPYZ",
                "4": "PJJG",
                "5": "WBWB"
            }
            search_type = match_type[search_type]
            # expanded = expand(args["search_content"])
            body.append({"match": {search_type: {"query": args["search_content"]}}})

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

        inf = get_info(query_result["hits"])

        print "Begin to reranking"
        print_time()
        query_result["hits"] = ranking.reranking(query_result["hits"], args)
        print "Reranking Done"
        print_time()

        temp = []
        for x in query_result["hits"][from_id:min(len(query_result["hits"]), from_id + size)]:
            temp.append(x["_source"])

        print "All over again"
        print_time()

        return make_response(json.dumps({"inf":inf,"data":temp}))

    return "gg"


@app.route('/doc')
def get_doc_byid():
    request.args = merge_dict([request.args, request.form])
    if "id" in request.args:
        if "username" in request.args:
            res_check = database.check_viewable(request.args)
            if res_check["code"] != 0:
                response = make_response(json.dumps(res_check))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'GET'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                return response
            res_add = database.add_view_log(request.args)
            if res_add["code"] != 0:
                response = make_response(json.dumps(res_add))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'GET'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                return response
        else:
            return util.create_error(666, u"用户未登录")
        query_result = elastic.get_by_id("law_meta", "meta", request.args["id"])
        data = {"_source": json.loads(query_result["_source"]["content"])}
        data["_source"]["FLYJ"] = formatter.sort_reason(data["_source"]["FLYJ"])
        data["code"] = 0
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


@app.route('/doc_temp')
def get_doc_byid_temp():
    request.args = merge_dict([request.args, request.form])
    if "id" in request.args:
        query_result = elastic.get_by_id("law_meta", "meta", request.args["id"])
        data = {"_source": json.loads(query_result["_source"]["content"])}
        data["_source"]["FLYJ"] = formatter.sort_reason(data["_source"]["FLYJ"])
        data["code"] = 0
        data = json.dumps(data)
        response = make_response(data)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response
        return json.dumps(query_result["_source"])

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


@app.route('/static/<path:filetype>/<path:filename>')
def serve_static(filetype, filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, app.config["WORK_DIR"], 'application', 'static', filetype),
                               filename)


@app.route('/gen_code', methods=["POST", "GET"])
def gen_code():
    return "gg"
    f = open ("code.csv","w")
    import uuid
    for a in range(0,4):
        for b in range(0,100):
            code = str(uuid.uuid4())
            print >> f,str(a)+","+code
            database.gen_code({"type":a,"code":code})
            #request.args = merge_dict([request.args, request.form])
    #code = database.gen_code(request.args)
    return "Success"


@app.route('/register', methods=["POST", "GET"])
def register():
    request.args = merge_dict([request.args, request.form])

    if not ("code" in request.args):
        return json.dumps(util.create_error(100, u"验证码不存在"))
    data = database.check_code(request.args["code"])
    if data == -1:
        return json.dumps(util.create_error(101, u"验证码不正确"))

    request.args["user_code"] = request.args["code"]
    result = database.add_user(request.args, data)
    if result["code"] == 0:
        database.move_code(request.args["code"])
    return json.dumps(result)


@app.route('/login', methods=["POST", "GET"])
def login():
    request.args = merge_dict([request.args, request.form])

    return json.dumps(database.check_user(request.args))


@app.route('/get_user_info', methods=["POST", "GET"])
def get_user_info():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.get_user_info(request.args), cls=util.CJsonEncoder)


@app.route('/add_favor_list', methods=["POST", "GET"])
def add_favor_list():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.add_favor_list(request.args), cls=util.CJsonEncoder)


@app.route('/get_favor_list', methods=["POST", "GET"])
def get_favor_list():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.get_favor_list(request.args), cls=util.CJsonEncoder)


@app.route('/get_favor_list_item', methods=["POST", "GET"])
def get_favor_list_item():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.get_favor_list_item(request.args), cls=util.CJsonEncoder)


@app.route('/add_favor_item', methods=["POST", "GET"])
def add_favor_item():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.add_favor_item(request.args), cls=util.CJsonEncoder)


@app.route('/get_history', methods=["POST", "GET"])
def get_history():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.get_history(request.args), cls=util.CJsonEncoder)


@app.route('/remove_favor_item', methods=["POST", "GET"])
def remove_favor_item():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.remove_favor_item(request.args), cls=util.CJsonEncoder)

@app.route('/auth_user',methods = ["POST","GET"])
def auth_user():
    request.args = merge_dict([request.args, request.form])
    return json.dumps(database.auth_user(request.args), cls=util.CJsonEncoder)
