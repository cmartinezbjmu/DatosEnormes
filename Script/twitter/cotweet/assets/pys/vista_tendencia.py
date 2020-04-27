from pymongo import MongoClient
from bson.code import Code
import pandas as pd
import re
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
import plotly.express as px


def query():
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
    database = client["Grupo03"]
    collection = database["COL_dataset"]

    query = {}
    projection = {}
    projection["_id"] = 1.0
    projection["reply_or_quote"] = 1.0
    projection["user"] = 1.0
    projection["tendencia"] = 1.0

    data = []
    cursor = collection.find(query, projection = projection)
    try:
        for doc in cursor:
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


def load_model():
    clf = load(cwd + '/assets/pys/modelo_tendencia_col.joblib')    
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open("/home/jcardenasc93/Documents/MISO/BigData/Repo/DatosEnormes/Script/twitter/cotweet/assets/pys/vocabulario_tendencia_col.pkl", "rb")))
    return clf, loaded_vec


## Poner el label de la emoción seg+un el número
def label_tendencia(number):
    tendencias =[["Apoyo",0],
             ["Contradicción",1],
             ["Matoneo",2]]
    tendencia = ''
    for i in range(len(tendencias)):
        if tendencias[i][1] == number:
            tendencia = tendencias[i][0]
    return tendencia


def plot_tendencia():
    clf, loaded_vec = load_model()
    df = pd.DataFrame(query(),columns=['_id', 'influencer', 'tweet', 'tendencia'])
    df['prediccion'] = df['tweet'].apply(lambda x: label_tendencia(int(clf_col.predict(loaded_vec_col.transform([quitar_cuentas(x)]))[0])))
    df = df.groupby(['prediccion', 'influencer']).count().reset_index()
    fig_1 = px.treemap(df, path=['prediccion', 'influencer'], values='tendencia', title='Tendencia general')
    fig_2 = px.treemap(df, path=['influencer', 'prediccion'], values='tendencia', title='Tendencia por influencer')

    return fig_1, fig_2
