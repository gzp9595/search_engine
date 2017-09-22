import logging
import os

insert_path = "/mnt/zhx/"
index = "law_doc"
doc_type = "content_seg"

server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

cnt = 0
count = 0
total = 0

cibiao = set()
f = open("cibiao.txt", "r")
for line in f:
    cibiao.add(line.replace("\n", ""))

from application import app, initialize

app.config.from_pyfile(config_file)
if os.path.exists(local_config_file):
    app.config.from_pyfile(local_config_file)

from application.elastic import update_by_id


def insert_file(index, doc_type, file_name):
    global cnt
    global count
    f = open(file_name, 'r')
    content = ''
    print file_name
    for line in f:
        try:
            line = line.decode('utf8')
            arr = line.split('\t')
            if len(arr) == 1:
                continue
            data = {}
            data["docId"] = arr[0]
            data["content"] = ""
            arr = arr[1].split(" ")
            first = True
            for a in range(0, len(arr)):
                if arr[a] in cibiao:
                    if not (first):
                        data["content"] += ""
                    first = False
                    data["content"] += arr[a]

            update_by_id(index, doc_type, data["docId"], data)

            cnt += 1

            if cnt % 100 == 0:
                print cnt, count

        except Exception as e:
            # print e
            count += 1
            of = open('fail_list.txt', 'a')
            print >> of, file_name, e, line.encode("utf8")
            of.close()

    print cnt


def dfs_insert(index, doc_type, path):
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            dfs_insert(index, doc_type, path + x + "/")
        else:
            insert_file(index, doc_type, path + x)


dfs_insert(index, doc_type, insert_path)
