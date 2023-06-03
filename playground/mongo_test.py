from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
db = client.dbName
coll = db.collectionName


# insert code goes here
docs = [
    {"itemID": 39313, "lastUploadTime": 1685773979116, "currentAveragePrice": 265151.58,
        "currentAveragePriceNQ": 246783.78, "currentAveragePriceHQ": 304541.22},
]

result = coll.insert_many(docs)

# display the results of your operation
print(result.inserted_ids)

# Close the connection to MongoDB when you're done.
client.close()
