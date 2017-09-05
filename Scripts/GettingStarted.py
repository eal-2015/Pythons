import json
from pymongo import MongoClient
import pymongo
import datetime
from bson import ObjectId, json_util
from flask import Flask
import pandas as pd
from bson.son import SON
from datetime import datetime


app = Flask(__name__)




mongoIp = "10.190.80.25"

#http://localhost:5000/MeasurementsBetweenDates/2017-04-30%2022:00:00/2017-04-30%2023:59:59/Anderupvej
#pandas behandling

def GetData(dataset, carType = None, lane = None):
    res = dataset
    if carType is not None:
        res = res[res.carType == carType]
    if lane is not None:
        res = res[res.lane == lane]
    return res

def PandasEfterbehandling(jsonfile):
    data = pd.read_json(jsonfile)
    data = data.transpose()
    return data



@app.route("/Counts")
def getCountForEachStation():
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

@app.route("/MeasurementsBetweenDates/<start>/<end>/<areaCode>") # from, to, name, speed, cartype, lane?
@app.route("/MeasurementsBetweenDates/<start>/<end>/<areaCode>/<lane>/<cartype>")

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
    
    return str(len(PandasEfterbehandling(res)))


@app.route("/AverageSpeedBetweenDates/<start>/<end>/<areaCode>") # from, to, name, speed, cartype, lane?
@app.route("/AverageSpeedBetweenDates/<start>/<end>/<areaCode>/<lane>/<cartype>")
def getAverageSpdBetweenDates(start, end, areaCode, lane=None, cartype=None):
    col = connectToMeasurements()
    
    From = datetime(int(start[0:4]), int(start[5:7]), int(start[8:10]), int(start[11:13]), int(start[14:16]), int(start[17:19]))
    To = datetime(int(end[0:4]), int(end[5:7]), int(end[8:10]), int(end[11:13]), int(end[14:16]), int(end[17:19]))
    pipeline = [
            {"$match": {"dateTime" :{"$gte":From, "$lt":To}}}   #, "areaCode":{ "$eq":areaCode} 
            #,{"$group": {"_id":"$carType","avgValue": {"$avg": "$speed"}}}
               ,{"$group": {"_id":"$areaCode","avgValue": {"$avg": "$speed"}}}
    ]
    return json.dumps(list(col.aggregate(pipeline)), default=json_util.default)



    '''
    


app = Flask(name)

mongoIp = "10.190.80.25"
from pymongo import MongoClient

@app.route("/GetMeasurementsBetweenDatesAllStations/<From>/<To>")
def GetMeasurementsBetweenDatesAllStations(From, To):


def connectToStation():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Stations


def connectToMeasurements():
    client = MongoClient(mongoIp)
    db = client.Trafik_DB
    return db.Measurements


# for keeping the flask api running
if name == 'main':
    app.run()


    '''
    
    
    #fromdb = col.find({'$text': {'$search': name}}).limit(15) #<-- slow?
    #fromdb = col.find({'stationName': {"$regex": name}}).limit(15) #<-- fast?
    '''
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
        
        '''
    #res = json.dumps(found, default=json_util.default)
    # Pandas efterbehandling af data
    

    #return str(PandasEfterbehandling(res).speed.mean())


@app.route("/CarClassesBetweenDates/<start>/<end>/<areacode>") # from, to, name, speed, cartype, lane?
@app.route("/CarClassesBetweenDates/<start>/<end>/<areacode>/<lane>")

def getCarClassesBetweenDates(start, end, areacode, lane=None, cartype=None):
    col = connectToMeasurements()
    #fromdb = col.find({'$text': {'$search': name}}).limit(15) #<-- slow?
    #fromdb = col.find({'stationName': {"$regex": name}}).limit(15) #<-- fast?
    from bson.code import Code

    
    query = []
    if lane != None:
        query.append({'lane': {'$eq': int(lane)}})
    if cartype != None:
        query.append({'carType': {'$eq': int(cartype)}})
    query.append({'areaCode': {'$eq': int(areacode)}})
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
    data = PandasEfterbehandling(res)
    print(data.groupby(data.carType).speed.count())
    res2 = data.groupby(data.carType).speed.count()
    print(res2)
    
    return res2



    
    

    #Returnerer nu et dataframe
    
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










def HowManyMeasurements(dataset):
    return len(dataset)

def HowManyMeasurements(cartype, lane):
    return len(GetData(cartype,lane))


def GetAverageSpeed(dataset):
    if len(dataset)>0:
        counter = 0
        for item in dataset.speed:
            counter = counter + item
        return (counter/ len(dataset))
    else:
        return 0









# for keeping the flask api running





if __name__ == '__main__':
    app.run()
