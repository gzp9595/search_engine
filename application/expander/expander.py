# coding: UTF-8
from application import app
from application.cutter import cut
from application.util import print_time
import numpy as np

word_list = {}
print "Begin read"
print_time()
f = open(app.config["WORD_FILE"], "r")
cnt = 0
arr = []
for line in f:
    word_list[line[0:len(line) - 1]] = cnt
    arr.append(line[0:len(line) - 1])
    cnt += 1
size = len(word_list)
print "Begin matrix"
print_time()

mat = np.transpose(np.reshape(np.fromfile(app.config["VEC_FILE"], dtype=np.float32), (-1, app.config["VEC_SIZE"])))

mat /= np.sqrt((mat ** 2.).sum(axis=0, keepdims=True))

print "Done"
print_time()


def expand(sentence):
    origin = sentence
    setence = cut(sentence)[0]

    l = []
    for x in setence:
        if x in word_list:
            l.append(word_list[x])

    print "Being calculation"
    print_time()
    now_mat = np.dot(np.transpose(mat[:, l]), mat)
    part_mat = np.argpartition(now_mat, size - app.config["EXPAND_K"] -1, axis=1)
    print "Done"
    print_time()

    for a in range(0, len(l)):
        print "Expand ",arr[l[a]]
        for b in range(size - app.config["EXPAND_K"]-1, size):
            if part_mat[a][b]!=l[a] and now_mat[a][part_mat[a][b]] > app.config["EXPAND_ALPHA"]:
                print arr[part_mat[a][b]],now_mat[a][part_mat[a][b]]
                origin += " " + arr[part_mat[a][b]]

    print origin
    return origin


if __name__ == "__main__":
    print expand(u"百科", 1, 5)
