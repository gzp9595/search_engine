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
    count = 0
    cnt = 0
    for x in os.listdir(config.DATA_DIR):
        cnt += 1
        print cnt
        f = open(config.DATA_DIR + x, 'r')
        content = ''
        for line in f:
            content = json.loads(line)
            break
        try:
            # content["splitTitle"] = ' '.join(list(jieba.cut_for_search(content["Title"])))
            # content["splitContent"] = ' '.join(list(jieba.cut_for_search(content["content"])))
            elastic.insert_doc('law', 'small_data', json.dumps(content))
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

        if util.check_date(body["from_year"],body["from_month"],body["from_day"]):
            gg
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
