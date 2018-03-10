# coding:utf-8
import numpy as np
import tensorflow as tf
import os
import time
import datetime
import random
from init import *
import os


class TextCNN(object):
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
        filter_sizes = config.filter_sizes
        num_filters = config.num_filters
        l2_loss = tf.constant(0.0)

        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            embedding = tf.Variable(word_embeddings, trainable=False)
            inputs = tf.nn.embedding_lookup(embedding, self.input_x)
            self.inputs = tf.expand_dims(inputs, -1)

        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                filter_shape = [filter_size, size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
                conv = tf.nn.conv2d(
                    self.inputs,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv")

                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, num_steps - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool")
                pooled_outputs.append(pooled)

        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool = tf.concat(3, pooled_outputs)
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])

        with tf.name_scope("dropout"):
            self.output = tf.nn.dropout(self.h_pool_flat, self.keep_prob)

        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            # l2_loss += tf.nn.l2_loss(W)
            # l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.output, W, b, name="scores")
            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        with tf.name_scope("loss"):
            self.soft = tf.nn.softmax(self.scores)
            losses = tf.nn.softmax_cross_entropy_with_logits(self.scores, self.input_y)
            self.loss = tf.reduce_mean(losses)  # + 0.0001 * l2_loss

        with tf.name_scope("accuracy"):
            self.ans = tf.argmax(self.input_y, 1)
            correct_predictions = tf.equal(self.predictions, self.ans)
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")


class Config(object):
    def __init__(self):
        self.num_layers = 2
        self.batch_size = 32
        self.num_epochs = 20
        self.num_steps = 500
        self.hidden_size = 50
        self.vocab_size = 10000
        self.num_classes = 550
        self.hits_k = [1]
        self.filter_sizes = [3, 4, 5]
        self.num_filters = 100


