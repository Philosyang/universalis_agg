# you can run this with a script, then use task scheduler / cron job for a set interval (e.g., 1 hour) and your DB will be constantly fed with fresh data
# add/remove item IDs to/from autoQueryList (100 items max)

# possible cert issue:
# https://stackoverflow.com/questions/69397039/pymongo-ssl-certificate-verify-failed-certificate-has-expired-on-mongo-atlas

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
url += '?entries=20&noGst=1'
# print(url)

x = requests.get(url)
y = json.loads(x.text)

# print(y)

for item in y['items']:
    # print(y['items'][item])
    mongo.pyMongoPush(y['items'][item])