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
        projection["coherencia"] = 1.0

        data = []
        cursor = collection.find(query, projection = projection)
        try:
            for doc in cursor:
                try:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], doc['coherencia']])
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
        projection["coherencia"] = 1.0

        data = []
        cursor_col = collection_col.find(query, projection = projection)
        cursor_arg = collection_arg.find(query, projection = projection)
        try:
            for doc in cursor_col:
                try:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], doc['coherencia']])
                except KeyError as e:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], ''])
            for doc in cursor_arg:
                try:
                    data.append([doc['_id'], doc['user'], doc['reply_or_quote'], doc['coherencia']])
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
        clf = load(cwd + '/assets/pys/modelo_coherencia_col.joblib')    
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd + "/assets/pys/vocabulario_coherencia_col.pkl", "rb")))
    if pais == 'ARG':
        clf = load(cwd + '/assets/pys/modelo_coherencia_arg.joblib')    
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd + "/assets/pys/vocabulario_coherencia_arg.pkl", "rb")))
    else:
        clf = load(cwd + '/assets/pys/modelo_coherencia_mix.joblib')    
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd + "/assets/pys/vocabulario_coherencia_mix.pkl", "rb")))
    return clf, loaded_vec


## Poner el label de la emoción seg+un el número
def label_coherencia(number):
    coherencias = [
                    ["Si",0],
                    ["No",1]
                  ]
    coherencia = ''
    for i in range(len(coherencias)):
        if coherencias[i][1] == number:
            coherencia = coherencias[i][0]
    return coherencia


def plot_coherencia(pais):
    clf, loaded_vec = load_model(pais)
    df = pd.DataFrame(query(pais),columns=['_id', 'influencer', 'tweet', 'coherencia'])
    df['prediccion'] = df['tweet'].apply(lambda x: label_coherencia(int(clf.predict(loaded_vec.transform([quitar_cuentas(x)]))[0])))
    df = df.groupby(['prediccion', 'influencer']).count().reset_index()
    fig_1 = px.treemap(df, path=['prediccion', 'influencer'], values='coherencia', title='Coherencia general')
    fig_2 = px.treemap(df, path=['influencer', 'prediccion'], values='coherencia', title='Coherencia por influencer')

    return fig_1, fig_2
