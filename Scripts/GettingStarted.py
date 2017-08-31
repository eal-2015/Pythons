import json
from pymongo import MongoClient
import pymongo
import datetime
from bson import ObjectId, json_util
from flask import Flask
import pandas as pd
app = Flask(__name__)
'''
from collections import OrderedDict
from pymongo import MongoClient
import bson
import bson.regex
import bson.son
'''

mongoIp = "10.190.80.25"

@app.route("/MeasurementsBetweenDates/<start>/<end>/<lane>/<cartype>/<name>")
def getMeasurementsBetweenDates(start, end, lane, cartype, name):
    col = connectToMeasurements()
    found = {}
    i = 0
    #fromdb = col.find({'$text': {'$search': name}}).limit(15) #<-- slow?
    #fromdb = col.find({'stationName': {"$regex": name}}).limit(15) #<-- fast?
    query = []
    query.append({'stationName': {'$regex': name}})
    query.append({'lane': {'$eq': int(lane)}})
    query.append({'carType': {'$eq': int(cartype)}})
    #query.append({'dateTime': {'$gte': datetime.datetime(2017, 4, 30, 21, 35, 17)}})
    #query.append({'dateTime': {'$lte': datetime.datetime(2017, 4, 30, 22, 35, 17)}})
    #splitdaytime = str(start).split(" ")
    #splitday = splitdaytime[0].split("-")
    #splittime = splitdaytime[1].split(":")
    #datefrom = datetime.datetime(int(splitday[0]), int(splitday[1]), int(splitday[2]), int(splittime[0]), int(splittime[1]), int(splittime[2]))
    #query.append({'dateTime': {'$gte': datefrom}})
    query.append({'dateTime': {'$gte': datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')}})
    query.append({'dateTime': {'$lte': datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')}})    
    #splitdaytime = str(end).split(" ")
    #splitday = splitdaytime[0].split("-")
    #splittime = splitdaytime[1].split(":")
    #dateto = datetime.datetime(int(splitday[0]), int(splitday[1]), int(splitday[2]), int(splittime[0]), int(splittime[1]), int(splittime[2]))
    #query.append({'dateTime': {'$lte': dateto}})
    fromdb = col.find({"$and": query})
    for x in fromdb:
        found[i] = x
        found[i]['dateTime'] = str(x['dateTime'])
        found[i]['_id'] = str(x['_id'])
        i = i+1

    res = json.dumps(found, default=json_util.default)
    # Pandas efterbehandling af data
    data = pd.read_json(res)
    data = data.transpose()
    print(data.columns)
    data.dateTime = pd.to_datetime(data.dateTime)
    print(data.dtypes)
    print(data.columns)
    print(data.speed.count())
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
