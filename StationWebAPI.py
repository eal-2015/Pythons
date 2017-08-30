import json
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, jsonify
app = Flask(__name__)

client = MongoClient()
db = client.Trafik_DB
col = db.Stations

# for fixing ObjectId when finding item in database
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class Station:
    def __init__(self, stationName, stationAreaCode, id=None):
        if id != None:
            self._id = id
        self.name = stationName
        self.areaCode = stationAreaCode

def connectToStation():
    client = MongoClient()
    db = client.Trafik_DB
    col = db.Stations

@app.route("/InsertStation/<name>/<areacode>")
def insertStation(name, areacode):
    connectToStation()
    obj = Station(name, areacode)
    objid = col.insert_one(obj.__dict__).inserted_id
    print(col.find_one({"_id": objid}))
    return "Ok"

@app.route("/GetAllStations")
def getAllStations():
    connectToStation()
    found = col.find({})
    tosend = {}
    i = 0
    for item in found:
        tosend[i] = item
        i = i+1
    
    return JSONEncoder().encode(tosend)

@app.route("/GetStation/<name>")
def getStation(name):
    connectToStation()
    found = col.find_one({"name": name})
    found = JSONEncoder().encode(found)
    return found

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
