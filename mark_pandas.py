import pandas as pd
import csv

data = pd.read_csv("precedents.csv", sep=",")
data["place"] = data["place"].map(lambda x: str(x).replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\"', '').replace('\'', '').lower())

data_bottom = data[:62000]
data_top = data[82000:]
data = pd.concat([data_bottom, data_top])

data = data.drop_duplicates(keep='first', inplace=False )

data = data[~data.place.str.contains("nan")]

new = data["place"].str.split(",", n=3, expand=True)
new[0] = new[0].str.lstrip('(')
new[3] = new[3].str.rstrip(')')
new[0] = new[0].str.strip()
new[1] = new[1].str.strip()
new[2] = new[2].str.strip()
new[3] = new[3].str.strip()
new[4] = data["precedent"].map(lambda x: str(x).lower().replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\n', ''))

new = new.rename(columns={
    0: 'subsidiary',
    1: 'contractor',
    2: 'worktype',
    3: 'place',
    4: 'description'})
new.to_csv('fixed_precedents.csv', index=True, quoting=csv.QUOTE_ALL)
# print(new)