#coding:utf-8
import numpy as np
import tensorflow as tf
import os
import time
import datetime
import random


class LSTM(object):

	def __init__(self, word_embeddings, config):

		self.batch_size = batch_size = config.batch_size
		self.num_steps = num_steps = config.num_steps
		size = config.hidden_size
		vocab_size = config.vocab_size
		num_classes = config.num_classes
		hits_k = config.hits_k
		self.input_x = tf.placeholder(tf.int32, [batch_size, num_steps])
		self.input_y = tf.placeholder(tf.float32, [batch_size, num_classes])
		self.keep_prob = tf.placeholder(tf.float32)

		lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(size, forget_bias = 1.0)

		lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=self.keep_prob)
		cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell] * config.num_layers)

		self.initial_state = cell.zero_state(batch_size, tf.float32)

		with tf.device("/cpu:0"), tf.name_scope("embedding"):
			embedding = tf.Variable(word_embeddings, trainable = False)
			inputs = tf.nn.embedding_lookup(embedding, self.input_x)

		outputs,_ = tf.nn.dynamic_rnn(cell,inputs,initial_state = self.initial_state)


		output = tf.expand_dims(tf.reshape(tf.concat(outputs,1), [batch_size, -1, size]), -1)

		with tf.name_scope("maxpool"):
			output_pooling = tf.nn.max_pool(output,
					ksize=[1, num_steps, 1, 1],
					strides=[1, 1, 1, 1],
					padding='VALID',
					name="pool")
			self.output = tf.reshape(output_pooling, [-1, size])

		with tf.name_scope("output"):
			softmax_w = tf.get_variable("softmax_w", [size, num_classes])
			softmax_b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="softmax_b")
			self.scores = tf.nn.xw_plus_b(self.output, softmax_w, softmax_b, name="scores")
			self.predictions = tf.argmax(self.scores, 1, name="predictions")

		with tf.name_scope("loss"):
			self.soft = tf.nn.softmax(self.scores)
			losses = tf.nn.softmax_cross_entropy_with_logits(logits = self.scores,labels =  self.input_y)
			self.loss = tf.reduce_mean(losses)

		with tf.name_scope("accuracy"):
			self.ans = tf.argmax(self.input_y, 1)
			correct_predictions = tf.equal(self.predictions, self.ans)
			self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")

class Config(object):

	def __init__(self):
		self.num_layers = 2
		self.batch_size = 64
		self.num_epochs = 20
		self.num_steps = 500
		self.hidden_size = 50
		self.vocab_size = 10000
		self.num_classes = 550
		self.hits_k = [1]

