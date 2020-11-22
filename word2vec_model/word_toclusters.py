import csv

import nltk
import pandas as pd
from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
from sklearn import cluster

model = Word2Vec.load('../data/word2vec_advanced.model')
data = model[model.wv.vocab]

cluster_number = 500
epochs = 30
assigned_clusters = cluster.KMeans(n_clusters=cluster_number, max_iter=epochs, n_jobs=4).fit(data).labels_

words = list(model.wv.vocab)
clusters = []
for i, word in enumerate(words):
    clusters.append([word, assigned_clusters[i]])

clusters = pd.DataFrame(clusters)
clusters = clusters.rename(columns={
    0: 'word',
    1: 'cluster'
})
clusters.to_csv('../data/word_clusters.csv', index=True, quoting=csv.QUOTE_ALL)
