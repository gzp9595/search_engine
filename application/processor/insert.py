import formatter
from ..elastic import elastic

import json
import os

cnt = 0
count = 0


def insert_file_new(index, doc_type, file_name):
    global cnt
    global count
    f = open(file_name, 'r')
    content = ''
    print file_name
    for line in f:
        try:
            content = json.loads(line)
            data = formatter.new_parse(content)
            if data["content"] == "":
                continue
            data["doc_name"] = data["docId"]

            elastic.update_by_id(index, doc_type, data["doc_name"], data)

            cnt += 1

        except Exception as e:
            print e
            count += 1
            f = open('fail_list.txt', 'a')
            print >> f, file_name, e
            f.close()

            # print cnt

            # gg
    print cnt


def insert_file(index, doc_type, file_name):
    global cnt
    global count
    f = open(file_name, 'r')
    content = ''
    text_field = ["caseName", "time", "caseType", "caseNumber", "spcx", "court", "judge", "lawyer", "keyword", "cause",
                  "docType", "punishment", "result", "docId", "document"]
    print file_name
    for line in f:
        try:
            arr = line.split('\t')
            if len(arr) == 1:
                continue
            if len(arr) != len(text_field):
                gg
            content = {}
            for a in range(0, len(text_field)):
                content[text_field[a]] = arr[a]
            if len(content["document"]) == 3:
                content["document"] = "{\"content\":\"\"}"
                of = open('no_content.txt', 'a')
                print >> of, content["docId"]
                of.close()
            else:
                content["document"] = content["document"][0:(len(content["document"]) - 2)]
            data = formatter.new_parse(content)
            if data["content"] == "":
                continue
            data["doc_name"] = data["docId"]

            elastic.update_by_id(index, doc_type, data["doc_name"], data)

            cnt += 1

            if cnt % 100 == 0:
                print cnt

        except Exception as e:
            # print e
            count += 1
            of = open('fail_list.txt', 'a')
            print >> of, file_name, e, line
            of.close()

            # gg
    print cnt


def dfs_insert(index, doc_type, path):
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            dfs_insert(index, doc_type, path + x + "/")
        else:
            if x.endswith(".json"):
                insert_file(index, doc_type, path + x)
