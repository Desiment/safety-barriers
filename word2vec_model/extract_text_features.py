import pandas as pd
import csv
texts = pd.read_csv('../data/texts_clustered.csv', delimiter=',')
texts_nof = pd.DataFrame(texts['text'])
texts_nof['cluster'] = texts['cluster']

texts_nof.to_csv('../data/texts_clustered_nof.csv', index=True, quoting=csv.QUOTE_ALL)