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
    result = ""
    if not (match1 is None):
        result = match1.group(2) + match1.group(3)
    elif not (match2 is None):
        result = match2.group(2) + match2.group(3)
    else:
        gg
    print result

    opt = 0
    if result == "刑事":
        opt = 1
    elif result == "民事":
        opt = 2
    elif result == "行政":
        opt = 3
    elif result == "赔偿":
        opt = 4
    elif result == "执行":
        opt = 5
    else:
        gg

    return opt

def get_number_of_case(obj):
    if obj["content"] == "":
        gg

    result = re.search(u'([\(（]\d+[\)）][\u4e00-\u9fa5\d]*\d+号)',obj["content"])
    print result.group()


def test():
    fout = open('test.log', 'w')
    cnt = 0
    for x in os.listdir("data/law/small_data"):
        fin = open("data/law/small_data/" + x, 'r')
        content = ''
        for line in fin:
            content = json.loads(line)
            break
        print >> fout,x
        for y in content:
            print >> fout, y, content[y].encode('utf8')
        print >> fout

        #if "WBSB" in content or "" in content:
        #    continue
        #    print >> fout,content["WBSB"].encode('utf8')
        #    print >> fout
        #else:
        #    print >> fout,x
        #    for y in content:
        #        print >> fout, y, content[y].encode('utf8')
        #    print >> fout
        # if "WBSB" in content:
        #    print get_name_of_court(content)
        #if content["content"]!="":
        #    get_number_of_case(content)
        cnt += 1
        if cnt >= 20:
            break
    fout.close()


if __name__ == "__main__":
    test()
