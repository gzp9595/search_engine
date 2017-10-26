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

print "Begin string"
print_time()
mat_id = np.reshape(np.fromfile(app.config["DIS_ID_FILE"], dtype=np.int32), (-1, app.config["MAX_K"]))
mat_value = np.reshape(np.fromfile(app.config["DIS_VALUE_FILE"], dtype=np.float32), (-1, app.config["MAX_K"]))

"""print "Begin matrix"
print_time()

mat = np.transpose(np.reshape(np.fromfile(app.config["VEC_FILE"], dtype=np.float32), (-1, app.config["VEC_SIZE"])))

mat /= np.sqrt((mat ** 2.).sum(axis=0, keepdims=True))
"""
print "Done"
print_time()


def expand(sentence, expand_k=None, expand_alpha=None):
    if expand_k is None:
        expand_k = int(app.config["EXPAND_K"])
    if expand_alpha is None:
        expand_alpha = float(app.config["EXPAND_ALPHA"])
    origin = sentence
    setence = cut(sentence)[0]

    l = []
    for x in setence:
        if x in word_list:
            l.append(word_list[x])

    """print "Being calculation"
    print_time()
    now_mat = np.dot(np.transpose(mat[:, l]), mat)
    part_mat = np.argpartition(now_mat, size - expand_k - 1, axis=1)
    print "Done"
    print_time()

    origin = ""
    for a in range(0, len(l)):
        print "Expand ", arr[l[a]]
        for b in range(size - expand_k - 1, size):
            if part_mat[a][b] != l[a] and now_mat[a][part_mat[a][b]] > expand_alpha:
                print arr[part_mat[a][b]], now_mat[a][part_mat[a][b]]
                origin += " " + arr[part_mat[a][b]]"""

    origin = ""
    for a in range(0, len(l)):
        print "Expand ", arr[l[a]]
        for b in range(1, expand_k + 1):
            (id_, value_) = (mat_id[l[a]][b], mat_value[l[a]][b])
            if value_ > expand_alpha:
                print id_, value_
                origin += " " + arr[id_]

    print origin
    return origin


if __name__ == "__main__":
    print expand(u"百科", 1, 5)
