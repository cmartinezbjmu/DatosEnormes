import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash_table
from sqlalchemy import create_engine
import plotly.express as px
import re
import json
import os
from pymongo import MongoClient, errors
from random import randint
from bson.objectid import ObjectId
from time import sleep
from PIL import Image
from assets.pys.modelo_tweet import quitar_cuentas
from sklearn.feature_extraction.text import CountVectorizer
from joblib import dump, load
from assets.pys.modelo_top_temas import top_temas_funcion, top_temas_noticieros_funcion
from assets.pys.evol_hashtags import evol_hastags_main
from assets.pys.vista_tendencia import plot_tendencia
from assets.pys.vista_emociones import plot_emociones
from assets.pys.vista_coherencia import plot_coherencia
from assets.pys.recolectar_tweets import main as recolectar_tweets
from assets.pys.vista_followers import plot_followers, lista_usuarios
from assets.pys.total_tweets_ARG import cuenta_total as cuenta_arg
from assets.pys.total_tweets_COL import cuenta_total as cuenta_col
import pickle
import random

cwd = os.getcwd()


##Librerías de correr modelos
from assets.pys.modelo_tweet import main as entrenar_modelo
from assets.pys.mejor_modelo import main as mejor_modelo


# Librería para nube de temas
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

## Importar aplicaciones
from app import app
# Paǵinas de la app
from apps import homepage, model, prediccion, top_temas, influencers, panel
# Barra izquierda
from navbar import Navbar


#### Crear nube de temas del home

# Relizar consultas a la base de datos

from pymongo import MongoClient
import pandas as pd
import random


client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
database = client["Grupo03"]
collection = database["COL_tweets"]
collection_dataset = database["COL_dataset"]

# Extraemos hashtags de los influenciadores
query = {}
query["hashtags"] = {
    u"$gt": {
        u"$size": 0.0
    }
}


projection = {}
projection["hashtags"] = 1.0

cursor = collection.find(query, projection = projection)
data = []
try:
    for doc in cursor:
        for i in range(len(doc['hashtags'])):
            data.append(doc['hashtags'][i]['text'].lower())
finally:
    client.close()

# Extraemos hashtags de los comentarios
query = {}
query["replys.id"] = {
    u"$exists": True
}
query["replys.hashtags"] = {
    u"$ne": u""
}

projection = {}
projection["replys.hashtags"] = 1.0

cursor = collection.find(query, projection = projection)
#data = []
try:
    for doc in cursor:
        for i in range(len(doc['replys'])):
            if len(doc['replys'][i]['hashtags']) > 0:
                for j in range(len(doc['replys'][i]['hashtags'])):
                    data.append(doc['replys'][i]['hashtags'][j]['text'].lower())
finally:
    client.close()

# Extraemos hashtags de las citas
query = {}
query["quotes.id"] = {
    u"$exists": True
}
query["quotes.hashtags"] = {
    u"$ne": u""
}

projection = {}
projection["quotes.hashtags"] = 1.0

cursor = collection.find(query, projection = projection)
#data = []
try:
    for doc in cursor:
        for i in range(len(doc['quotes'])):
            if len(doc['quotes'][i]['hashtags']) > 0:
                for j in range(len(doc['quotes'][i]['hashtags'])):
                    data.append(doc['quotes'][i]['hashtags'][j]['text'].lower())
finally:
    client.close()


## Cargar modelo de predicción
#Emociones
clf_col = load(cwd+'/assets/pys/modelo_sentimientos_col.joblib') 
loaded_vec_col = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_sentimientos_col.pkl", "rb")))


emociones=[["Neutro",0],
           ["Optimista",1],
           ["Triste",2],
           ["Enojo",3],
           ["Sorprendido",4],
           ["Orgulloso",5]]

## Poner el label de la emoción según el número
def label_emocion(number):
    emocion=''
    for i in range(len(emociones)):
        if emociones[i][1]==number:
            emocion=emociones[i][0]
    return emocion
    
tendencias =[["Apoyo",0],
             ["Contradicción",1],
             ["Matoneo",2]]

    
def label_tendencia(number):
    tendencia = ''
    for i in range(len(tendencias)):
        if tendencias[i][1] == number:
            tendencia = tendencias[i][0]
    return tendencia
    
coherencia=[
    ["Si",0],
    ["No",1]
]


def label_coherencia(number):
    coherente = ''
    for i in range(len(coherencia)):
        if coherencia[i][1] == number:
            coherente = coherencia[i][0]
    return coherente

def yellow_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % randint(0, 10)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config['suppress_callback_exceptions'] = True

nav = Navbar()
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(
        [
            html.Div(
                [
                    html.Img(src="/assets/images/Semantic-banner.png",style={'width': '100%'}),
                    html.H2(id='titulo'),
                    html.P(id='explanation'),           
                    html.H6('Juan Camilo Cardenas'),
                    html.H6('j.cardenasc@uniandes.edu.co'),
                    html.H6('Cristian Martinez'),
                    html.H6('c.martinezb1@uniandes.edu.co'),
                    html.H6('David Ocampo'),
                    html.H6('d.ocampo@uniandes.edu.co'),
                ],
                className="div_izq_home",
            ),
            html.Div(
                [
                    html.Div(id='page-content')
                ],
                className="div_der_home",
            )
        ],
    ),   
])



### Layout de las páginas

@app.callback(Output('page-content','children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return homepage.app.layout
    if pathname == '/apps/model':
        return model.app.layout
    if pathname == '/apps/analisis':
        return influencers.app.layout
    if pathname == '/apps/prediccion':
        return prediccion.app.layout
    if pathname == '/apps/top_temas':
        return top_temas.app.layout
    if pathname == '/apps/panel':
        return panel.app.layout

### Título de las páginas

@app.callback(Output('titulo','children', ),
    [Input('url', 'pathname')])
def display_title(pathname):
    if pathname == '/':
        return homepage.app.titulo
    if pathname == '/apps/model':
        return model.app.titulo
    if pathname == '/apps/analisis':
        return influencers.app.titulo
    if pathname == '/apps/prediccion':
        return prediccion.app.titulo    
    if pathname == '/apps/top_temas':
        return top_temas.app.titulo
    if pathname == '/apps/panel':
        return panel.app.titulo

### Explicación de las páginas

@app.callback(Output('explanation','children', ),
    [Input('url', 'pathname')])
def display_explanation(pathname):
    if pathname == '/':
        return homepage.app.explanation
    if pathname == '/apps/model':
        return model.app.explanation
    if pathname == '/apps/analisis':
        return influencers.app.explanation
    if pathname == '/apps/prediccion':
        return prediccion.app.explanation    
    if pathname == '/apps/top_temas':
        return top_temas.app.explanation
    if pathname == '/apps/panel':
        return panel.app.explanation
########################################################
########Funciones de las paǵinas########################
########################################################



if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=True)
