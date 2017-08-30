import json
from pymongo import MongoClient
import pymongo
from bson import ObjectId, json_util
from flask import Flask
app = Flask(__name__)
'''
from collections import OrderedDict
from pymongo import MongoClient
import bson
import bson.regex
import bson.son
'''

client = MongoClient("10.190.80.25")
db = client.Trafik_DB

@app.route("/MeasurementsBetweenDates/<start>/<end>/<lane>/<cartype>/<stationname>")
def getMeasurementsBetweenDates(start, end, lane, cartype, stationname):
    col = connectToMeasurements()
    found = {}
    i = 0
    #fromdb = col.find({'$text': {'$search': stationname}} and {'$carType':  {'$search': cartype}})
    query = {'stationName': stationname}
    #query['lane'] = lane
    #query['carType'] = cartype
    #query = [{'stationName': stationname}]
    #query.append({'lane': lane})
    #query.append({'carType': cartype})
    fromdb = col.find(query)
    for x in fromdb:
        found[i] = x
        i = i+1
    return json.dumps(found, default=json_util.default)

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
    client = MongoClient("10.190.80.25")
    db = client.Trafik_DB
    return db.Stations

def connectToMeasurements():
    client = MongoClient("10.190.80.25")
    db = client.Trafik_DB
    return db.Measurements

# for keeping the flask api running
if __name__ == '__main__':
    app.run()
