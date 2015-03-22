#encoding=utf-8
import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC




def load_train_data():
	infile = open('Positive_text.txt','r')
	data1 = infile.readlines()
	infile.close()

	infile = open('Negative_text.txt','r')
	data2 = infile.readlines()
	infile.close()
	return data1,data2

def load_test_data():
	infile = open('test_selected_text.txt','r')
	#infile = open('Positive_part.txt','r')
	data = infile.readlines()
	infile.close()
	return data

def load_time_data():
	result = []
	infile = open('test_selected_time.txt','r')
	data = infile.readlines()
	for d in data:
		result.append(d.strip('\r\n'))
	infile.close()
	return result

if __name__ == '__main__':
	#lines = get_data('Negative.txt')
	#data_partition(lines)
	test_time = load_time_data()
	data1,data2 = load_train_data()
	data = data1+data2
	target = [1]*len(data1)+[2]*len(data2)
	target = np.array(target)
	
	count_vect = CountVectorizer()
	count_vect.fit(data)
	X_train_counts = count_vect.transform(data)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	#print target
	
	test_data = load_test_data()
	X_test_counts = count_vect.transform(test_data)
	X_test_tfidf = tfidf_transformer.transform(X_test_counts)
	#print X_test_counts

	clf = MultinomialNB().fit(X_train_tfidf,target)
	#clf = SVC()
	#clf.fit(X_train_tfidf,target)
	#predicted = clf.predict(X_test_tfidf)
	predicted = clf.predict_proba(X_test_tfidf)
	#predicted = clf.predict(X_test_tfidf)
	ofile = open('test_selected_result.txt','w')
	i = 1
	for p,t in zip(predicted,test_time):
		if max(p[0],p[1])>0.65:
			if(p[0]>=p[1]):
				tmp = '1'
			else:
				tmp = '2'
			ofile.write(t+' '+str(p[0])+' '+str(p[1])+' '+tmp+'\r\n')
		else:
			ofile.write(t+' '+'0'+' '+'0'+' '+'0'+'\r\n')
		i+=1
	#

	
	