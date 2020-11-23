import csv
import math
import numpy as np
import pandas as pd
from joblib import load
from gensim.models import Word2Vec


test = pd.read_csv('../data/test.csv', delimiter=',', index_col=0)
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

test_features = np.zeros((len(test.index), clusters))

for i, row in test.iterrows():
    if str(row['text']) != 'nan':
        for word in row['text'].split(' '):
            if word in weights_dict.keys():
                test_features[i][word_clusters[word]] += weights_dict[word]

model = load('../data/simple_kmeans.joblib')
clusters = model.predict(test_features)

test['cluster'] = pd.DataFrame(clusters)
test.to_csv('../data/test.csv', index=True, quoting=csv.QUOTE_ALL)

