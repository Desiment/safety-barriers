import pandas as pd
import numpy as np


spec_symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.', ',', '№', '\\', '/', '(', ')', '\"']
def reduct(word):
    for sym in spec_symbols:
        word = word.replace(sym, ' ')
    return word

data = pd.read_csv("data.csv")
for msg in data['description']:
    msg_splay = str(msg).split(' ')
    for word in msg_splay:
        with open('dictonary.dic', 'a') as corpus_out:
            corpus_out.write(reduct(str(word)) + "\n")
