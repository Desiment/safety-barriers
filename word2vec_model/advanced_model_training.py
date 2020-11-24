import csv

import pandas as pd
from joblib import dump
from nltk.cluster import GAAClusterer
from nltk.cluster import KMeansClusterer
from nltk.cluster import cosine_distance
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import OPTICS
from sklearn.cluster import SpectralClustering

data = pd.read_csv('../data/documents_advanced_vectors.csv', delimiter=',', index_col=0)
vectors = data[[str(i) for i in range(1024)]].to_numpy()

cluster_number = 15
epochs = 30

#nltk kmeans
model = KMeansClusterer(cluster_number, distance=cosine_distance, repeats=epochs)
clusters = model.cluster(vectors, assign_clusters=True)

dump(model, '../data/advanced_nltk_kmeans.joblib')

# Just cluster
data['cluster'] = pd.DataFrame(clusters)
data[['text', 'cluster']].to_csv('../data/text_clustered_nltk_kmeans.csv', index=True, quoting=csv.QUOTE_ALL)

#nltk GAAClusterer
model = GAAClusterer(num_clusters=cluster_number)
model.cluster(vectors, assign_clusters=True)

clusters = [model.classify_vectorspace(vector.tolist()) for vector in vectors]

data['cluster'] = pd.DataFrame(clusters)
data[['text', 'cluster']].to_csv('../data/text_clustered_nltk_gaac.csv', index=True, quoting=csv.QUOTE_ALL)

#sklearn means
model = KMeans(n_clusters=cluster_number, max_iter=epochs, n_jobs=8)
model.fit(vectors)
dump(model, '../data/advanced_sklearn_kmeans.joblib')

data['cluster'] = pd.DataFrame(model.labels_)
data[['text', 'cluster']].to_csv('../data/text_clustered_sklearn_kmeans.csv', index=True, quoting=csv.QUOTE_ALL)

#sklearn agglomerative
model = AgglomerativeClustering(n_clusters=cluster_number)
clusters = model.fit_predict(vectors)
data['cluster'] = pd.DataFrame(clusters)
data[['text', 'cluster']].to_csv('../data/text_clustered_sklearn_agglomerative.csv', index=True, quoting=csv.QUOTE_ALL)

#sklearn Spectral
model = SpectralClustering(n_clusters=cluster_number, n_jobs=8)
clusters = model.fit_predict(vectors)
data['cluster'] = pd.DataFrame(clusters)
data[['text', 'cluster']].to_csv('../data/text_clustered_sklearn_spectral.csv', index=True, quoting=csv.QUOTE_ALL)

#sklearn optics
model = OPTICS(min_cluster_size=cluster_number, n_jobs=8)
clusters = model.fit_predict(vectors)
data['cluster'] = pd.DataFrame(clusters)
data[['text', 'cluster']].to_csv('../data/text_clustered_sklearn_optics.csv', index=True, quoting=csv.QUOTE_ALL)


