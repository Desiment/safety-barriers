from nltk.corpus import stopwords
import pandas as pd
import csv
import re

stop_words_data = pd.read_csv('data/stopwords', delimiter=',')
stop_words = set(stop_words_data['words'])

data = pd.read_csv('data/fixed_precedents.csv', delimiter=',', quotechar='\"')

text_data = (data['subsidiary'] + ' '
             + data['contractor'].str.replace('не привлекался', '') + ' '
             + data['worktype'].str.replace('не определена', '') + ' '
             + data['place'] + ' '
             + ' ' + data['description']).str.strip()

text_data = pd.DataFrame(text_data)
text_data = text_data.rename(columns={0: 'text'})

pattern = re.compile('[^А-яЁё_]+', re.UNICODE)
text_data['text'] = text_data['text'].map(lambda s: ' '.join(
    list(filter(lambda s: s not in stop_words and len(s.strip()) > 0,
                [pattern.sub('', w) for w in str(s).strip().split(' ')]))))

# print(text_data)
text_data.to_csv('data/documents.csv', index=True, quoting=csv.QUOTE_ALL)