from flask import Flask, request, render_template
import config
import elastic
import os
import json
import jieba
import util

app = Flask(__name__)
app.config.from_object(config)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/insert_all')
def insert_all():
    if not ("index" in request.args) or not ("doc_type" in request.args):
        return "No specific data"
    count = 0
    cnt = 0
    index = request.args["index"]
    doc_type = request.args["doc_type"]
    for x in os.listdir(config.DATA_DIR + index + "/" + doc_type + "/"):
        cnt += 1
        print cnt
        f = open(config.DATA_DIR + index + "/" + doc_type + "/" + x, 'r')
        content = ''
        for line in f:
            content = json.loads(line)
            break
        try:
            # content["splitTitle"] = ' '.join(list(jieba.cut_for_search(content["Title"])))
            # content["splitContent"] = ' '.join(list(jieba.cut_for_search(content["content"])))
            elastic.insert_doc(index, doc_type, json.dumps(content))
            # print x + " Succeed"
        except Exception as e:
            count += 1
            f = open('fail_list.txt', 'a')
            print >> f, x
            f.close()
            # print x + " Failed"
    return "Failed:" + str(count)


@app.route('/get_count')
def get_count():
    return str(elastic.get_count(request.args["index"], request.args["doc_type"])["count"])


@app.route('/remove_all')
def remove_all():
    return "Succeed delete " + str(elastic.remove_all(request.args["index"], request.args["doc_type"])["deleted"])


@app.route('/search')
def search():
    content = ""
    result = []
    if "content" in request.args and "type" in request.args and "doc_type" in request.args and "index" in request.args:
        body = {}
        if "size" in request.args:
            body["size"] = int(request.args["size"])
        else:
            body["size"] = 100

        body["query"] = {}
        if True:
            body["query"]["match"] = {}

        if request.args["type"] == "title":
            body["query"]["match"]["Title"] = request.args["content"]
        else:
            body["query"]["match"]["content"] = request.args["content"]

        if "from_year" in request.args and "from_month" in request.args and "from_day" in request.args and util.check_date(
                request.args["from_year"], request.args["from_month"], request.args["from_day"]):
            if not ("range" in body["query"]):
                body["query"]["range"] = {}
            if not ("PubDate" in body["query"]["range"]):
                body["query"]["range"]["PubDate"] = {}
            body["query"]["range"]["PubDate"]["gte"] = request.args["from_year"] + "-" + request.args[
                "from_month"] + "-" + request.args["from_day"]

        if "to_year" in request.args and "to_month" in request.args and "to_day" in request.args and util.check_date(
                request.args["to_year"], request.args["to_month"], request.args["to_day"]):
            if not ("range" in body["query"]):
                body["query"]["range"] = {}
            if not ("PubDate" in body["query"]["range"]):
                body["query"]["range"]["PubDate"] = {}
            body["query"]["range"]["PubDate"]["lte"] = request.args["to_year"] + "-" + request.args[
                "to_month"] + "-" + request.args["to_day"]

        print body
        query_result = elastic.search_doc(request.args["index"], request.args["doc_type"], json.dumps(body))["hits"]
        # res = [request.args["content"]]
        # print request.args["content"]
        for x in query_result:
            # res.append(x["_source"]["Title"])
            result.append({"title": x["_source"]["Title"], "id": x["_id"]})
            # print res

    if "content" in request.args:
        content = request.args["content"]
    return render_template("search.html", content=content, result=result, args=request.args)


@app.route('/doc')
def get_doc_byid():
    if "doc_type" in request.args and "index" in request.args and "id" in request.args:
        query_result = elastic.get_by_id(request.args["index"], request.args["doc_type"], request.args["id"])
        print query_result["_source"]["content"]
        return render_template("news.html", content=query_result["_source"]["content"],
                               Title=query_result["_source"]["Title"], PubDate=query_result["_source"]["PubDate"])
    return "Error"


if __name__ == '__main__':
    app.run()
