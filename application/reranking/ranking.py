from application import app
from application.reranking import classifer, feature
from application.util import print_time

import json
import os
import uuid
import warnings

import numpy as np

from application.doc2vec.Doc2vec import *

length = 11 * 2 + 1 + 3 + 2

if not (os.path.exists(app.config["TRAINING_DIR"])):
    os.makedirs(app.config["TRAINING_DIR"])

model = classifer.model()
try:
    model.load_model()
except Exception:
    pass

doc2vec_model = Doc2vec(save_path=app.config["ANOTHER_DOC2VEC"])


def write_model():
    model.save_model()


def get_feature(obj, query):
    obj = feature.gen_ranking_feature(obj, query)

    features = []

    features.append(query["where_to_search"])

    keylist = ["WBWB", "DSRXX", "PubDate", "Title", "CPYZ", "AJJBQK", "PJJG", "content", "SSJL", "WBSB", "AJJBQK"]
    for word in keylist:
        features.append(obj["feature"]["statistics"][word + "_length"])
        features.append(obj["feature"]["statistics"][word + "_num_of_words"])

    features.append(obj["feature"]["statistics"]["judge_timestamp"])

    features.append(obj["feature"]["classification"]["FYCJ"])
    features.append(obj["feature"]["classification"]["AJLX"])
    features.append(obj["feature"]["classification"]["WSLX"])

    if len(obj["feature"]["matching_result"]["matched_time"]) == 0:
        obj["feature"]["matching_result"]["matched_time"].append(0)
    if len(obj["feature"]["matching_result"]["matched_or_not"]) == 0:
        obj["feature"]["matching_result"]["matched_or_not"].append(0)
    features.append(np.average(obj["feature"]["matching_result"]["matched_time"]))
    features.append(np.average(obj["feature"]["matching_result"]["matched_or_not"]))

    return features


def add_data(obj, query, score):
    prin( score)
    file_name = str(uuid.uuid4())
    f = open(app.config["TRAINING_DIR"] + file_name + ".json", "w")
    print(json.dumps({"obj": obj, "query": query, "score": score}),file=f)
    f.close()


def try_get(obj, mode):
    #print "Try get begin"
    #print_time()
    from application.elastic import get_by_id
    import numpy as np
    have_vector = {"TFIDF": "tfidf", "WORD embedding": "word"}
    arr = ["LDA", "TFIDF", "WORD embedding", "LSTM", "CNN"]
    if arr[mode] == "TFIDF" and False:
        data = get_by_id("law_vector", have_vector[arr[mode]], obj["doc_name"])
        if not(data is None):
            data = data["_source"]["vector"]
            data = data[0:len(data) - 1].split(" ")
            res = {}
            for x in data:
                if ":" in x:
                    t = x.split(":")
                    res[int(t[0])] = float(t[1])
            #print "Try get end"
            #print_time()
            return res
    elif arr[mode] == "WORD embedding" and False:
        data = get_by_id("law_vector", have_vector[arr[mode]], obj["doc_name"])
        if not(data is None):
            data = data["_source"]["vector"]
            data = data[0:len(data) - 1].split(" ")
            for a in range(0, len(data)):
                data[a] = float(data[a])
            #print "Try get end"
            #print_time()
            return np.array(data, dtype=np.float32)
    
    #print obj["doc_name"]
    
    return doc2vec_model.get_embedding(text=obj["content"].encode('utf8'), mode=mode)


pre_text = ["","","","",""]
embed = ["","","","",""]

def update_text(s,t):
    if s != pre_text[t]:
        pre_text[t] = s
        embed[t] = doc2vec_model.get_embedding(text=s.encode("utf8"),mode=t)

def get_score(obj, query, sc):
    model_type = int(query["type_of_model"])
    if model_type == -2:
        return sc
    if model_type == -1:
        # print "gg"
        have_vector = {"TFIDF": "tfidf", "WORD embedding": "word"}
        arr = ["LDA", "TFIDF", "WORD embedding", "LSTM", "CNN"]
        match_type = {
            "0": "content",
            "1": "WBSB",
            "2": "AJJBQK",
            "3": "CPYZ",
            "4": "PJJG",
            "5": "WBWB"
        }
        score = 0
        for a in range(0, len(arr)):
            ratio = 0
            if arr[a] in query:
                ratio = float(query[arr[a]])
            else:
                ratio = 0
            # print arr[a],ratio
            if ratio > 0:
                update_text(query["search_content"],a)
                sc = doc2vec_model.get_similarity(
                    embedding1=doc2vec_model.get_embedding(
                        text=try_get(obj, a)),
                    embedding2=embed[a],
                    mode=a
                ) * (1 - float(query["title_ratio"])) + doc2vec_model.get_similarity(
                    embedding1=doc2vec_model.get_embedding(
                        text=obj["Title"].encode("utf8"), mode=a),
                    embedding2=embed[a],
                    mode=a
                ) * float(query["title_ratio"])
                score += sc * ratio
                # with warnings.catch_warnings():
                #    warnings.simplefilter("ignore")
                #    return model.judge(get_feature(obj, query))
        return score
    else:
        update_text(query["search_content"],model_type)
        return doc2vec_model.get_similarity(
            embedding1=try_get(obj,model_type),
            embedding2=embed[model_type],
            mode=model_type) * 0.6 + doc2vec_model.get_similarity(
            embedding1=doc2vec_model.get_embedding(text=obj["Title"].encode('utf8'), mode=model_type),
            embedding2=embed[model_type],
            mode=model_type) * 0.4


def cmp(a, b):
    if a["_source"]["score"] < b["_source"]["score"]:
        return 1
    if a["_source"]["score"] > b["_source"]["score"]:
        return -1
    """if a["_source"]["FYCJ"] < b["_source"]["FYCJ"]:
        return 1
    if a["_source"]["FYCJ"] > b["_source"]["FYCJ"]:
        return -1
    if a["_source"]["Title"] < b["_source"]["Title"]:
        return 1
    if a["_source"]["Title"] < b["_source"]["Title"]:
        return -1"""
    return 0

from functools import cmp_to_key
def reranking(result, query):
    model.load_model()
    # random.shuffle(result)
    # return result

    for a in range(0, len(result)):
        result[a]["_source"]["score"] = get_score(result[a]["_source"], query, result[a]["_score"])

    # nowp = 0
    # while nowp < len(result):
    #    nowf = get_feature(result[nowp]["_source"],query)
    #    print nowf
    #    if nowf[len(nowf) - 1] < 0.3:
    #        result = result[0:nowp] + result[nowp + 1:len(result)]
    #    else:
    #        nowp += 1

    result.sort(key=cmp_to_key(cmp))

    return result
