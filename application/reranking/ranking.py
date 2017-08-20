from application import app
from application.reranking import classifer, feature

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

doc2vec_model = Doc2vec(save_path=app.config["DOC2VEC_PATH"])


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
    print score
    file_name = str(uuid.uuid4())
    f = open(app.config["TRAINING_DIR"] + file_name + ".json", "w")
    print >> f, json.dumps({"obj": obj, "query": query, "score": score})
    f.close()


def get_score(obj, query,sc):
    model_type=int(query["type_of_model"])
    print model_type
    if model_type == -2:
        return sc
    if model_type == -1:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return model.judge(get_feature(obj, query))
    else:
        return doc2vec_model.get_similarity(
            embedding1=doc2vec_model.get_embedding(text=obj["content"].encode('utf8'), mode=model_type),
            embedding2=doc2vec_model.get_embedding(text=query["search_content"].encode('utf8'), mode=model_type),
            mode=model_type)


def cmp(a, b):
    if a["_source"]["score"] < b["_source"]["score"]:
        return 1
    if a["_source"]["score"] > b["_source"]["score"]:
        return -1
    if a["_source"]["FYCJ"] < b["_source"]["FYCJ"]:
        return 1
    if a["_source"]["FYCJ"] > b["_source"]["FYCJ"]:
        return -1
    if a["_source"]["Title"] < b["_source"]["Title"]:
        return 1
    if a["_source"]["Title"] < b["_source"]["Title"]:
        return -1
    return 0


def reranking(result, query):
    model.load_model()
    # random.shuffle(result)
    # return result

    for a in range(0, len(result)):
        result[a]["_source"]["score"] = get_score(result[a]["_source"], query,result[a]["_score"])

    # nowp = 0
    # while nowp < len(result):
    #    nowf = get_feature(result[nowp]["_source"],query)
    #    print nowf
    #    if nowf[len(nowf) - 1] < 0.3:
    #        result = result[0:nowp] + result[nowp + 1:len(result)]
    #    else:
    #        nowp += 1

    result.sort(cmp)

    return result
