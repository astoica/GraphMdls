## simulate data for the sLDA that mimics a 20%-size of the original Data-2 in the following way:
## - simulate genders randomly in equal proportion
## - choose two relatively neutral topics from supervised lda (run supervised-lda-final.r to see them)
## - sample raw documents based on these topics, adding a modicum of noise
## Author: Ana-Andreea Stoica
## Date: December 16, 2018

import csv 
import numpy as np 

# simulate genders
f= open('gender_simulated_testdata.csv', 'w')
writer= csv.writer(f, lineterminator="\n")

num_docs = 184
# simulate random genders in equal proportion, of length equal to the test data length, 184 documents
a = np.random.choice([-1, 1], size=(num_docs,), p=[1./2, 1./2])
b = list(a)

for i in b: 
    writer.writerow([i])

f.close()

# simulate raw documents data 
f = open('topics20_1000_docs_slda.csv', 'r')
reader = csv.reader(f)

topics = [] 
vocab = []
for row in reader: 
    topics.append(row)
    for i in row:
        vocab.append(i)

# choose the topics we want to simulate on 
fem_topics = topics[6]
#fem_topics =topics[8]
mal_topics = topics[10]
#mal_topics = topics[3]

ff = open('test_docs_slda_20topics.csv', 'w')
#ff = open('test_docs_slda_20topics_moregendered.csv', 'w')  
writer= csv.writer(ff, lineterminator="\n")

# since we have randomized gender, we may choose the first half of people to talk about one of the topics and the second half to talk about the other topic without reducing the randomness of what gender talks about which of the topics; we choose 90 words related to their topics and 10 random words from any of the topics to add a bit of noise
for i in range(int(num_docs/2)):
    words = [] 
    idx_topic = np.random.choice(range(15), size=(90,), p=[1./15]*15)
    idx_general = np.random.choice(range(len(vocab)), size=(10,), p=[1./len(vocab)]*len(vocab))

    for j in idx_topic:
        words.append(fem_topics[j])    

    for j in idx_general:
        words.append(vocab[j])

    writer.writerow(words)

for i in range(int(num_docs/2)):
    words = []
    idx_topic = np.random.choice(range(15), size=(90,), p=[1./15]*15)
    idx_general = np.random.choice(range(len(vocab)), size=(10,), p=[1./len(vocab)]*len(vocab))

    for j in idx_topic:
        words.append(mal_topics[j])

    for j in idx_general:
        words.append(vocab[j])

    writer.writerow(words)

f.close()
ff.close()
