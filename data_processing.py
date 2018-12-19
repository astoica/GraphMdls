## this code was used to transport data from psql into csv files, it is not needed for running experiments after data was retrieved
## Author: Ana-Andreea Stoica
## Data: December 10, 2018

from gensim import corpora, models, similarities
import pandas as pd
import psycopg2
import csv 
from collections import defaultdict

conn = psycopg2.connect("host=localhost dbname=chris user=ana password=wham5!wallet")
cur = conn.cursor()

# this is the dictionary of hashtags
d= {}
# this is the document collection: each user is a document with the set of values as the hashtags they use
dx = defaultdict(list)
# list of hashtags with less than 1000 occurences
l = []
# select the tags from 1000 random users
cur.execute("select ig_user_id, tag from tags_10000")
conn.commit()

res = cur.fetchall()
#for i in range(len(res)):
#    if (res[i][1] in d.keys()):
#        d[res[i][1]] += 1
#    else:
#        d[res[i][1]] = 1

# only retain the hashtags with at least 10 occurences
#for k in d.copy():
#    if (d[k] < 10):
#        l.append(k)
#        d.pop(k)

#f = open('dictionary100_hashtags_counts.csv', 'w')
#ff = open('dictionary100_hashtags.csv', 'w')
f = open('documents10000-ids.csv', 'w')
fx= open('documents10000.csv', 'w')
#writer=csv.writer(f, lineterminator="\n")
#writer2 = csv.writer(ff, lineterminator="\n")
writer= csv.writer(f, lineterminator="\n")
writerx = csv.writer(fx, lineterminator="\n")

#for k,v in d.items():
#    writer.writerow([k,v])

#for k in d.keys():
#    writer2.writerow([k])

#filter out the words that appear under 10 times or so 
#for a,b in res:
#    if b not in l:
#        dx[a].append(b)

# don't filter out any words
for a,b in res:
    dx[a].append(b)

#for x,y in dx.items():
#    dx[a] = list(set(dx[a]) - set(l))

for j in dx.keys():
    writer.writerow([j])
    writerx.writerow(dx[j])

f.close()
#ff.close()
fx.close()
