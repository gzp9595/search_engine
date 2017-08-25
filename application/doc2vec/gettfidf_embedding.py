from Doc2vec import *
m = Doc2vec(save_path='./model')
for i in range(4,30):
	fin = open('/mnt/data/out_content_d/'+str(i),'r')
	fout = open('/mnt/data/tfidf_embedding/' + str(i),'w')
	num = 0
	print str(i)+'/30'
	while True:
		content = fin.readline()
		if not content:
			break
		content = content.strip().split('\t')
		if len(content) != 2:
			continue
		text = content[1].strip(' ').split(' ')
		id = content[0]
		vec  = m.get_embedding(text, 1)
		towrite = content[0]+'\t'
		for v in vec:
			towrite = towrite + " " + str(v)+':'+str(vec[v])
		towrite = towrite.strip(" ") + '\n'
		fout.write(towrite)
		num += 1
		if num % 10000 == 0:
			print num
	fin.close()
	fout.close()
