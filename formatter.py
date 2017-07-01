#  -*- coding:utf-8 -*-

import os
import json
import re


def get_name_of_court(obj):
    return re.search(u"([\u4e00-\u9fa5]*法院[\u4e00-\u9fa5]*)", obj["WBSB"]).group()


def get_type_of_case(obj):
    if obj["content"] == "":
        return
    match1 = re.search(u"(([\u4e00-\u9fa5])\s([\u4e00-\u9fa5])\s裁\s定\s书)", obj["content"])
    match2 = re.search(u"(([\u4e00-\u9fa5])\s([\u4e00-\u9fa5])\s判\s决\s书)", obj["content"])
    #print match1
    #print match2
    result = ""
    #print match1 is None
    #print match2 is None
    if not (match1 is None):
        result = match1.group(2) + match1.group(3)
    elif not (match2 is None):
        result = match2.group(2) + match2.group(3)
    else:
        gg
    #print result

    opt = 0
    if result == u"刑事":
        opt = 1
    elif result == u"民事":
        opt = 2
    elif result == u"行政":
        opt = 3
    elif result == u"赔偿":
        opt = 4
    elif result == u"执行":
        opt = 5
    else:
        gg

    return opt


def get_number_of_case(obj):
    if obj["content"] == "":
        gg

    result = re.search(u'([\(（]\d+[\)）][\u4e00-\u9fa5\d]*\d+号)', obj["content"])
    return result.group()


def get_level_of_court(obj):
    if not("WBSB" in obj) or obj["WBSB"] == "":
        return 5

    if re.search(u"最高",obj["WBSB"] )is None:
        if re.search(u"高级",obj["WBSB"]) is None:
            if re.search(u"中级",obj["WBSB"]) is None:
                if re.search(u"法院",obj["WBSB"]) is None:
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

    try:
        obj["FYMC"] = get_name_of_court(obj)
    except Exception:
        aa

    try:
        obj["AJLX"] = get_type_of_case(obj)
    except Exception as e:
        bb

    try:
        obj["AJAH"] = get_number_of_case(obj)
    except Exception:
        cc

    try:
        obj["FYCJ"] = get_level_of_court(obj)
    except Exception:
        dd

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
