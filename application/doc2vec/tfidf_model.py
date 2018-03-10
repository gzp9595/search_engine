import numpy
from gensim import corpora, models, similarities


class tfidf_model(object):
    def __init__(self, dict_path, tfidf_path):
        self.dictionary = corpora.Dictionary.load(dict_path)
        self.tfidf = models.TfidfModel.load(tfidf_path)

    def get_embedding(self, text):
        doc_bow = self.tfidf[self.dictionary.doc2bow(text)]
        result = {}
        for i in doc_bow:
            result[i[0]] = i[1]
        return result

    def get_similarity(self, embedding1, embedding2):
        result = 0.0
        l1 = 0.0
        l2 = 0.0
        for i in embedding1:
            if i in embedding2:
                result += embedding2[i] * embedding1[i]
            l1 += embedding1[i] * embedding1[i]
        for i in embedding2:
            l2 += embedding2[i] * embedding2[i]
        if (l1 == 0 or l2 == 0):
            return 0.0
        return result / pow(l1, 0.5) / pow(l2, 0.5)
