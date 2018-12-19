## This code implments unsupervised lda on raw document texts that contain hashtags from Instagram using gensim
## Author: Ana-Andreea Stoica
## Date: December 12, 2018

from gensim import corpora, models, similarities
import csv 
from pprint import pprint
import psycopg2
import numpy as np 
from collections import defaultdict

# create a dictionary of users-> gender for the total of 92k users
fgender = open('users_all_reduced.csv', 'r')
readerg = csv.reader(fgender)
d = {}
for row in readerg:
    d[row[0]] = row[10]

# create a dictionary of users -> hashtags they use
dd = defaultdict(list)
fh = open('tags_1000.csv', 'r')
readerh = csv.reader(fh)
header = next(readerh)
for row in readerh:
    dd[row[2]].append(row[3])

# set the number of topics - this should be validated
num_topics = 10 

# parse the documents into a gensim dictionary and a corpus
#f = open('test-documents.csv', 'r')
f = open("documents1000.csv", 'r')
reader = csv.reader(f)
docs = []
for row in reader:
    docs.append(row)

dict = corpora.Dictionary(docs)
corps = [dict.doc2bow(text) for text in docs]

# run lda on the dictionary and corpus
# we find that 10 topics for 91 users are doing well 
lda = models.ldamodel.LdaModel(corpus = corps, id2word=dict, num_topics = num_topics, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

pprint(lda.show_topics())

#perplexity score, is pretty good 
lda.log_perplexity(corps)

# write the topics all of users 
# this needs to be re-written with a csv file of the tags 
#conn = psycopg2.connect("host=localhost dbname=chris user=ana password=wham5!wallet")
#cur = conn.cursor()

#ff = open('test-document-ids.csv', 'r')
ff = open('documents1000-ids.csv', 'r')
readerf = csv.reader(ff)
ppl = [] 
for row in readerf:
    ppl.append(row)

fx = open('users_and_topics1000.csv', 'w')
writer= csv.writer(fx, lineterminator="\n")
ffx = open('users_and_topics1000_matrixform.csv', 'w')
writerx = csv.writer(ffx, lineterminator="\n")
headerx = ['ig_user_id', 'gender', 'topic_1', 'topic_2', 'topic_3', 'topic_4','topic_5','topic_6','topic_7','topic_8','topic_9','topic_10']
writerx.writerow(headerx)
#matrix = [] 

for a in ppl:
    xx = [] 
    xx.append(a[0])
    #cur.execute("SELECT tag FROM tags WHERE ig_user_id = %s", a)
    #user_tags = [tag[0] for tag in cur.fetchall()]
    user_tags = dd[a]
    user_bow = dict.doc2bow(user_tags)
    lda_user = lda[user_bow]
    top = sorted(lda_user[0], key=lambda x: x[1], reverse=True)
    for i in top:
        xx.append(i)
    writer.writerow(xx)
    aa = np.zeros(num_topics)
    ind = [b[0] for b in xx[1:]]
    ind2 = [b[1] for b in xx[1:]]
    aa[ind] = ind2
    #matrix.append([aa])
    #np.savetext("users_and_topics100_matrixform.csv", matrix, delimiter=',')
    aa = [str(i) for i in aa]
    aa = [a[0]] + [d[a[0]]] + aa
    writerx.writerow(aa)

fx.close()
ffx.close()
