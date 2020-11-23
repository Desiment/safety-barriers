import pandas as pd
from sklearn.cluster import KMeans
from joblib import dump
import csv

data = pd.read_csv('../data/text_clustered_features.csv', delimiter=',', index_col=0)
vectors = data[[str(i) for i in range(500)]].to_numpy()

cluster_number = 15
epochs = 20
model = KMeans(n_clusters=cluster_number, max_iter=epochs, n_jobs=4)
model.fit(vectors)

dump(model, '../data/simple_kmeans.joblib')

clusters = model.labels_
data['cluster'] = pd.DataFrame(clusters)

data.to_csv('../data/text_clustered.csv', index=True, quoting=csv.QUOTE_ALL)