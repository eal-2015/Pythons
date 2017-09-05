import json
from pymongo import MongoClient
import pymongo
import datetime
from bson import ObjectId, json_util
import pandas as pd
import time
import cgitb
import cgi

cgitb.enable()

form = cgi.FieldStorage()

mongoIp = "localhost"

def connectToStation():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Stations

def connectToMeasurements():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Measurements

def getOneStation(name):
    col = connectToStation()
    found = {}
    i = 0
    fromdb = col.find({'name': name})
    for x in fromdb:
        found[i] = x
        i = i+1
    print(json.dumps(found, default=json_util.default))

def getAllStations():
    col = connectToStation()
    found = col.find({})
    tosend = {}
    i = 0
    for item in found:
        tosend[i] = item
        i = i+1
    print(json.dumps(tosend, default=json_util.default))

print('Content-Type: text/plain')
print('')
#getAllStations()
getOneStation(str(form.getvalue('name')))
