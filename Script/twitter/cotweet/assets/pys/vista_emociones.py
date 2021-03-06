from pymongo import MongoClient
from bson.code import Code
import pandas as pd
import re
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px
import os
import pickle

cwd = os.getcwd()

def query(pais):
    if pais != 'CA':
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection = database[pais + "_dataset"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection:
                    break
            
        query = {}
        projection = {}
        projection["_id"] = 1.0
        projection["reply_or_quote"] = 1.0
        projection["user"] = 1.0
        projection["emocion"] = 1.0

        data = []
        cursor = collection.find(query, projection = projection)
        try:
            for doc in cursor:
                try:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], doc['emocion']])
                except KeyError as e:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], ''])
                
        finally:
            client.close()
        
        return data
    
    else:
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection_col = database["COL_dataset"]
                collection_arg = database["ARG_dataset"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection_col and collection_arg:
                    break
        query = {}
        projection = {}
        projection["_id"] = 1.0
        projection["reply_or_quote"] = 1.0
        projection["user"] = 1.0
        projection["emocion"] = 1.0

        data = []
        cursor_col = collection_col.find(query, projection = projection)
        cursor_arg = collection_arg.find(query, projection = projection)
        try:
            for doc in cursor_col:
                try:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], doc['tendencia']])
                except KeyError as e:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], ''])
            for doc in cursor_arg:
                try:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], doc['tendencia']])
                except KeyError as e:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], ''])
        finally:
            client.close()
        return data


def quitar_cuentas(a):
    texto=" ".join(filter(lambda x:x[0]!='@', a.split()))
    return texto


def load_model(pais):
    if pais == 'COL':
        clf = load(cwd + '/assets/pys/modelo_sentimientos_col.joblib')    
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd + "/assets/pys/vocabulario_sentimientos_col.pkl", "rb")))
    if pais == 'ARG':
        clf = load(cwd + '/assets/pys/modelo_sentimientos_arg.joblib')
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd + "/assets/pys/vocabulario_sentimientos_arg.pkl", "rb")))
    else:
        clf = load(cwd + '/assets/pys/modelo_sentimientos_mix.joblib')
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd + "/assets/pys/vocabulario_sentimientos_mix.pkl", "rb")))
    return clf, loaded_vec


## Poner el label de la emoción seg+un el número
def label_emocion(number):
    emociones=[["Neutro",0],
           ["Optimista",1],
           ["Triste",2],
           ["Enojo",3],
           ["Sorprendido",4],
           ["Orgulloso",5]]
    emocion = ''
    for i in range(len(emociones)):
        if emociones[i][1] == number:
            emocion = emociones[i][0]
    return emocion


def query_minsalud(pais):
    if pais != 'CA':
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection_dataset = database[pais + "_minsalud"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection_dataset:
                    break

        query = {}
        projection = {}
        projection["user"] = 1.0
        projection["reply_or_quote"] = 1.0
        projection["created_at"] = 1.0

        cursor = collection_dataset.find(query, projection = projection)
        data = []
        #fecha = datetime.datetime.strptime('2020-04-01', '%Y-%m-%d') "Fri Apr 10 04:09:23 +0000 2020"
        try:
            for doc in cursor:
                tweet_date = str(doc['created_at']).split('T')
                tweet_date = tweet_date[0]
        #        tweet_date = datetime.datetime.strptime(tweet_date, '%b%d%Y')            
                data.append([tweet_date, doc['user'], doc['reply_or_quote']])
        finally:
            client.close()
        df = pd.DataFrame(data,columns=['fecha', 'user', 'tweet'])
        return df

    else:
        while True:
            try:
                client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
                database = client["Grupo03"]
                collection_col = database["COL_minsalud"]
                collection_arg = database["ARG_minsalud"]
            except errors.ServerSelectionTimeoutError as err:        
                print(err)
            finally:
                if collection_col and collection_arg:
                    break

        query = {}
        projection = {}
        projection["user"] = 1.0
        projection["reply_or_quote"] = 1.0
        projection["created_at"] = 1.0

        cursor_col = collection_col.find(query, projection = projection)
        cursor_arg = collection_arg.find(query, projection = projection)
        data = []
        #fecha = datetime.datetime.strptime('2020-04-01', '%Y-%m-%d') "Fri Apr 10 04:09:23 +0000 2020"
        try:
            for doc in cursor_col:
                tweet_date = str(doc['created_at']).split('T')
                tweet_date = tweet_date[0]         
                data.append([tweet_date, doc['user'], doc['reply_or_quote']])

            for doc in cursor_arg:
                tweet_date = str(doc['created_at']).split('T')
                tweet_date = tweet_date[0]         
                data.append([tweet_date, doc['user'], doc['reply_or_quote']])
        finally:
            client.close()
        df = pd.DataFrame(data,columns=['fecha', 'user', 'tweet'])
        return df

def plot_emociones(pais):
    clf, loaded_vec = load_model(pais)
    df = pd.DataFrame(query(pais),columns=['_id', 'influencer', 'tweet', 'emocion'])
    df['prediccion'] = df['tweet'].apply(lambda x: label_emocion(int(clf.predict(loaded_vec.transform([quitar_cuentas(x)]))[0])))
    df = df.groupby(['prediccion', 'influencer']).count().reset_index()

    # Grafico de minsalud
    df_minsalud = query_minsalud(pais)
    df_minsalud['prediccion'] = df_minsalud['tweet'].apply(lambda x: label_emocion(int(clf.predict(loaded_vec.transform([quitar_cuentas(x)]))[0])))
    df_plot = df_minsalud.groupby(['fecha', 'prediccion']).count().reset_index()

    fig_1 = px.treemap(df, path=['prediccion', 'influencer'], values='emocion', title='Emociones generales')
    fig_2 = px.treemap(df, path=['influencer', 'prediccion'], values='emocion', title='Emociones hacia influencers')
    fig_3 = px.line(df_plot, x="fecha", y="tweet", color='prediccion')
    return fig_1, fig_2, fig_3
