from pymongo import MongoClient
from bson.code import Code


reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i];"
               "  }"
               "  return total;"
               "}")


def cuenta_tweets():
    map = Code("function () {"
            "var tweets = this.id;"                       
            "emit(tweets, 1);"
            "}")
    return map


def cuenta_replys():
    map = Code("function () {"            
            "var tweet_replys = this.replys;"
            "tweet_replys.forEach(function(y) {"
            "emit(y['id'], 1);"
            "});" 
          "}")
    
    return map

def cuenta_quotes():
    map = Code("function () {"            
                "var tweet_quotes = this.quotes;"
                "tweet_quotes.forEach(function(y) {"
                "emit(y['id'], 1);"
                "});" 
            "}")
    
    return map


def cuenta_total():
    while True:
        try:
            client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
            database = client["Grupo03"]
            collection = database["ARG_tweets"]
        finally:
            if collection: break

    mapper = cuenta_tweets()
    result = database.ARG_tweets.map_reduce(mapper, reduce, "cant_ARG")
    total_tweets = collection.find().count()

    mapper = cuenta_replys()
    result = database.ARG_tweets.map_reduce(mapper, reduce, "cant_ARG")
    total_replys = collection.find().count()

    mapper = cuenta_quotes()
    result = database.ARG_tweets.map_reduce(mapper, reduce, "cant_ARG")
    total_quotes = collection.find().count()

    return total_tweets + total_replys + total_quotes

