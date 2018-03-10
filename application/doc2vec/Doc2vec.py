#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lda_model import *
from .wordembedding_model import *
from .tfidf_model import *
from .lawlstm import *
from .lawcnn import *
from application.util import print_time
from application import app

import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from ctypes import cdll, c_char, c_char_p, cast, POINTER
import os.path
import json
import os


def lac_init(model_path='', user_dict_path='', pre_alloc_size=1024 * 1024 * 16, t2s=False, just_seg=True):
    _lib = None
    if _lib == None:
        # path = os.path.dirname(os.path.realpath(__file__)) #设置so文件的位�?
        _lib = cdll.LoadLibrary(model_path + '/libthulac.so')  # 读取so文件
        # if len(model_path) == 0:
        # model_path = path+'/models' #获取models文件夹位�?
        model_path = model_path + '/models'
    _lib.init(c_char_p(model_path), c_char_p(user_dict_path), pre_alloc_size, int(t2s), int(just_seg))  # 调用接口进行初始�?
    return _lib


def lac_clear(lib):
    if lib != None: lib.deinit()


def seg(data, lib):
    assert lib != None
    r = lib.seg(c_char_p(data))
    assert r > 0
    lib.getResult.restype = POINTER(c_char)
    p = lib.getResult()
    s = cast(p, c_char_p)
    d = '%s' % s.value
    lib.freeResult();
    return d.split(' ')


class Doc2vec(object):
    def __init__(self, save_path):
        if not(app.config["LOAD_MODEL"]):
            return
        print("Loading model")
        print_time()

        self.lac_lib = lac_init(model_path=save_path + '/thulac', user_dict_path=save_path + '/thulac/user.txt')

        self.stop_words = {}
        fs = open(save_path + '/stop_words_zh.txt', 'r')
        fs_lines = fs.readlines()
        for fs_line in fs_lines:
            self.stop_words[unicode(fs_line.strip(), 'utf-8')] = 1
        fs.close()

        #self.lda_m = lda_model(save_path + '/ldamodel')
        #self.lda_m.load()
        self.tfidf_m = tfidf_model(save_path + '/dic', save_path + '/tfidf')
        self.wordembedding_m = wordembedding_model(save_path + '/words.vec')
        #self.lstm = lstm_model(save_path)
        #self.cnn = cnn_model(save_path)

        print("Load done")
        print_time()

    def get_embedding(self, text, mode=0):

        text = seg(text, self.lac_lib)
        temp = []
        for w in text:
            if w not in self.stop_words:
                temp.append(w)
        text = temp
        if mode == 0:
            return self.lda_m.get_embedding(text)
        if mode == 1:
            return self.tfidf_m.get_embedding(text)
        if mode == 2:
            return self.wordembedding_m.get_embedding(text)
        if mode == 3:
            return self.lstm.get_embedding(text)
        if mode == 4:
            return self.cnn.get_embedding(text)
        if mode == 5:
            vec0 = self.lda_m.get_embedding(text)
            vec2 = self.wordembedding_m.get_embedding(text)
            return vec0.extend(vec2)
        if mode == 6:
            vec = []
            vec0 = self.lda_m.get_embedding(text)
            vec1 = self.tfidf_m.get_embedding(text)
            vec2 = self.wordembedding_m.get_embedding(text)
            vec.append(vec0)
            vec.append(vec1)
            vec.append(vec2)
            return vec
        print("wrong mode")
        return False

    def get_similarity(self, embedding1, embedding2, mode=0, rate=[1.0 / 3 for i in range(3)]):

        if mode == 0:
            return self.lda_m.get_similarity(embedding1, embedding2)
        if mode == 1:
            return self.tfidf_m.get_similarity(embedding1, embedding2)
        if mode == 2:
            return self.wordembedding_m.get_similarity(embedding1, embedding2)
        if mode == 3:
            return self.lstm.get_similarity(embedding1, embedding2)
        if mode == 4:
            return self.cnn.get_similarity(embedding1, embedding2)
        if mode == 5:
            return self.wordembedding_m.get_similarity(embedding1, embedding2)
        if mode == 6:
            result = 0.0
            result += rate[0] * self.lda_m.get_similarity(embedding1[0], embedding2[0])
            result += rate[1] * self.tfidf_m.get_similarity(embedding1[1], embedding2[1])
            result += rate[2] * self.wordembedding_m.get_similarity(embedding1[2], embedding2[2])
        print("wrong mode")
        return False
