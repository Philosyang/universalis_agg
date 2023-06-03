# you can run this with a script, then use task scheduler / cron job for a set interval (e.g., 1 hour) and your DB will be constantly fed with fresh data
# add/remove item IDs to/from autoQueryList (100 items max)

import requests
import json

import mongo

query_dict = {}
with open('autoQueryDict', 'r', encoding='utf-8') as reader:
    query_dict = reader.read()
dic = json.loads(query_dict)
# print(dic)

url = 'https://universalis.app/api/v2/猫小胖/'
for key in dic:
    url += key + ','
url += '?listings=0&entries=0&fields=items.itemID%2Citems.lastUploadTime%2Citems.currentAveragePrice%2Citems.currentAveragePriceNQ%2Citems.currentAveragePriceHQ'
# print(url)

x = requests.get(url)
y = json.loads(x.text)

# print(y)

for item in y['items']:
    # print(y['items'][item])
    mongo.pyMongoPush(y['items'][item])