import os

size = 0
total = 0
dic = {}


def count_file(path):
    global total
    global size
    print path
    f = open(path, "r")

    print total, size

    for line in f:
        arr = line.split('\t')[1].split(' ')
        print arr

        gg

        total += len(arr)

        for x in arr:
            if not (x in dic):
                dic[x] = 0
                size += 1
            dic[x] += 1


def dfs_insert(path):
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            dfs_insert(path + x + "/")
        else:
            if x.endswith(".json"):
                count_file(path + x)


if __name__ == "__main__":
    path = "data/"

    dfs_insert(path)
