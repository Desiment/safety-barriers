import pandas as pd
from gensim.models.word2vec import Word2Vec

model = Word2Vec.load('../data/word2vec_simple.model')

# sentences = []
# epochs = 30
# total_number = 1
#
# model.train(sentences=sentences, total_examples=total_number, epochs=epochs)

model.save('../data/word2vec_advanced.model')
