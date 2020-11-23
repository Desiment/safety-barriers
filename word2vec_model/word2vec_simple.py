import pandas as pd
from gensim.models.word2vec import Word2Vec

data = pd.read_csv('../data/documents_advanced.csv', delimiter=',')
model = Word2Vec(
    min_count=3,
    window=5,
    size=100,
    sample=6e-5,
    alpha=0.03,
    min_alpha=0.0001,
    negative=10,
    workers=4)

sentences = [str(sen).split() for sen in data['text'].tolist()]
model.build_vocab(sentences, progress_per=10000)

model.train(sentences, total_examples=model.corpus_count, epochs=30)
model.save('../data/word2vec_simple.model')
