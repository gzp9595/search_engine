# coding=utf-8
from gensim import corpora, models, similarities
from application.util import print_time
from application.cutter import cut


def train_tfidf(text):
    dictionary = corpora.Dictionary(text)
    corpus = [dictionary.doc2bow(texts) for texts in text]
    tfidf = models.TfidfModel(corpus)

    return (dictionary, corpus, tfidf)


def get_best(search_content, document):
    text = document
    arr = []
    for a in range(0, max(1, len(text) - 100), 63):
        arr.append([])
        now = len(arr) - 1
        for b in range(0, 100):
            if a + b < len(text):
                arr[now].append(text[a + b])

    # print "Begin tfidf"
    # print_time()
    (dictionary, corpus, tfidf) = train_tfidf(arr)
    corpus_tfidf = tfidf[corpus]
    # print "End tfidf"
    # print_time()

    vec_bow = dictionary.doc2bow(search_content)
    vec_tfidf = tfidf[vec_bow]
    se = set()
    for x in search_content:
        se.add(x)

    try:
        index = similarities.MatrixSimilarity(corpus_tfidf)
        sims = index[vec_tfidf]
    except ValueError as e:
        sims = []
        for x in arr:
            s = 0
            for y in x:
                if y in se:
                    s += 1
            sims.append(s)

    # print "Begin similarity"
    # print_time()

    similarity = list(sims)
    # print "End similarity"
    # print_time()

    # for a in range(0, len(similarity)):
    #    print similarity[a],
    # print
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
    document = "�����кϴ��������� �� �� �� ��2014���Ϸ�����ֵ�07519ԭ��ʯ��ǿ���У�1982��2��8�ճ��������壬ס�����кϴ���ί�д����˽��׺飬���������ʦ��������ʦ����ΰ������У�1964��7��10�ճ��������壬ס�����кϴ�����Ժ������ԭ��ʯ��ǿ�뱻��ΰ������������һ���У�ԭ��ʯ��ǿ2014��11��14����Ժ����������뱾Ժ��Ϊ��ԭ��ʯ��ǿ�ڱ��������ڼ�����Ա���ΰ������ߣ����ڷ�������ķ�Χ�ڶ��Լ�������Ȩ���������Ĵ��֣�ԭ��ʯ��ǿ����ĳ������룬���Ϸ��ɹ涨�ĳ�����������Ժ����׼���ݴˣ����ա��л����񹲺͹��������Ϸ�����һ����ʮ������һ���һ����ʮ������һ��ڣ��壩��Ĺ涨���ö�����׼��ԭ��ʯ��ǿ���ضԱ���ΰ��������߰��������50Ԫ��������ȡ25Ԫ����ԭ��ʯ��ǿ��������Ա������ѩ����һ����ʮһ��ʮ�����Ա��������ӱ"
    data = "�������"

    print
    get_best(data, document)
