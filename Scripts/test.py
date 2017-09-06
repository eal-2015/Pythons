import json #used for converting to json
from pymongo import MongoClient #used for connecting to mongodb
import pymongo #used for interacting with mongodb
from bson import json_util #used with json to make sure we got the format right
import cgitb #for exception handling
import cgi #for getting the arguments in the url

cgitb.enable() #used for handling exceptions

args = cgi.FieldStorage() #gets a dictionary of the arguments like: {'argument key': 'argument value'}

mongoIp = "localhost"

def connectToStation():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Stations

def connectToMeasurements():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Measurements

def fixStation(station):
    station['_id'] = str(station['_id'])
    station['installed'] = str(station['installed'])
    return station

def fixMeasurement(measurement):
    measurement['_id'] = str(measurement['_id'])
    measurement['dateTime'] = str(measurement['dateTime'])
    return measurement

def getOneStation(name):
    col = connectToStation()
    found = {}
    i = 0
    fromdb = col.find({'name': name})
    for x in fromdb:
        found[i] = fixStation(x)
        i = i+1
    return json.dumps(found, default=json_util.default)

def getAllStations():
    col = connectToStation()
    found = col.find({})
    tosend = {}
    i = 0
    for item in found:
        tosend[i] = fixStation(item)
        i = i+1
    return json.dumps(tosend, default=json_util.default)

def runMe(allArgs):
    if len(allArgs) == 0: #if no args were sent
        return getAllStations()
    #if we have args use the name to get a station
    return getOneStation(args.getvalue('name'))

print('Content-Type: text/plain') #can be changed for what you like
print('Access-Control-Allow-Origin: *') #needed
print('') #needed
print(runMe(args)) #run what ever function you want
