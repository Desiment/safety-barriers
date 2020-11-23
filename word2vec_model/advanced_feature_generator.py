import csv

import pandas as pd
from simple_elmo import ElmoModel

batch_size = 32

model = ElmoModel()
model.load('../data/195.zip', max_batch_size=batch_size)

data = pd.read_csv('../data/documents_advanced.csv', delimiter=',', index_col=0)
messages = data['text'].tolist()

with open('../data/documents_advanced_vectors.csv', 'w') as out:
    csvwriter = csv.writer(out, delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)
    res = ['', 'text'] + [str(i) for i in range(0, 1024)]
    csvwriter.writerow(res)

    i = 0
    while i < len(messages):
        nxt = min(len(messages), i + batch_size)

        batch = messages[i:nxt]
        sentences = [s.split(' ') for s in batch]
        vectors = model.get_elmo_vector_average(sentences)

        for j, vector in enumerate(vectors):
            res = [str(i+j), batch[j]] + [str(val) for val in vector]
            csvwriter.writerow(res)

        i = nxt


