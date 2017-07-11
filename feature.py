import re
import jieba
import datetime
import time


def get_document_statistics(obj, query):
    obj["feature"]["statistics"] = {}

    keylist = ["WBWB", "DSRXX", "PubDate", "Title", "CPYZ", "AJJBQK", "PJJG", "content", "SSJL", "WBSB", "AJJBQK"]
    for word in keylist:
        obj["feature"]["statistics"][word + "_length"] = len(obj[word])
        obj["feature"]["statistics"][word + "_num_of_words"] = len(list(jieba.cut(obj[word])))

    obj["feature"]["statistics"]["judge_timestamp"] = int(
        time.mktime(datetime.datetime.strptime(obj["CPRQ"], "%Y-%m-%d").timetuple()))

    return obj


def get_classification_of_document(obj, query):
    obj["feature"]["classification"] = {}

    obj["feature"]["classification"]["FYCJ"] = obj["FYCJ"]
    obj["feature"]["classification"]["AJLX"] = obj["AJLX"]
    obj["feature"]["classification"]["WSLX"] = obj["WSLX"]

    return obj


def get_text_matching_feature(obj, query):
    content = query["search_content"]

    obj["feature"]["matching_result"] = {}

    # process 1
    word_list = list(jieba.cut(content))

    obj["feature"]["matching_result"]["matched_time"] = []
    obj["feature"]["matching_result"]["matched_or_not"] = []
    match_type = {
        "0": "content",
        "1": "WBSB",
        "2": "AJJBQK",
        "3": "CPYZ",
        "4": "PJJG",
        "5": "WBWB"
    }
    search_type = match_type[query["where_to_search"]]
    for a in range(0, len(word_list)):
        obj["feature"]["matching_result"]["matched_time"].append(len(re.findall(word_list[a], obj[search_type])))
        obj["feature"]["matching_result"]["matched_or_not"].append(len(re.findall(word_list[a], obj[search_type])) >= 1)

    return obj


def gen_ranking_feature(obj, query):
    obj["features"] = {}

    obj = get_text_matching_feature(obj, query)

    return obj
