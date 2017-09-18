import os

size = 0
total = 0
tf = {}
idf = {}


def count_file(path):
    global total
    global size
    print path
    f = open(path, "r")

    print total, size
    cnt = 0

    for line in f:
        cnt += 1
        if cnt % 10000 == 0:
            print total, size
        arr = line.split('\t')[1].split(' ')

        total += len(arr)

        cur = {}
        for x in arr:
            if not (x in cur):
                cur[x] = 0
            cur[x] += 1

        for x in cur:
            if not (x in tf):
                tf[x] = 0
                idf[x] = 0
                size += 1
            tf[x] += cur[x]
            idf[x] += 1


def dfs_insert(path):
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            dfs_insert(path + x + "/")
        else:
            count_file(path + x)


if __name__ == "__main__":
    path = "data/"

    dfs_insert(path)

    for x in tf:
        print x, tf[x], idf[x]
