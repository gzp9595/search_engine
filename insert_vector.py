import os
import config

index = "law_vector"
doc_type_list = ["lda", "tfidf", "word"]
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

    for doc_type in doc_type_list:
        for x in os.listdir(dir_path + doc_type):
            file_name = dir_path + doc_type + "/"+ x
            f = open(file_name, "r")
            for line in f:
                total += 1
                if basic < total:
                    continue
                if total % 100 == 0:
                    print total, cnt, count
                try:
                    arr = line.split('\t')
                    update_by_id(index, doc_type, arr[0], {"vector": arr[1]})
                    cnt += 1
                except Exception as e:
                    count += 1
                    of = open('fail_vector_list.txt', 'a')
                    print >> of, file_name, e, line.split('\t')[0]
                    of.close()
