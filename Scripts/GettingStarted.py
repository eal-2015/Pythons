import json
from pymongo import MongoClient
import pymongo
import datetime
from bson import ObjectId, json_util
from flask import Flask
import pandas as pd
import time
app = Flask(__name__)

mongoIp = "10.190.80.25"

@app.route("/Counts")
def getCountForEachStation():
    #'''
    start = time.time()
    col = connectToStation()
    found = {}
    data = col.find({})
    for x in data:
        found[x['name']] = 0
    col = connectToMeasurements()
    for x in found:
        print("Checking: " + x)
        go = time.time()
        found[x] = col.find({'$text': {"$search": "\""+x+"\""}}).count()
        #found[x] = col.find({'stationName': {"$regex": x}}).count()
        print("Took: " + str(time.time() - go))
        print("Found: " + str(found[x]))
    end = time.time()
    res1 = end - start
    print("text:")
    print(res1)
    #'''
    '''
    start = time.time()
    col = connectToStation()
    found = {}
    data = col.find({})
    for x in data:
        found[x['name']] = 0
    col = connectToMeasurements()
    for x in found:
        print("Checking: " + x)
        go = time.time()
        #found[x] = col.find({'$text': {"$search": x}}).count()
        found[x] = col.find({'stationName': {"$regex": x}}).count()
        print("Took: " + str(time.time() - go))
        print("Found: " + str(found[x]))
    end = time.time()
    #'''
    #print("text:")
    #print(res1)
    print("total:")
    print(end - start)

    return "Done"
    #return json.dumps(found, default=json_util.default)

@app.route("/MeasurementsBetweenDates/<start>/<end>/<name>") # from, to, name, speed, cartype, lane?
@app.route("/MeasurementsBetweenDates/<start>/<end>/<name>/<lane>/<cartype>")

def getMeasurementsBetweenDates(start, end, name, lane=None, cartype=None):
    col = connectToMeasurements()
    #fromdb = col.find({'$text': {'$search': name}}).limit(15) #<-- slow?
    #fromdb = col.find({'stationName': {"$regex": name}}).limit(15) #<-- fast?
    query = []
    if lane != None:
        query.append({'lane': {'$eq': int(lane)}})
    if cartype != None:
        query.append({'carType': {'$eq': int(cartype)}})
    query.append({'stationName': {'$regex': name}})
    query.append({'dateTime': {'$gte': datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')}})
    query.append({'dateTime': {'$lte': datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')}})
    fromdb = col.find({"$and": query})
    found = {}
    i = 0
    for x in fromdb:
        found[i] = x
        found[i]['dateTime'] = str(x['dateTime'])
        found[i]['_id'] = str(x['_id'])
        i = i+1

    res = json.dumps(found, default=json_util.default)
    # Pandas efterbehandling af data
    '''
    data = pd.read_json(res)
    data = data.transpose()
    print(data.columns)
    data.dateTime = pd.to_datetime(data.dateTime)
    print(data.dtypes)
    print(data.columns)
    print(data.speed.count())
    '''
    return res
    #return json.dumps(found, default=json_util.default)

@app.route("/GetStation/<name>")
def getOneStation(name):
    col = connectToStation()
    found = {}
    i = 0
    fromdb = col.find({'$text': {'$search': name}})
    for x in fromdb:
        found[i] = x
        i = i+1
    return json.dumps(found, default=json_util.default)

@app.route("/GetAllStations")
def getAllStations():
    col = connectToStation()
    found = col.find({})
    tosend = {}
    i = 0
    for item in found:
        tosend[i] = item
        i = i+1
    return json.dumps(tosend, default=json_util.default)

# Helping methods for fixing ObjectId and changing collection in DB

# not needed?
# for fixing ObjectId when finding item in database
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def connectToStation():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Stations

def connectToMeasurements():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Measurements

# for keeping the flask api running
if __name__ == '__main__':
    app.run()