class cnn_model(object):
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

        f = open(label_path, "r")
        self.relationhash = {}
        while True:
            content = f.readline()
            if content == "":
                break
            content = content.strip()
            self.relationhash[content] = len(self.relationhash)

    def __init__(self, save_path):

        self.load_labels(vec_path=save_path + '/words.vec', label_path=save_path + '/category')
        self.config = Config()
        self.config.hidden_size = len(self.word_embeddings[0])
        self.config.vocab_size = len(self.word_embeddings)
        self.config.num_classes = len(self.relationhash)

        self.eval_config = Config()
        self.eval_config.hidden_size = len(self.word_embeddings[0])
        self.eval_config.vocab_size = len(self.word_embeddings)
        self.eval_config.num_classes = len(self.relationhash)
        self.eval_config.batch_size = 1024

        self.out_config = Config()
        self.out_config.hidden_size = len(self.word_embeddings[0])
        self.out_config.vocab_size = len(self.word_embeddings)
        self.out_config.num_classes = len(self.relationhash)
        self.out_config.batch_size = 1

        self.model_path = save_path + '/cnnmodel/model'
        self.load_path = save_path + '/cnnmodel/model-9100'

        with tf.Graph().as_default():
            self.sess = tf.Session()
            with self.sess.as_default():
                initializer = tf.contrib.layers.xavier_initializer()
                with tf.variable_scope("model", reuse=None, initializer=initializer):
                    self.m = TextCNN(word_embeddings=self.word_embeddings, config=self.config)
                with tf.variable_scope("model", reuse=True, initializer=initializer):
                    self.mtest = TextCNN(word_embeddings=self.word_embeddings, config=self.eval_config)
                with tf.variable_scope("model", reuse=True, initializer=initializer):
                    self.mout = TextCNN(word_embeddings=self.word_embeddings, config=self.out_config)

                self.saver = tf.train.Saver()

                lr = tf.Variable(0.001, trainable=False)
                self.global_step = tf.Variable(0, name="global_step", trainable=False)
                optimizer = tf.train.AdamOptimizer(lr)
                self.train_op = optimizer.minimize(self.m.loss, global_step=self.global_step)

                self.sess.run(tf.initialize_all_variables())

    def load_data(self, path):

        x_train = []
        y_train = []

        f = open('/data/disk1/private/lixiang/out_content_id_10w_train', "r")
        content = f.readlines()
        random.shuffle(content)
        for i in content:
            z = i.strip().split("\t")
            if (len(z) != 2):
                continue
            x_train.append(z[0])
            y_train.append(z[1])

        f.close()
        print
        len(x_train)

        x_test = []
        y_test = []

        f = open('/data/disk1/private/lixiang/out_content_id_10w_test', "r")
        content = f.readlines()
        for i in content:
            z = i.strip().split("\t")
            if (len(z) != 2):
                continue
            x_test.append(z[0])
            y_test.append(z[1])

        f.close()
        print
        len(x_test)

        res = []
        num_r = [0, 0, 0, 0, 0]
        for i in xrange(0, len(y_test)):
            label = [0 for k in range(0, len(self.relationhash))]
            uid = self.relationhash[y_test[i]]
            label[uid] = 1
            res.append(label)
            num_r[uid] += 1

        fx = open('rel', 'w')
        for i in range(len(self.relationhash)):
            fx.write(str(num_r[i]) + '\n')

        y_test = np.array(res)

        res = []
        for i in xrange(0, len(y_train)):
            label = [0 for k in range(0, len(self.relationhash))]
            uid = self.relationhash[y_train[i]]
            label[uid] = 1
            res.append(label)

        y_train = np.array(res)

        max_document_length_train = sum([len(x.split()) for x in x_train]) / len(x_train)
        max_document_length_test = max([len(x.split()) for x in x_test])
        max_document_length = max(max_document_length_train, max_document_length_test)
        max_document_length = 500

        size = len(x_train)

        for i in xrange(size):
            blank = self.word2id['BLANK']
            text = [blank for j in xrange(max_document_length)]
            content = x_train[i].split()
            for j in xrange(len(content)):
                if (j == max_document_length):
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
                if (j == max_document_length):
                    break
                if not content[j] in self.word2id:
                    text[j] = self.word2id['UNK']
                else:
                    text[j] = self.word2id[content[j]]
            x_test[i] = text
        x_test = np.array(x_test)
        print
        'init finish'
        return x_train, y_train, x_test, y_test

    def batch_iter(self, data, batch_size, num_epochs, shuffle=True):

        data = np.array(data)
        data_size = len(data)
        num_batches_per_epoch = (int)(round(len(data) / batch_size))
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
        self.saver.restore(self.sess, self.load_path)

    def Train(self, path):

        def train_step(x_batch, y_batch):

            feed_dict = {
                self.m.input_x: x_batch,
                self.m.input_y: y_batch,
                self.m.keep_prob: 0.5
            }
            _, step, loss, accuracy = self.sess.run(
                [self.train_op, self.global_step, self.m.loss, self.m.accuracy], feed_dict)

            time_str = datetime.datetime.now().isoformat()

            if step % 50 == 0:
                print("{}: step {}, loss {:g}, accuracy {:g}".format(time_str, step, loss, accuracy))

        def dev_step(x_batch, y_batch, writer=None):

            feed_dict = {
                self.mtest.input_x: x_batch,
                self.mtest.input_y: y_batch,
                self.mtest.keep_prob: 1.0
            }
            accuracy, loss = self.sess.run([self.mtest.accuracy, self.mtest.loss], feed_dict=feed_dict)

            return accuracy, loss

        # _, x_train, y_train, x_dev, y_dev, sz, answer, namehash = load_data_and_labels(path = path)
        x_train, y_train, x_dev, y_dev = self.load_data(path=path)
        batches = self.batch_iter(data=list(zip(x_train, y_train)), batch_size=self.config.batch_size,
                                  num_epochs=self.config.num_epochs)

        with tf.Graph().as_default():
            with self.sess.as_default():

                for batch in batches:
                    x_batch, y_batch = zip(*batch)
                    train_step(x_batch, y_batch)
                    current_step = tf.train.global_step(self.sess, self.global_step)

                    if current_step % 100 == 0:
                        accuracys = 0.0
                        losses = 0.0

                        print("\nEvaluation:")
                        num = (int)(len(y_dev) / (float)(self.eval_config.batch_size))
                        print
                        num
                        for i in range(num):
                            accuracy, loss = dev_step(
                                x_dev[i * self.eval_config.batch_size:(i + 1) * self.eval_config.batch_size],
                                y_dev[i * self.eval_config.batch_size:(i + 1) * self.eval_config.batch_size])

                            losses += loss
                            accuracys += accuracy

                        print
                        'accuracy = ' + str(accuracys / num)
                        print
                        'loss = ' + str(losses / num)
                        p = self.saver.save(self.sess, self.model_path, global_step=current_step)
                        print
                        p

    def get_embedding(self, text):

        blank = self.word2id['BLANK']
        content = [blank for j in range(500)]
        for j in xrange(len(text)):
            if (j == 500):
                break
            if not text[j] in self.word2id:
                content[j] = self.word2id['UNK']
            else:
                content[j] = self.word2id[text[j]]
        feed_dict = {
            self.mout.input_x: [content],
            self.mout.keep_prob: 1.0
        }
        output = self.sess.run([self.mout.output], feed_dict=feed_dict)
        ret = []
        for k in output[0]:
            for j in k:
                ret.append(j)
        return ret

    def get_similarity(self, embedding1, embedding2):
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        if len(embedding1) != len(embedding2):
            print
            "dimension unmatched"
            return 0
        result = 0.0
        l1 = 0.0
        l2 = 0.0
        for i in range(len(embedding1)):
            result += embedding1[i] * embedding2[i]
            l1 += embedding1[i] * embedding1[i]
            l2 += embedding2[i] * embedding2[i]
        if (l1 == 0 or l2 == 0):
            return 0.0
        return result / pow(l1, 0.5) / pow(l2, 0.5)

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
    a = cnn_model(save_path='./model')
    a.Load()
    # a.Train(path = '')
    a.get_embedding(text='我 爱 北京 天安门')
