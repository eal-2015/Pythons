import json
from pymongo import MongoClient
import pymongo
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

client = MongoClient("10.190.80.25")
db = client.Trafik_DB
col = db.Stations

@app.route("/MeasurementsBetweenDates/<start>/<end>/<lane>/<cartype>/<stationname>")
def getMeasurementsBetweenDates(start, end, lane, cartype, stationname):
    connectToMeasurements()
    found = []
    for x in col.find({'$text': {'$search': stationname}}):
        found.append(x)
    return pd.read_json(found) #JSONEncoder().encode(found)

@app.route("/GetStation/<name>")
def getOneStation(name):
    connectToStation()
    found = []
    for x in col.find({'$text': {'$search': name}}):
        found.append(x)
    return JSONEncoder().encode(found)

@app.route("/GetAllStations")
def getAllStations():
    connectToStation()
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
    client = MongoClient()
    db = client.Trafik_DB
    col = db.Stations

def connectToMeasurements():
    client = MongoClient()
    db = client.Trafik_DB
    col = db.Measurements

# for keeping the flask api running
if __name__ == '__main__':
    app.run()
