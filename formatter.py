#  -*- coding:utf-8 -*-

import os
import json
import re
import util


def get_name_of_court(obj):
    return re.search(u"([\u4e00-\u9fa5]*法院[\u4e00-\u9fa5]*)", obj["WBSB"]).group()


def get_type_of_case(obj):
    if obj["content"] == "":
        return

    word_list = [u"刑\s事", u"民\s事", u"行\s政", u"赔\s偿", u"执\s行"]

    for a in range(0, len(word_list)):
        match = re.search(word_list[a], obj["content"])
        if not (match is None):
            return a + 1

    gg


def get_type_of_doc(obj):
    if obj["Title"] == "":
        return 10

    word_list = [u"判决书", u"裁定书", u"调解书", u"决定书", u"通知书", u"批复", u"答复", u"函", u"令"]

    for a in range(0,len(word_list)):
        match = re.search(word_list[a], obj["Title"])
        if not (match is None):
            return a + 1

    #print obj["Title"]

    return 10


def get_number_of_case(obj):
    if obj["content"] == "":
        gg

    result = re.search(u'([\(（]\d+[\)）][\u4e00-\u9fa5\d]*\d+[-\d+]?[号]?)', obj["content"])
    return result.group()


def get_level_of_court(obj):
    if not ("WBSB" in obj) or obj["WBSB"] == "":
        return 5

    if re.search(u"最高人民法院  ", obj["WBSB"]) is None:
        if re.search(u"高级", obj["WBSB"]) is None:
            if re.search(u"中级", obj["WBSB"]) is None:
                if re.search(u"法院", obj["WBSB"]) is None:
                    return 5
                else:
                    return 4
            else:
                return 3
        else:
            return 2
    else:
        return 1

    gg


def get_date_of_judgement(obj):
    if not ("WBWB" in obj):
        return

    if not (re.search(u"中华人民共和国民法通则", obj["WBWB"]) is None):
        return

    if not (re.search(u"李哲", obj["WBWB"]) is None):
        return

    date_list = {
        u"〇": 0,
        u"\uff2f": 0,
        u"\u3007": 0,
        u"\u25cb": 0,
        u"\uff10": 0,
        u"\u039f": 0,
        "O": 0,
        "0": 0,
        u"一": 1,
        u"元": 1,
        u"二": 2,
        u'三': 3,
        u'四': 4,
        u'五': 5,
        u'六': 6,
        u'七': 7,
        u'八': 8,
        u'九': 9,
        u'十': 10
    }
    # print obj["WBWB"]
    result = re.search(u"([O|\d|\uff2f|\u3007|\u25cb|\uff10|\u039f|\u4e00-\u9fa5]{4})年([\u4e00-\u9fa5]*)月", obj["WBWB"])
    p = obj["WBWB"].find(result.group()) + len(result.group())
    while obj["WBWB"][p] == u"月":
        p += 1
    endp = p
    while obj["WBWB"][endp] in date_list:
        endp += 1

    year_str = result.group(1)
    month_str = result.group(2)
    day_str = obj["WBWB"][p:endp]

    year = 0
    for a in range(0, len(year_str)):
        year = year * 10 + date_list[year_str[a]]

    month = 0
    if len(month_str) == 1:
        month = date_list[month_str[0]]
    else:
        month = 10 + date_list[month_str[1]]

    day = 0
    if day_str == "":
        return

    if len(day_str) > 3:
        day_str = day_str[0:3]
    if len(day_str) == 1:
        day = date_list[day_str[0]]
    elif len(day_str) == 2:
        if day_str[0] == u"十":
            day = 10 + date_list[day_str[1]]
        elif day_str[1] == u"十":
            day = date_list[day_str[0]] * 10
        else:
            day = date_list[day_str[0]] * 10 + date_list[day_str[1]]
    elif len(day_str) == 3:
        day = date_list[day_str[0]] * 10 + date_list[day_str[2]]
    else:
        gg

    year_str = str(year)
    while len(year_str) < 4:
        year_str = "0" + year_str

    month_str = str(month)
    while len(month_str) < 2:
        month_str = "0" + month_str

    day_str = str(day)
    while len(day_str) < 2:
        day_str = "0" + day_str
    if not (util.check_date(year_str, month_str, day_str)):
        gg

    return year_str + "-" + month_str + "-" + day_str


def parse(obj):
    if not ("content" in obj) or obj["content"] == "":
        return obj

    if "" in obj and not ("WBSB" in obj):
        obj["WBSB"] = obj[""]

    if "" in obj:
        obj.pop("", None)

    if not ("AJJBQK" in obj) and "SSJL" in obj:
        obj["AJJBQK"] = obj["SSJL"]

    try:
        if "WBSB" in obj:
            obj["FYMC"] = get_name_of_court(obj)
        else:
            obj["FYMC"] = ""
    except Exception:
        obj["FYMC"] = ""

    try:
        obj["AJLX"] = get_type_of_case(obj)
    except Exception as e:
        obj["AJLX"] = 0

    try:
        obj["WSLX"] = get_type_of_doc(obj)
    except Exception:
        obj["WSLX"] = 10

    try:
        obj["AJAH"] = get_number_of_case(obj)
    except Exception:
        obj["AJAH"] = ""

    try:
        obj["FYCJ"] = get_level_of_court(obj)
    except Exception:
        obj["FYCJ"] = 5

    try:
        if "WBWB" in obj:
            obj["CPRQ"] = get_date_of_judgement(obj)
        else:
            obj["CPRQ"] = "1900-01-01"
    except Exception:
        obj["CPRQ"] = "1900-01-01"

    keylist = ["WBWB", "DSRXX", "PubDate", "Title", "CPYZ", "AJJBQK", "PJJG", "content", "SSJL", "WBSB", "AJJBQK"]

    for key in keylist:
        if not (key in obj):
            obj[key] = ""

    return obj


def test():
    fout = open('test.log', 'w')
    cnt = 0
    for x in os.listdir("data/law/small_data"):
        fin = open("data/law/small_data/" + x, 'r')
        content = ''
        for line in fin:
            content = json.loads(line)
            break
        #print >> fout, x
        #for y in content:
        #    print >> fout, y, content[y].encode('utf8')
        #print >> fout
        get_type_of_doc(content)
        # try:
        #    get_date_of_judgement(content)
        # except AttributeError:
        #    continue

        # if "WBSB" in content or "" in content:
        #    continue
        #    print >> fout,content["WBSB"].encode('utf8')
        #    print >> fout
        # else:
        #    print >> fout,x
        #    for y in content:
        #        print >> fout, y, content[y].encode('utf8')
        #    print >> fout
        # if "WBSB" in content:
        #    print get_name_of_court(content)
        # if content["content"]!="":
        #    get_number_of_case(content)
        cnt += 1
        if cnt >= 20:
            continue
            break
    fout.close()


if __name__ == "__main__":
    test()
