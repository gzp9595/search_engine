# coding: UTF-8
from application import app
from application.cutter import cut
import numpy as np

word_list = {}
f = open(app.config["WORD_FILE"], "r")
cnt = 0
arr = []
for line in f:
    word_list[line[0:len(line) - 1]] = cnt
    arr.append(line[0:len(line) - 1])
    cnt += 1
size = len(word_list)

mat = np.transpose(np.reshape(np.fromfile(app.config["VEC_FILE"], dtype=np.float32), (-1, app.config["VEC_SIZE"])))


def expand(sentence):
    origin = sentence
    setence = cut(sentence)[0]

    l = []
    for x in setence:
        if x in word_list:
            l.append(word_list[x])

    now_mat = np.dot(mat[:, l], mat)
    part_mat = np.argpartition(now_mat, size - app.confg["EXPAND_K"], axis=1)

    for a in range(0, len(l)):
        for b in range(size - app.confg["EXPAND_K"], size):
            if now_mat[a][part_mat[a][b]] > app.config["EXPAND_alpha"]:
                origin += " " + arr[part_mat[a][b]]

    return origin


if __name__ == "__main__":
    print expand(u"百科", 1, 5)
