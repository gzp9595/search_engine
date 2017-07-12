import feature
import numpy as np
import os

X = []
Y = []
length = 11 * 2 + 1 + 3 + 2
layer = (2 * np.random.random((length, 1)) - 1)


def write_model():
    global layer
    f = open("model", "w")
    for a in range(0, length):
        print >> f, layer[a][0]
    f.close()


if os.path.exists("model"):
    f = open("model", "r")
    cnt = 0
    for line in f:
        layer[cnt] = [float(line)]
        cnt += 1
    f.close()
else:
    write_model()


def train(iter):
    global layer
    for a in range(0, iter):
        l0 = np.array(X)
        l1 = 1 / (1 + np.exp(-np.dot(l0, layer)))
        l1_error = Y - l1
        print l1_error
        l1_delta = l1_error * (l1 * (1 - l1))
        print l1_delta
        layer += np.dot(l0.T, l1_delta)
    write_model()


def judge(vec):
    global layer
    return 1 / (1 + np.exp(-np.dot(vec, layer)))


def get_feature(obj):
    feature = []

    keylist = ["WBWB", "DSRXX", "PubDate", "Title", "CPYZ", "AJJBQK", "PJJG", "content", "SSJL", "WBSB", "AJJBQK"]
    for word in keylist:
        feature.append(obj["feature"]["statistics"][word + "_length"])
        feature.append(obj["feature"]["statistics"][word + "_num_of_words"])

    feature.append(obj["feature"]["statistics"]["judge_timestamp"])

    feature.append(obj["feature"]["classification"]["FYCJ"])
    feature.append(obj["feature"]["classification"]["AJLX"])
    feature.append(obj["feature"]["classification"]["WSLX"])

    feature.append(np.average(obj["feature"]["matching_result"]["matched_time"]))
    feature.append(np.average(obj["feature"]["matching_result"]["matched_or_not"]))

    return feature


def add_data(obj, query,score):
    global X, Y
    X.append(get_feature(feature.gen_ranking_feature(obj,query)))
    Y.append([score])
    if len(X) % 5 == 0:
        train(3)


def get_score(obj):
    return judge(get_feature(obj))


def cmp(a, b):
    if a["_source"]["score"] < b["_source"]["score"]:
        return 1
    if a["_source"]["score"] > b["_source"]["score"]:
        return -1
    return 0


def reranking(result, query):
    for a in range(0, len(result)):
        result[a]["_source"] = feature.gen_ranking_feature(result[a]["_source"], query)
        result[a]["_source"]["score"] = get_score(result[a]["_source"])

    nowp = 0
    while nowp<len(result):
        nowf = get_feature(result[nowp]["_source"])
        print nowf
        if nowf[len(nowf)-1]<0.3:
            result=result[0:nowp]+result[nowp+1:len(result)]
        else:
            nowp += 1

    result.sort(cmp)

    return result
