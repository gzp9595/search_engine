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
    for line in f:
        #try:
            content = json.loads(line)
            data = formatter.new_parse(content)
            if data["content"] == "":
                continue
            data["doc_name"] = file_name[len(file_name) - 49:len(file_name) - 13]

            elastic.update_by_id(index, doc_type, data["doc_name"], data)
            
            cnt += 1
            gg

            # print x + " Succeed"
        #except Exception as e:
        #    print e
        #    count += 1
        #    f = open('fail_list.txt', 'a')
        #    print >> f, file_name, e
        #    f.close()

        #gg


def dfs_insert(index, doc_type, path):
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            dfs_insert(index, doc_type, path + x + "/")
        else:
            if x.endswith(".json"):
                insert_file_new(index, doc_type, path + x)
