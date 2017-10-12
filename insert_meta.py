import os
import config
import json

index = "law_meta"
doc_type = "meta"
dir_path = "/mnt/vec/"

server_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(server_dir, 'config.py')
local_config_file = os.path.join(server_dir, 'local_config.py')

if __name__ == '__main__':
    from application import app, initialize

    app.config.from_pyfile(config_file)
    if os.path.exists(local_config_file):
        app.config.from_pyfile(local_config_file)

    total = 0
    cnt = 0
    count = 0
    basic = 0

    from application.elastic import update_by_id
    from application.processor import formatter

    text_field = ["caseName", "time", "caseType", "caseNumber", "spcx", "court", "judge", "lawyer",
                  "keyword", "cause",
                  "docType", "punishment", "result", "docId", "document"]

    for x in os.listdir(dir_path):
        file_name = dir_path + x
        f = open(file_name, "r")
        for line in f:
            total += 1
            if basic > total:
                continue
            if total % 100 == 0:
                print total, cnt, count

            try:
                line = line.decode('utf8')
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

                update_by_id(index, doc_type, data["doc_name"], {"content": json.dumps(data)})

                cnt += 1

            except Exception as e:
                # print e
                count += 1
                of = open('fail_list.txt', 'a')
                print >> of, file_name, e, line.encode("utf8")
                of.close()
