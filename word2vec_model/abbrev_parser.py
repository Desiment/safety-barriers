from bs4 import BeautifulSoup
import requests as req
import csv
import pandas as pd
import re
import pymorphy2

pattern = re.compile('[^А-яЁё_]+', re.UNICODE)
pattern2 = re.compile('[^A-zА-яЁё_]+', re.UNICODE)
morph = pymorphy2.MorphAnalyzer()

res = []
with open("../data/abbrevs", 'r') as file:
    for line in file.readlines():
        if len(line.strip()) > 0:
            strs = [str.strip() for str in line.lower().rstrip('>>>').strip().split('-')]
            strs[1] = ' '.join(map( lambda s: morph.parse(s)[0].normal_form, list(filter(lambda s: len(s.strip()) > 0, [pattern.sub('', w) for w in strs[1].strip().split(' ')]))))
            strs[0] = ' '.join(map( lambda s: morph.parse(s)[0].normal_form, list(filter(lambda s: len(s.strip()) > 0, [pattern2.sub('', w) for w in strs[0].strip().split(' ')]))))
            if len(strs) == 2 and len(strs[1]) > 0 and len(strs[0]) > 0:
                res.append(strs)

data = pd.DataFrame(res)
data = data.rename(columns={
    0: "abbr",
    1: "desc"
})
data.to_csv('../data/abbrevs.csv', index=True, quoting=csv.QUOTE_ALL)
