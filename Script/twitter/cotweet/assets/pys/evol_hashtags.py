from pymongo import MongoClient
import pandas as pd
import datetime
from bson.code import Code
import plotly.express as px

def mapreduce(pais):
    map = Code("function () {"
            "var hashtags_text = this.hashtags;"
            "var hashtags_date = this.created_at.split(' ');"
            "hashtags_text.forEach(function(z) {"
            "var text = z['text'].toLowerCase();"
            "emit(text.concat('#').concat(hashtags_date[1]).concat(hashtags_date[2]).concat(hashtags_date[5]), 1);"
            "});"
           
            "var hashtags_text_reply = this.replys;"
            "hashtags_text_reply.forEach(function(y) {"
            "var hashtags_date = y['created_at'].split(' ');"
            "var hashtags = y['hashtags'];"
            "hashtags.forEach(function(x) {"
            "var text = x['text'].toLowerCase();"           
            "emit(text.concat('#').concat(hashtags_date[1]).concat(hashtags_date[2]).concat(hashtags_date[5]), 1);"
            "});"           
            "});"    

            "var hashtags_text_quotes = this.quotes;"
            "hashtags_text_quotes.forEach(function(m) {"
            "var hashtags_date = m['created_at'].split(' ');"
            "var hashtags = m['hashtags'];"
            "hashtags.forEach(function(n) {"
            "var text = n['text'].toLowerCase();"           
            "emit(text.concat('#').concat(hashtags_date[1]).concat(hashtags_date[2]).concat(hashtags_date[5]), 1);"
            "});"           
            "});"           
            "}")
    
    reduce = Code("function (key, values) {"
               "  var total = 0;"
               "  for (var i = 0; i < values.length; i++) {"
               "    total += values[i];"
               "  }"
               "  return total;"
               "}")

    if pais != 'CA':
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection = database[pais + "_tweets"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection:
                    break
        result = collection.map_reduce(map, reduce, "evol_hashtags")
    else:
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection_col = database.COL_tweets
                collection_arg = database.ARG_tweets
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection_col and collection_arg:
                    break

        result = collection_col.map_reduce(map, reduce, "evol_hashtags_COL")
        result = collection_arg.map_reduce(map, reduce, "evol_hashtags_ARG")

def query(pais):
    if pais != 'CA':
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection = database["evol_hashtags"]

                query = {}
                projection = {}
                projection["_id"] = 1.0
                projection["value"] = 1.0

                cursor = collection.find(query, projection = projection)
                data = []
                fecha = datetime.datetime.strptime('2020-04-01', '%Y-%m-%d')
                try:
                    for doc in cursor:
                        dates = doc['_id'].split('#')
                        tweet_date = datetime.datetime.strptime(dates[1], '%b%d%Y')
                        if tweet_date >= fecha:
                            data.append([dates[0], tweet_date, doc['value']])
                finally:
                    client.close()
            finally:
                if collection:
                    break
        df_hashtags = pd.DataFrame(data,columns=['hashtag', 'date', 'value'])
        return df_hashtags

    else:
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection = database["evol_hashtags_COL"]

                query = {}
                projection = {}
                projection["_id"] = 1.0
                projection["value"] = 1.0

                cursor = collection.find(query, projection = projection)
                data = []
                fecha = datetime.datetime.strptime('2020-04-01', '%Y-%m-%d')
                try:
                    for doc in cursor:
                        dates = doc['_id'].split('#')
                        tweet_date = datetime.datetime.strptime(dates[1], '%b%d%Y')
                        if tweet_date >= fecha:
                            data.append([dates[0], tweet_date, doc['value']])
                finally:
                    pass
                try:
                    collection = database["evol_hashtags_ARG"]
                    cursor = collection.find(query, projection = projection)
                    for doc in cursor:
                        dates = doc['_id'].split('#')
                        tweet_date = datetime.datetime.strptime(dates[1], '%b%d%Y')
                        if tweet_date >= fecha:
                            data.append([dates[0], tweet_date, doc['value']])
                finally:
                    pass
            finally:
                if collection:
                    client.close()
                    break
        df_hashtags = pd.DataFrame(data,columns=['hashtag', 'date', 'value'])
        return df_hashtags

def evol_hastags_main(pais):
    mapreduce(pais)
    df_hashtags = query(pais)
    fig = px.line(df_hashtags, x="date", y="value", color='hashtag')
    return fig