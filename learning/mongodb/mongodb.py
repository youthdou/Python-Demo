import pymongo
import json
import pprint
import sys
import ConfigManager
import bson

def readData():
    with open('data.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        if '_id' in data:
            data['_id'] = bson.objectid.ObjectId(data['_id'])
        return data

def connect():
    CONFIG = ConfigManager.ConfigManager('config.json')
    client = pymongo.MongoClient(CONFIG.get('host'), CONFIG.get('port'))
    db = client[CONFIG.get('db')]
    db.authenticate(CONFIG.get('user'), CONFIG.get('passwd'))
    collection = db[CONFIG.get('collection')]
    #for document in collection.find():
    #    pprint.pprint(document)
    #print("Count: ", collection.count())
    return collection

def find(collection):
    for document in collection.find():
        pprint.pprint(document)

def insert(collection):
    collection.insert_one(readData())


if __name__ == '__main__':
    collection = connect()
    if collection is None:
        sys.exit(1)
    find(collection)
