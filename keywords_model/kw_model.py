from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
import csv
import re
import pymorphy2
import statistics

STOPWORDS_PATH = "../data/stopwords.txt"
CLUSTER_PATH = "clusters.csv"

def fstmin(numbers):
    mn = float('+inf')
    pos = -1
    for i in range(0, len(numbers)):
        if numbers[i] < mn:
            mn = numbers[i]
            pos = i
    return mn, i

def fstmax(numbers):
    mx = float('-inf')
    pos = -1
    for i in range(0, len(numbers)):
        if numbers[i] > mx:
            mx = numbers[i]
            pos = i
    return mx, i

def secmax(numbers):
    mx = smx = float('-inf')
    pos = -1
    for i in range(0, len(numbers)):
        if numbers[i] > smx:
            if numbers[i] >= mx:
                mx, smx = numbers[i], mx            
            else:
                smx = numbers[i]
                pos = i
    return smx, i


def clear_msg(message):
    message = str(message).replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\"', '').replace('\'', '').lower()
    
    stop_words_data = pd.read_csv(STOPWORDS_PATH, delimiter=',')
    stop_words = set(stop_words_data['words'])
    
    morph = pymorphy2.MorphAnalyzer()

    pattern = re.compile('[^А-яЁё_]+', re.UNICODE)
    message = list(map(lambda s: morph.parse(s)[0].normal_form, [pattern.sub('', wrd) for wrd in message.split(' ') if (wrd not in stop_words and len(wrd.strip()) > 0)]))
    return message

def procs_msg(message):
    message = clear_msg(message)
    classificator = pd.read_csv(CLUSTER_PATH, delimiter=',')
    
    values = []
    row = 0
    for index, cluster in classificator.iterrows():
        values.append(0)
        for key_val in str(cluster[1]).split(' '):    
            values[index] += message.count(str(key_val))
    
    mn, indn  = fstmin(values.copy())
    mx, indx  = fstmax(values.copy())
    smx, inds = secmax(values.copy())
    
    
    cluster_row = -3
    if (mx - mn < 2):
        cluster_row = -1
    else:
        for i in range(0, len(values)):
            values[i] = (values[i] - mn) / (mx - mn)
        
        if statistics.median(values) >= 0.7:
            cluster_row = -1
        else:
            if (mx - smx > 1):
                cluster_row = indx
            else:
                cluster_row = -2
    
    if cluster_row = -1:
        return ("Другое", "")
    else if cluster_row = -2:
        return (to_str(classifictor["names"][indx]), to_str(classifictor["names"][inds])) 
    else:
        return (to_str(classifictor["names"][cluster_row]), "") 


procs_msg("лед, ветер, вода, труба, автомобиль")
    