class lstm_model(object):
	def __init__(self, save_path):

		load_path(vec_path = save_path + '/word.vec', label_path = save_path + '/category')
		config = Config()
		config.hidden_size = len(self.word_embeddings[0])
		config.vocab_size = len(self.word_embeddings)
		config.num_classes = len(self.relationhash[0])
		
		eval_config = Config()
		eval_config.hidden_size = len(self.word_embeddings[0])
		eval_config.vocab_size = len(self.word_embeddings)
		eval_config.num_classes = len(self.relationhash[0])
		eval_config.batch_size = 1024

		
		out_config = Config()
		out_config.hidden_size = len(self.word_embeddings[0])
		out_config.vocab_size = len(self.word_embeddings)
		out_config.num_classes = len(self.relationhash[0])
		out_config.batch_size = 1

		self.model_path = save_path + '/lstmmodel/model'
		self.saver = tf.train.Saver()

		with tf.Graph().as_default():
			self.sess = tf.Session()
			with self.sess.as_default():
				initializer = tf.contrib.layers.xavier_initializer()
				with tf.variable_scope("model", reuse=None, initializer = initializer):
					self.m = LSTM(word_embeddings = self.word_embeddings, config = config)
				with tf.variable_scope("model", reuse=True, initializer = initializer):
					self.meval = LSTM(word_embeddings = self.word_embeddings, config = eval_config)
				with tf.variable_scope("model", reuse=True, initializer = initializer):
					self.mout = LSTM(word_embeddings = self.word_embeddings, config = out_config)


				lr = tf.Variable(0.001, trainable=False)
				global_step = tf.Variable(0, name="global_step", trainable=False)
				optimizer = tf.train.AdamOptimizer(lr)
				train_op = optimizer.minimize(m.loss,global_step = global_step)
				self.sess.run(tf.initialize_all_variables())


	def load_labels(self, vec_path, label_path):

		word_embeddings = []
		self.word2id = {}
		f = open(vec_path, "r")
		content = f.readline()
		while True:
			content = f.readline()
			if content == "":
				break
			content = content.strip().split()
			self.word2id[content[0]] = len(self.word2id)
			content = content[1:]
			content = [(float)(i) for i in content]
			word_embeddings.append(content)
		f.close()
		self.word2id['UNK'] = len(self.word2id)
		self.word2id['BLANK'] = len(self.word2id)
		lists = [0.0 for i in range(len(word_embeddings[0]))]
		word_embeddings.append(lists)
		word_embeddings.append(lists)
		self.word_embeddings = np.array(word_embeddings, dtype=np.float32)

		f = open(label.path,"r")
		self.relationhash = {}
		content = f.readline()
		while True:
			content = f.readline()
			if content == "":
				break
			content = content.strip()
			self.relationhash[content] = len(self.relationhash)


	def load_data(self, path):

		x_train = []
		y_train = []

		f = open(path + '', "r")
		content = f.readlines()
		random.shuffle(content)
		for i in content:
			z = i.strip().split("\t")
			if(len(z) != 2):
				continue
			x_train.append(z[0])
			y_train.append(z[1])

		f.close()
		print len(x_train)

		x_test = []
		y_test = []

		f = open(path + '', "r")
		content = f.readlines()
		for i in content:
			z = i.strip().split("\t")
			if(len(z) != 2):
				continue
			x_test.append(z[0])
			y_test.append(z[1])

		f.close()
		print len(x_test)

		res = []
		for i in xrange(0, len(y_test)):

			label = [0 for k in range(0, len(self.relationhash))]
			uid = relationhash[y_test[i]]
			label[uid] = 1
			res.append(label)

		y_test = np.array(res)

		for i in xrange(0, len(y_train)):

			label = [0 for k in range(0, len(self.relationhash))]
			uid = relationhash[y_train[i]]
			label[uid] = 1
			res.append(label)

		y_train = np.array(res)

		max_document_length_train = sum([len(x.split()) for x in x_train])/len(x_train)
		max_document_length_test = max([len(x.split()) for x in x_test])
		max_document_length = max(max_document_length_train, max_document_length_test)
		max_document_length = 500

		size = len(x_train)

		for i in xrange(size):
			blank = self.word2id['BLANK']
			text = [blank for j in xrange(max_document_length)]
			content = x_train[i].split()
			for j in xrange(len(content)):
				if(j == max_document_length):
					break
				if not content[j] in self.word2id:
					text[j] = self.word2id['UNK']
				else:
					text[j] = self.word2id[content[j]]
			x_train[i] = text
		x_train = np.array(x_train)

		size = len(x_test)
		for i in xrange(size):
			blank = self.word2id['BLANK']
			text = [blank for j in xrange(max_document_length)]
			content = x_test[i].split()
			for j in xrange(len(content)):
				if(j == max_document_length):
					break
				if not content[j] in self.word2id:
					text[j] = self.word2id['UNK']
				else:
					text[j] = self.word2id[content[j]]
			x_test[i] = text
		x_test = np.array(x_test)
		print 'init finish'
		return x_train, y_train, x_test, y_test


	def batch_iter(self, data, batch_size, num_epochs, shuffle=True):

		data = np.array(data)
		data_size = len(data)
		num_batches_per_epoch = (int)(round(len(data)/batch_size)) 
		for epoch in range(num_epochs):
				# Shuffle the data at each epoch
			if shuffle:
				shuffle_indices = np.random.permutation(np.arange(data_size))
				shuffled_data = data[shuffle_indices]
			else:
				shuffled_data = data
			for batch_num in range(num_batches_per_epoch):
				start_index = batch_num * batch_size
				end_index = min((batch_num + 1) * batch_size, data_size)
				yield shuffled_data[start_index:end_index]

	def Load(self):
		self.saver.restore(self.sess, self.model_path)

	def Train(path):

		def train_step(x_batch, y_batch):

			feed_dict = {
				self.m.input_x: x_batch,
				self.m.input_y: y_batch,
				self.m.keep_prob: 0.5
			}
			_, step, loss = self.sess.run(
				[train_op, global_step, self.m.loss], feed_dict)

			time_str = datetime.datetime.now().isoformat()

			if step % 500 == 0:
 				print("{}: step {}, loss {:g}".format(time_str, step, loss))

		def dev_step(x_batch, y_batch, writer=None):

			feed_dict = {
				self.mtest.input_x: x_batch,
				self.mtest.input_y: y_batch,
				self.mtest.keep_prob: 1.0
			}
			accuracy, loss = self.sess.run([self.mtest.accuracy, self.mtest.loss], feed_dict=feed_dict)

			return accuracy, loss

		x_train, y_train, x_dev, y_dev = load_data(path = path)
		batches = batch_iter(data = list(zip(x_train, y_train)), batch_size = config.batch_size, num_epochs = config.num_epochs)

		for batch in batches:
			x_batch, y_batch = zip(*batch)
			train_step(x_batch, y_batch)
			current_step = tf.train.global_step(self.sess, global_step)

			if current_step % 2000 == 0:

				print("\nEvaluation:")
				
				for i in range(num):
					accuracy, loss = dev_step(x_dev[i * eval_config.batch_size:(i+1)*eval_config.batch_size], y_dev[i * eval_config.batch_size:(i+1)*eval_config.batch_size])

					losses += loss
					accuracys += accuracy

				print 'accuracy = ' + str(accuracys / num)
				print 'loss = ' + str(losses / num)


	# def Outout_Re(x_batch):

	# 	feed_dict = {
	# 		m.input_x: x_batch,
	# 		m.keep_prob: 1.0
	# 	}
	# 	output = sess.run([m.output], feed_dict=feed_dict)
	# 	return output


	# def output():
	# 	num = (int)(len(y_train) / (float)(eval_config.batch_size))

	# 	fx = open('/data/disk1/private/lx/law/Re/train_x.txt','w')
	# 	for i in range(num):
	# 		output = Outout_Re(x_train[i * eval_config.batch_size:(i+1)*eval_config.batch_size])
	# 		for k in output[0]:
	# 			for j in k:
	# 				fx.write(str(j) + ' ')
	# 			fx.write('\n')

	# 	fx = open('/data/disk1/private/lx/law/Re/test_x.txt','w')
			
	# 	num = (int)(len(y_dev) / (float)(eval_config.batch_size))
	# 	# print num
			
	# 	for i in range(num):
	# 		output = Outout_Re(x_dev[i * eval_config.batch_size:(i+1)*eval_config.batch_size])
	# 		for k in output[0]:
	# 			for j in k:
	# 				fx.write(str(j) + ' ')
	# 			fx.write('\n')

	# 	left = len(y_dev) - num * eval_config.batch_size
	# 	output = Outout_Re(np.append(x_dev[num * eval_config.batch_size:], [zero_x for i in range(eval_config.batch_size - left)], axis = 0))

	# 	for k in range(left):
	# 		for j in output[0][k]:
	# 			fx.write(str(j) + ' ')
	# 		fx.write('\n')




if __name__ == "__main__":
	tf.app.run()