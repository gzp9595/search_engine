# coding=utf-8
from application import app


def count_level(obj_list):
    match_list = ["", u"最高人民法院", u"高级人民法院", u"中级人民法院", u"基层人民法院", u"其他法院"]
    result = {}
    for a in range(1, len(match_list)):
        result[match_list[a]] = 0

    for x in obj_list:
        if "FYCJ" in x:
            if x["FYCJ"] == 0:
                continue
            result[match_list[x["FYCJ"]]] += 1

    return result


def count_case_type(obj_list):
    match_list = ["", u"刑事", u"民事", u"行政", u"赔偿", u"执行", u"其他"]
    result = {}
    for a in range(1, len(match_list)):
        result[match_list[a]] = 0

    for x in obj_list:
        if "AJLX" in x:
            if x["AJLX"] == 0:
                continue
            result[match_list[x["AJLX"]]] += 1

    return result


def count_doc_type(obj_list):
    match_list = ["", u"判决书", u"裁定书", u"调解书", u"决定书", u"通知书", u"批复", u"答复", u"函", u"令", u"其他"]
    result = {}
    for a in range(1, len(match_list)):
        result[match_list[a]] = 0

    for x in obj_list:
        if "WSLX" in x:
            if x["WSLX"] == 0:
                continue
            result[match_list[x["WSLX"]]] += 1

    return result


def count_judge_date(obj_list):
    result = {"year": {}, "month": {}, "day": {}}
    for x in obj_list:
        if not ("CPRQ" in x):
            continue
        arr = x["CPRQ"].split("-")
        year = int(arr[0])
        month = int(arr[1])
        day = int(arr[2])
        if not (year in result["year"]):
            result["year"][year] = 0
        result["year"][year] += 1
        if not (month in result["month"]):
            result["month"][month] = 0
        result["month"][month] += 1
        if not (day in result["day"]):
            result["day"][day] = 0
        result["day"][day] += 1

    return result


def count_pub_date(obj_list):
    result = {"year": {}, "month": {}, "day": {}}
    for x in obj_list:
        if not ("PubDate" in x):
            continue
        arr = x["PubDate"].split("-")
        year = int(arr[0])
        month = int(arr[1])
        day = int(arr[2])
        if not (year in result["year"]):
            result["year"][year] = 0
        result["year"][year] += 1
        if not (month in result["month"]):
            result["month"][month] = 0
        result["month"][month] += 1
        if not (day in result["day"]):
            result["day"][day] = 0
        result["day"][day] += 1

    return result


def count_region(obj_list):
    l = [u"辽宁", u"吉林", u"黑龙江", u"河北", u"山西", u"陕西", u"山东", u"安徽", u"江苏", u"浙江", u"河南", u"湖北", u"湖南", u"江西", u"福建",
         u"云南", u"海南", u"四川", u"贵州", u"广东", u"甘肃", u"青海", u"西藏", u"新疆", u"广西", u"内蒙古", u"宁夏", u"北京", u"天津", u"上海",
         u"重庆", u"香港", u"澳门", u"台湾"]

    result = {}
    for x in l:
        result[x] = 0

    for x in obj_list:
        for y in l:
            if y in x["content"]:
                result[y] += 1

    return result


def get_info(obj_list):
    l = []
    for x in obj_list:
        l.append(x["_source"])
    obj_list = l
    result = {}

    result["court_level"] = count_level(obj_list)
    result["type_case"] = count_case_type(obj_list)
    result["type_doc"] = count_doc_type(obj_list)
    result["judge_date"] = count_judge_date(obj_list)
    result["pub_date"] = count_pub_date(obj_list)
    result["region"] = count_region(obj_list)

    return result
