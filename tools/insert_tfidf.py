import os

dir_path = "/mnt/data/tfidf_embedding/"

for x in os.listdir(dir_path):
    file_name = dir_path + x
    f = open(file_name,"r")
    for line in f:
        arr = line.split('\t')
        print arr[0]
        print arr[1]

        gg