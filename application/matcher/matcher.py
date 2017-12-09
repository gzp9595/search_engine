# coding=utf-8
from gensim import corpora, models, similarities
from application.util import print_time
from application.cutter import cut


def train_tfidf(text):
    import numpy as np
    dic = {}
    cnt = 0
    for a in range(0, len(text[0])):
        if not (text[0][a] in dic):
            dic[text[0][a]] = cnt
            cnt += 1

    tf = np.array(cnt, dtype=np.int32)
    idf = np.array(cnt, dtype=np.int32)
    for a in xrange(0, len(text)):
        for b in xrange(0, len(text[a])):
            arr = np.array(cnt,dtype=np.int32)
            if text[a][b] in dic:
                tf[dic[text[a][b]]] += 1
                arr[dic[text[a][b]]] = 1
            idf += arr


    return (dictionary, corpus, tfidf)


def get_best(search_content, document):
    text = document
    arr = [search_content]
    for a in range(0, max(1, len(text) - 100), 63):
        arr.append([])
        now = len(arr) - 1
        for b in range(0, 100):
            if a + b < len(text):
                arr[now].append(text[a + b])

    similarity = []
    se = set()
    for x in search_content:
        se.add(x)
    for x in arr:
        s = 0
        for y in x:
            if y in se:
                s += 1
        similarity.append(s)

    p = 0
    for a in range(1, len(similarity)):
        if similarity[a] > similarity[p]:
            p = a

    res = ""
    for x in arr[p]:
        find = False
        for y in se:
            if x == y:
                find = True
                break
        if len(x.decode("utf8")) == 1:
            find = False
        if find:
            res = res + "<highlight>" + x + "</highlight>"
        else:
            res = res + x

    return res


if __name__ == "__main__":
    document = "重庆市合川区人民法民 事 裁 定 （2014）合法民初字第07519原告石忠强，男，1982年2月8日出生，汉族，住重庆市合川区委托代理人蒋甲洪，重庆合州律师事务所律师被告何安国，男，1964年7月10日出生，汉族，住重庆市合川区本院在审理原告石忠强与被告何安国民间借贷纠纷一案中，原告石忠强2014年11月14日向本院提出撤诉申请本院认为，原告石忠强在本案诉讼期间申请对被告何安国撤诉，是在法律允许的范围内对自己的诉讼权利所作出的处分，原告石忠强提出的撤诉申请，符合法律规定的撤诉条件，本院予以准许。据此，依照《中华人民共和国民事诉讼法》第一百四十五条第一款、第一百五十四条第一款第（五）项的规定，裁定如下准许原告石忠强撤回对被告何安国的起诉案件受理费50元，减半收取25元，由原告石忠强负担审判员　　冯雪二〇一四年十一月十四书记员　　刘　颖"
    data = "借贷纠纷"

    print get_best(data, document)
