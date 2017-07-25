from flask import Flask, request, render_template
import config
import elastic
import os
import json
import jieba
import util
import platform
import formatter
import ranking

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    return 'Hello World!'


cnt = 0
count = 0


def insert_file(index, doc_type, file_name):
    global cnt
    global count
    cnt += 1
    print cnt
    f = open(file_name, 'r')
    content = ''
    for line in f:
        content = json.loads(line)
        break
    try:
        # print formatter.parse(content)
        data = formatter.parse(content)
        if data["content"] == "":
            return
        data["doc_name"] = file_name[len(file_name) - 49:len(file_name) - 13]
        elastic.insert_doc(index, doc_type, data)
        # print x + " Succeed"
    except Exception as e:
        print e
        count += 1
        f = open('fail_list.txt', 'a')
        print >> f, file_name, e
        f.close()


def dfs_insert(index, doc_type, path):
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            dfs_insert(index, doc_type, path + x + "/")
        else:
            if x.endswith(".json"):
                insert_file(index, doc_type, path + x)


@app.route('/insert_all')
def insert_all():
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


@app.route('/search')
def search():
    content = ""
    result = []
    if "content" in request.args and "type" in request.args and "doc_type" in request.args and "index" in request.args:
        body = {}

        body["must"] = {}
        body["filter"] = {}
        if True:
            body["must"]["match"] = {}

        body["must"]["match"][request.args["type"]] = "\"" + request.args["content"] + "\""

        if "from_year" in request.args and "from_month" in request.args and "from_day" in request.args and util.check_date(
                request.args["from_year"], request.args["from_month"], request.args["from_day"]):
            if not ("range" in body["filter"]):
                body["filter"]["range"] = {}
            if not ("PubDate" in body["filter"]["range"]):
                body["filter"]["range"]["PubDate"] = {}
            body["filter"]["range"]["PubDate"]["gte"] = request.args["from_year"] + "-" + request.args[
                "from_month"] + "-" + request.args["from_day"]

        if "to_year" in request.args and "to_month" in request.args and "to_day" in request.args and util.check_date(
                request.args["to_year"], request.args["to_month"], request.args["to_day"]):
            if not ("range" in body["filter"]):
                body["filter"]["range"] = {}
            if not ("PubDate" in body["filter"]["range"]):
                body["filter"]["range"]["PubDate"] = {}
            body["filter"]["range"]["PubDate"]["lte"] = request.args["to_year"] + "-" + request.args[
                "to_month"] + "-" + request.args["to_day"]

        print body
        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"],
                                          json.dumps({"query": {"bool": body}, "size": 100}))[
            "hits"]
        # res = [request.args["content"]]
        # print request.args["content"]
        for x in query_result:
            # res.append(x["_source"]["Title"])
            result.append({"title": x["_source"]["Title"], "id": x["_id"]})
            # for y in x["_source"]:
            #    if y != "content":
            #        print y,x["_source"][y]
            # break
        # print res

        if "content" in request.args:
            content = request.args["content"]
    return render_template("search.html", content=content, result=result, args=request.args)


@app.route('/search_new')
def search_new():
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

        print body

        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"],
                                          json.dumps({"query": {"bool": {"must": body}}, "size": 100}))
        query_result["hits"] = ranking.reranking(query_result["hits"],args)


        for x in query_result["hits"]:
            # res.append(x["_source"]["Title"])
            result.append({"title": x["_source"]["Title"], "id": x["_id"]})
	
    args = dict(request.args)
    if not("search_content" in request.args):
        args["search_content"] = ""
    if not("where_to_search" in request.args):
        args["where_to_search"] = ""
    if not("index" in request.args):
        args["index"] = ""
    if not("doc_type" in request.args):
        args["doc_type"] = ""
    return render_template("search_new.html", args=request.args, result=result, query=request.args)


@app.route('/adddata',methods=["POST","GET"])
def add_data():
    print "GG"
    print request.form
    query = json.loads(request.form["query"])
    obj = elastic.get_by_id(query["index"],query["doc_type"],request.form["id"])
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


def click(id, perform):
    print id, perform


if __name__ == '__main__':
    if platform.system() == "Windows":
        app.run(host='127.0.0.1', port=8000)
    else:
        app.run(host='115.28.106.67', port=8000)
