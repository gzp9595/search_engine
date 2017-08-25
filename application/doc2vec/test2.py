#coding=utf-8
from Doc2vec import *
m = Doc2vec(save_path='./model')
print 'init'
count = 0
f = open('/data/disk1/private/lixiang/out_content_100w.txt','r')
while True:
    l = f.readline()
    if not l:
        break
    l = l.strip().split(' ')
    vec = m.get_embedding(l,1)
    count += 1
    if count % 10000 == 0:
        print count
