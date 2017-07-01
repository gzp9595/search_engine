#  -*- coding:utf-8 -*-

import os
import json
import re


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


def get_number_of_case(obj):
    if obj["content"] == "":
        gg

    result = re.search(u'([\(（]\d+[\)）][\u4e00-\u9fa5\d]*\d+[-\d+]?[号]?)', obj["content"])
    return result.group()


def get_level_of_court(obj):
    if not ("WBSB" in obj) or obj["WBSB"] == "":
        return 5

    if re.search(u"最高", obj["WBSB"]) is None:
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
        obj["AJAH"] = get_number_of_case(obj)
    except Exception:
        obj["AJAH"] = ""

    try:
        obj["FYCJ"] = get_level_of_court(obj)
    except Exception:
        obj["FYCJ"] = 5

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
        print >> fout, x
        for y in content:
            print >> fout, y, content[y].encode('utf8')
        print >> fout

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
            break
    fout.close()


if __name__ == "__main__":
    test()
