import csv

import nltk
import pandas as pd
from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
import math
import numpy as np
from sklearn import cluster

words = pd.read_csv('../data/word_clusters.csv', delimiter=',', index_col=0)
model = Word2Vec.load('../data/word2vec_advanced.model')

clusters = words['cluster'].max() + 1
clusters_mean = []
for cluster_index in range(clusters):
    clusters_mean.append([])
    for word in words[words['cluster'] == cluster_index]['word']:
        clusters_mean[cluster_index].append(model.wv[str(word)])
    clusters_mean[cluster_index] = np.mean(clusters_mean[cluster_index], axis=0)

word_clusters = dict()
for i, row in words.iterrows():
    word_clusters[row['word']] = row['cluster']

weights = []
weights_dict = {}
for i, word in enumerate(words['word'].tolist()):
    weights.append(math.exp(-1 * np.std(clusters_mean[word_clusters[word]] - model.wv[word])))
    weights_dict[word] = weights[i]
words['weights'] = weights

texts = pd.read_csv('../data/documents.csv', delimiter=',', index_col=0)
text_features = np.zeros((clusters, len(texts.index)))

for i, row in texts.iterrows():
    if str(row['text']) != 'nan':
        for word in row['text'].split(' '):
            if word in weights_dict.keys():
                text_features[word_clusters[word]][i] += weights_dict[word]

for cluster_id in range(clusters):
    texts[cluster_id] = pd.DataFrame(text_features[cluster_id])

cluster_number = 25
epochs = 20
data = text_features.T[...]
assigned_clusters = cluster.KMeans(n_clusters=cluster_number, max_iter=epochs, n_jobs=4).fit(data).labels_

texts['cluster'] = assigned_clusters

words.to_csv('../data/weighted_words.csv', index=True, quoting=csv.QUOTE_ALL)
texts.to_csv('../data/texts_clustered.csv', index=True, quoting=csv.QUOTE_ALL)