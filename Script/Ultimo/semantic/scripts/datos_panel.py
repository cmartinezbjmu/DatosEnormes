from pymongo import MongoClient


def obtener_tweets():
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    collection = database["COL_tweets"]
    
    query = {}
    projection = {}    
    projection["user"] = 1.0
    
    
    cursor = collection.find(query, projection = projection).count()

    return cursor


def obtener_noticias():
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    collection = database["RSS_feed"]

    query = {}
    query["noticia"] = {
        u"$ne": u""
    }
    query["$and"] = [
        {
            u"noticia": {
                u"$exists": True
            }
        }
    ]
    projection = {}
    projection["noticia"] = 1.0    

    cursor = collection.find(query, projection = projection).count()

    return cursor
    

def get_data():
    tweets = obtener_tweets()
    noticias = obtener_noticias()
    total_docs = tweets + noticias
    return tweets, noticias, total_docs