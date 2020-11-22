from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
import csv
import re
import pymorphy2


#Constants:
RAW_DATA_PATH = "./data/precedents.csv"
SEP_DATA_PATH = "./data/fixed_precedents.csv"
MERGED_DATA_PATH = "./data/documents.csv"
FREQUENCY_DICTIONARY = "./data/frequency.dic"

STOPWORDS_PATH = "data/stopwords.txt"
BAD_BLOCK_BEG = 62000
BAD_BLOCK_END = 82000


def data_seperate(output_path = SEP_DATA_PATH):
    
    raw_data = pd.read_csv(RAW_DATA_PATH, sep=",")
    raw_data["place"] = raw_data["place"].map(lambda x: str(x).replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\"', '').replace('\'', '').lower())
    
    data_bottom, data_top = raw_data[:BAD_BLOCK_BEG], raw_data[:BAD_BLOCK_END]
    raw_data = pd.concat([data_bottom, data_top])
    raw_data = raw_data.drop_duplicates(keep='first', inplace=False )
    raw_data = raw_data[~raw_data.place.str.contains("nan")]

    new = raw_data["place"].str.split(",", n=3, expand=True)
    new[0] = new[0].str.lstrip('(')
    new[3] = new[3].str.rstrip(')')
    new[0] = new[0].str.strip()
    new[1] = new[1].str.strip()
    new[2] = new[2].str.strip()
    new[3] = new[3].str.strip()
    new[4] = raw_data["precedent"].map(lambda x: str(x).lower().replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\n', ''))

    new = new.rename(columns={
        0: 'subsidiary',
        1: 'contractor',
        2: 'worktype',
        3: 'place',
        4: 'description'})
    
    new.to_csv(output_path, index=True, quoting=csv.QUOTE_ALL)


def data_merge(input_path = SEP_DATA_PATH, output_path = MERGED_DATA_PATH):
    stop_words_data = pd.read_csv(STOPWORDS_PATH, delimiter=',')
    stop_words = set(stop_words_data['words'])

    data = pd.read_csv(input_path, delimiter=',', quotechar='\"')

    text_data = (data['subsidiary'] + ' '
                + data['contractor'].str.replace('не привлекался', '') + ' '
                + data['worktype'].str.replace('не определена', '') + ' '
                + data['place'] + ' '
                + ' ' + data['description']).str.strip()

    text_data = pd.DataFrame(text_data)
    text_data = text_data.rename(columns={0: 'text'})

    morph = pymorphy2.MorphAnalyzer()

    pattern = re.compile('[^А-яЁё_]+', re.UNICODE)
    text_data['text'] = text_data['text'].map(lambda s: ' '.join(map(lambda s: morph.parse(s)[0].normal_form,
        list(filter(lambda s: s not in stop_words and len(s.strip()) > 0,
                    [pattern.sub('', w) for w in str(s).strip().split(' ')])))))

    # print(text_data)
    text_data.to_csv(output_path, index=True, quoting=csv.QUOTE_ALL)


def build_dictonary(input_path = SEP_DATA_PATH, output_path = FREQUENCY_DICTIONARY):

    stop_words_data = pd.read_csv(STOPWORDS_PATH, delimiter=',')
    stop_words = set(stop_words_data['words'])
    
    data = pd.read_csv(input_path, delimiter=',')
    morph = pymorphy2.MorphAnalyzer()

    pattern = re.compile('[^А-яЁё_]+', re.UNICODE)
    data['description'] = data['description'].map(lambda s: ' '.join(map(lambda s: morph.parse(s)[0].normal_form,
        list(filter(lambda s: s not in stop_words and len(s.strip()) > 0,
                    [pattern.sub('', w) for w in str(s).strip().split(' ')])))))
        
    for msg in data['description']:
        for word in str(msg).split(' '):
            with open(output_path, 'a') as dictionary_freq:
                dictionary_freq.write(str(word) + "\n")
