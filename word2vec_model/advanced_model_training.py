from simple_elmo import ElmoModel
import pandas as pd
from sklearn.cluster import KMeans
import csv

from joblib import dump

data = pd.read_csv('../data/documents_advanced_vectors.csv', delimiter=',', index_col=0)
vectors = data[[str(i) for i in range(1024)]].to_numpy()

cluster_number = 15
epochs = 20
model = KMeans(n_clusters=cluster_number, max_iter=epochs, n_jobs=4)
model.fit(vectors)

dump(model, '../data/advanced_kmeans.joblib')

clusters = model.labels_

# Just cluster
data['cluster'] = pd.DataFrame(clusters)
data.to_csv('../data/text_clustered_advanced_features.csv', index=True, quoting=csv.QUOTE_ALL)

data = data[['text', 'cluster']]
data.to_csv('../data/text_clustered_advanced.csv', index=True, quoting=csv.QUOTE_ALL)