from joblib import load
import pandas as pd
from simple_elmo import ElmoModel
import csv

test = pd.read_csv('../data/test.csv', delimiter=',', index_col=0)

elmo = ElmoModel()
elmo.load('../data/195.zip')


vectors = elmo.get_elmo_vector_average([test['text'].tolist()])

model = load('../data/advanced_kmeans.joblib')
clusters = model.predict(vectors)

test['cluster'] = pd.DataFrame(clusters)
test.to_csv('../data/test.csv', index=True, quoting=csv.QUOTE_ALL)

