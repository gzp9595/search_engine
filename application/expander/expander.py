# coding: UTF-8
from application import app
from application.cutter import cut
import gensim

#model = gensim.models.Word2Vec.load(app.config["DOC2VEC_PATH"])


def expand(word, mode, bound):
    return model.most_similar(positive=[word], topn=bound)


def get_expand(text):
    cut_result = cut(text)
    result = []
    for x in cut_result:
        s = expand(x,0,2)
        for y in s:
            result.append(y)

    for x in result:
        text = text + " "+ x
    print text

    return text

if __name__ == "__main__":
    print expand(u"百科", 1, 5)
