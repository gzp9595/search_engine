import numpy as np
class wordembedding_model(object):
	def __init__(self, wordembedding_path = '../train/words.vec'):

		f_vec = open(wordembedding_path, 'r')
		lines = f_vec.readlines()
		info = lines[0].strip().split(' ')
		self.embedding_size = int(info[1])
		self.word2id = {}
		self.word_embedding = []
		for i in range(1, len(lines)):
			rep = lines[i].strip().split(' ')
			self.word2id[rep[0]] = len(self.word2id)
			temp = []
			for j in range(1, len(rep)):
				temp.append(float(rep[j]))
			self.word_embedding.append(temp)

		self.dict_size = len(self.word2id)

	def get_embedding(self, text):
		result = np.array([0.0 for i in range(self.embedding_size)])
		count = 0
		for word in text:
			if word in self.word2id:
				id = self.word2id[word]
				result += np.array(self.word_embedding[id])
				count += 1.0
		if(count == 0):
			return result
		result = result/count
		return result
	
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

