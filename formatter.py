#encoding = utf8

import os
import json


def test():
    for x in os.listdir("data/law/small_data"):
        f = open("data/law/small_data/"+ x, 'r')
        content = ''
        for line in f:
            content = json.loads(line)
            break
        print content
        f = open('test.log','w')
        for y in content:
            print >> f,y,content[y].encode('utf8')
        break

if __name__=="__main__":
    test()