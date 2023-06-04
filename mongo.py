from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime

import itemCalc as ic

uri = 'put uri in file mongo_uri'
with open('mongo_uri', 'r') as reader:
    uri = reader.read()

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


# https://www.mongodb.com/docs/guides/crud/insert/

# database and collection code goes here
db = client.universalis
coll = db.sales


def mongoWrap(y):
    mongo_filter = {}
    mongo_newvalues = {}
    mongo_newvalues_values = {}

    mongo_filter['itemID'] = y['itemID']
    # https://pymongo.readthedocs.io/en/stable/examples/datetimes.html
    mongo_filter['lastUploadTime'] = datetime.datetime.fromtimestamp(y['lastUploadTime'] / 1000)
    mongo_newvalues_values['median9Listings'], mongo_newvalues_values['median99Listings'], mongo_newvalues_values['medianListings'] = ic.columnMedian(y, 'listings', -1)
    mongo_newvalues_values['median9ListingsHQ'], mongo_newvalues_values['median99ListingsHQ'], mongo_newvalues_values['medianListingsHQ'] = ic.columnMedian(y, 'listings', 1)
    mongo_newvalues_values['medianSales'] = ic.columnMedian(y, 'recentHistory', -1)
    mongo_newvalues_values['medianSalesHQ'] = ic.columnMedian(y, 'recentHistory', 1)
    mongo_newvalues['$set'] = mongo_newvalues_values

    return [mongo_filter, mongo_newvalues]


def mongoUpsert(mongo_wrap):
    result = coll.update_one(mongo_wrap[0], mongo_wrap[1], upsert=True)
    return result.upserted_id


def pyMongoPush(y):
    out = mongoUpsert(mongoWrap(y))
    print(out)
    return


# # insert code goes here
# docs = [
#     {"itemID": 39313, "lastUploadTime": 1685772979116, "averagePrice": 265151.58, "averagePriceNQ": 246783.78, "averagePriceHQ": 304541.22},
# ]

# result = coll.insert_many(docs)

# # display the results of your operation
# print(result.inserted_ids)

# # Close the connection to MongoDB when you're done.
# client.close()
