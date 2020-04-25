#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:52:12 2020

@author: davidsaw
"""

from pymongo import MongoClient, errors

client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
database = client["Grupo03"]
collection = database["COL_tweets"]
collection_dataset = database["COL_dataset"]

query = {}
projection = {}
projection["created_at"] = u"$created_at"
projection["hashtags"] = u"$hashtags"
projection["_id"] = 0

cursor = collection.find(query, projection = projection)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()
    
    
    
from bson.code import Code
map = Code("function () {"
                    "  this.hashtags.forEach(function(z) {"
                    "    emit(z, 1);"
                    "  });"
                    "}")


reduce = Code("function (key, values) {"
                "  var total = 0;"
                "  for (var i = 0; i < values.length; i++) {"
                "    total += values[i];"
                "  }"
                "  return total;"
                "}")

result = collection.map_reduce(map, reduce, "myresults")
for doc in result.find():
    print(doc)







