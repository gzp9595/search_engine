from gensim import corpora,models,similarities
import numpy as np

class lda_model(object):
	def __init__(self, save_path):

		self.num_topics = 10
		self.save_path = save_path

	def train(self, text):

		con = []
		for i in texts:
			tmp = []
			for j in i:
				tmp.append(j)
			con.append(tmp)


		print 'train',len(con)

		self.dictionary = corpora.Dictionary(con)
		corpus = [ self.dictionary.doc2bow(text) for text in con ]
		self.tfidf = models.TfidfModel(corpus)
		corpus_tfidf = self.tfidf[corpus]
		self.lda = models.LdaModel(corpus=corpus, id2word=self.dictionary, num_topics=self.num_topics)
		self.lda.save(self.save_path + '/lda')
		self.dictionary.save(self.save_path + '/dic')
		self.tfidf.save(self.save_path + '/tfidf')

	def load(self):
		self.lda = models.LdaModel.load(self.save_path + '/lda')
		self.dictionary = corpora.Dictionary.load(self.save_path + '/dic')
		self.tfidf = models.TfidfModel.load(self.save_path + '/tfidf')

	def print_topic(self):
		topic_list = self.lda.print_topics(self.num_topics)

		f1 = open('topic.txt','w')
		for topic in topic_list:
			f1.write(topic[1].encode('utf8') + '\n')

	def get_embedding(self, text):
		doc_bow = self.tfidf[self.dictionary.doc2bow(text)]
		doc_lda = self.lda[doc_bow]
		ret = [0.0] * self.num_topics
		for i in doc_lda:
			ret[i[0]] = i[1]
		#print ret
		return ret

	def get_similarity(self, embedding1, embedding2):
		embedding1 = np.array(embedding1)
		embedding2 = np.array(embedding2)
		if len(embedding1) != len(embedding2):
			print "dimension unmatched"
			return 0
		result = 0.0
		l1 = 0.0
		l2 = 0.0
		for i in range(len(embedding1)):
			result += embedding1[i]*embedding2[i]
			l1 += embedding1[i]*embedding1[i]
			l2 += embedding2[i]*embedding2[i]
		return result/pow(l1, 0.5)/pow(l2, 0.5)
	
