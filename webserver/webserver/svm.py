#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pickle
import os
import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.preprocessing import scale
from gensim.models.word2vec import Word2Vec
from sklearn.metrics import matthews_corrcoef,accuracy_score
import jieba.posseg as posseg
import gensim

class SVM_Model:
    def __init__(self):
        self.dim = 150
        self.model,self.svm = self.load()

    def cleanText(self,corpus):
        corpus = [z.replace('\n','').split() for z in corpus]
        return corpus

    def buildWordVector(self,text, size):
        vec = np.zeros(size).reshape((1, size))
        count = 0.
        for word in text:
            try:
                word = unicode(word)
                # vec += imdb_w2v[word].reshape((1, size))
                vec += self.model[word].reshape((1, size))
                count += 1.
            except KeyError:
                continue
        if count != 0:
            vec /= count
        return vec

    def cleanText_1(self,corpus):
        corpus = [z.replace('\n','') for z in corpus]
        return corpus

    def line_posseg(self,line):
        line = line.strip()
        new_line = ""
        word_w = posseg.cut(line)
        for item in word_w:
            word = item.word
            flag = item.flag
            new_line += word + "_" + flag + " "
        return new_line

    def predict(self,contents = ["太差了太差了太差了","太差了太差了太差了","太差了太差了太差了","太差了太差了太差了"]):
        # with open('test','r') as infile:
        s = [self.line_posseg(line) for line in contents]
        s = self.cleanText(s)
        s_test = np.concatenate([self.buildWordVector(z, self.dim) for z in s])
        s_vector = scale(s_test)
        value = self.svm.predict(s_vector)
        return value

    def predict_from_text(self,path):
        with open(path, "r") as f:
            s = f.readlines()
            s = [self.line_posseg(line) for line in s]
            s = self.cleanText(s)
            s_test = np.concatenate([self.buildWordVector(z, self.dim) for z in s])
            s_vector = scale(s_test)
            value = self.svm.predict(s_vector)
            return value

    def load(self):
        #导入词向量
        # model = Word2Vec.load_word2vec_format('/home/d/Desktop/LP/Vector/gupiao.vector', binary= False)
        # model = Word2Vec.load_word2vec_format('./conf/gupiao.vector', binary= False)
        model = gensim.models.KeyedVectors.load_word2vec_format('/home/demon/PycharmProjects/webserver/webserver/conf/gupiao.vector', binary= False)
        f= open("/home/demon/PycharmProjects/webserver/webserver/conf/gupiao.model",'r')
        clf = pickle.load(f)
        f.close()
        return model, clf

if __name__ == "__main__":
    model = SVM_Model()
    # model.predict(contents=["董明珠吹牛已无上限狡辩抵赖天下天下少有","我认为银隆是大骗子","脑残董粉","银隆犬一边去！","能在顺风赚钱"])
    # print(model.predict_from_text("./gupiao.txt"))

