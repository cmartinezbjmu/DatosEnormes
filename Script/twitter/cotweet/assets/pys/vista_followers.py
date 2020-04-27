from pymongo import MongoClient
import pandas as pd
import datetime
import plotly.express as px


def query(pais, user):
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
            
        query = {}
        query["user.screen_name"] = user

        projection = {}
        projection["user.screen_name"] = 1.0
        projection["created_at"] = 1.0
        projection["user.followers_count"] = 1.0
        data = []
        cursor = collection.find(query, projection = projection)
        fecha = datetime.datetime.strptime('2020-03-01', '%Y-%m-%d').date()

        try:
            for doc in cursor:
                tweet_date = datetime.datetime.strptime(doc['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
                if tweet_date >= fecha:
                    data.append([doc['user']['screen_name'], tweet_date, doc['user']['followers_count']])                
        finally:
            client.close()
        
        return data

def query_usuarios(pais):
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
            
        query = {}
        projection = {}
        projection["user.screen_name"] = 1.0
        projection["created_at"] = 1.0
        projection["user.followers_count"] = 1.0
        data = []
        cursor = collection.find(query, projection = projection)
        fecha = datetime.datetime.strptime('2020-03-01', '%Y-%m-%d').date()

        try:
            for doc in cursor:
                tweet_date = datetime.datetime.strptime(doc['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
                if tweet_date >= fecha:
                    data.append([doc['user']['screen_name'], tweet_date, doc['user']['followers_count']])                
        finally:
            client.close()
        df = pd.DataFrame(data,columns=['user', 'fecha', 'No.Seguidores'])
        lista_users = df.user.value_counts().reset_index()['index'].tolist()
        return lista_users
    


def plot_followers(pais, user):
    df = pd.DataFrame(query(pais, user), columns=['usuario', 'fecha', 'No. Seguidores'])
    df = df.sort_values(by=['fecha']).reset_index()
    fig = px.line(df, x="fecha", y="No. Seguidores", color='usuario')

    return fig


def lista_usuarios(pais):    
    return query_usuarios(pais)







