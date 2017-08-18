import json
import os

import application.processor.formatter

file_name = "C:\\work\\search_engine\\data\\newdata\\result\\" + "2015-02-16.json"

dir_name = "C:\\work\\search_engine\\data\\newdata\\result\\"


content = ""

cnt = 0

for x in os.listdir(dir_name):
    file_name=dir_name+x
    f = open(file_name, "r")
    for line in f:
        #print len(line)
        content = json.loads(line)
        application.processor.formatter.new_parse(content)

    #print

