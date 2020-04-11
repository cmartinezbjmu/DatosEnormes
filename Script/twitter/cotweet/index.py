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
import random
import os
from pymongo import MongoClient, errors
from random import randint
from bson.objectid import ObjectId
from time import sleep

cwd = os.getcwd()

# Librería para nube de temas
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

## Importar aplicaciones
from app import app
# Paǵinas de la app
from apps import homepage, model
# Barra izquierda
from navbar import Navbar


#### Crear nube de temas del home
read = 'assets/find_query.json'

data = []
with open(read) as f:
    for line in f:
        data.append(json.loads(line))

temas=[]        
for i in range(len(data)):
    ht=data[i]['hashtags']
    for i in range(len(ht)):
        temas.append(ht[i]['text'])

def yellow_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 10)
        
wordcloud = WordCloud(background_color="white",width=4096, height=2160).generate(" ".join(temas))
wordcloud.recolor(color_func = yellow_color_func)
wordcloud.to_file(cwd+"/assets/images/home-nube.png")

### Extrae tweet aleatorio
def get_random_tweet():
    try:
        client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        client.server_info()
        db = client.Grupo03
        collection_dataset = db.ARG_dataset
        query = dict()
        query["id_reply_or_quote"] = {
            u"$exists": True
        }
        query["emocion"] = {
            u"$exists": False
        }
        query["tendencia"] = {
            u"$exists": False
        }
        projection = dict()
        projection["_id"] = 1.0
        projection["user"] = 1.0
        projection["tweet"] = 1.0
        projection["reply_or_quote"] = 1.0
        cursor = collection_dataset.find(query, projection = projection)
        total_sin_etiquetar = cursor.count()
        #print(total_sin_etiquetar)
        total_documents = collection_dataset.estimated_document_count()
        r = random.randint(0,total_documents)
        randomElement = collection_dataset.find(query, projection = projection).limit(1).skip(r)
        # print(randomElement)
        for i in randomElement:
            _id = i['_id']
            user = i['user']
            tweet = i['tweet']            
            reply_or_quote = i['reply_or_quote']
        
        return _id, user, tweet, reply_or_quote


    except errors.ServerSelectionTimeoutError as err:        
        print(err)

    finally:
        client.close()



### Extrae tweet aleatorio
def update_tweet_dataset(id_document, emocion, tendencia):
    try:
        client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        client.server_info()
        db = client.Grupo03
        collection_dataset = db.ARG_dataset
        query = {}
        query['_id'] = ObjectId(id_document)
        update = {
                    "$set": { 
                        "emocion": emocion,
                        "tendencia": tendencia},
                }
        #print(collection_dataset.update_one(query, update))
 
    except errors.ServerSelectionTimeoutError as err:        
        print(err)

    finally:
        client.close()



#calificacion=pd.read_csv('../../../export_dataframe.csv')
#calificacion = pd.DataFrame.from_dict(tweet)



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
                    html.Img(src="/assets/images/co-tweet-banner.png",style={'width': '100%'}),
                    html.H2(id='titulo'),
                    html.P(id='explanation'),           
                    html.H5('Juan Camilo Cardenas'),
                    html.H6('j.cardenasc@uniandes.edu.co'),
                    html.H5('Cristian Martinez'),
                    html.H6('c.martinezb1@uniandes.edu.co'),
                    html.H5('David Ocampo'),
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
 

### Título de las páginas

@app.callback(Output('titulo','children', ),
    [Input('url', 'pathname')])
def display_title(pathname):
    if pathname == '/':
        return homepage.app.titulo
    if pathname == '/apps/model':
        return model.app.titulo

### Explicación de las páginas

@app.callback(Output('explanation','children', ),
    [Input('url', 'pathname')])
def display_explanation(pathname):
    if pathname == '/':
        return homepage.app.explanation
    if pathname == '/apps/model':
        return model.app.explanation

########################################################
########Funciones de las paǵinas########################
########################################################


### Mostrar tweets para calificar cuenta - respuesta

@app.callback(
    [dash.dependencies.Output('model-cuenta', 'children'),
    dash.dependencies.Output('model-respuesta', 'children'),
    dash.dependencies.Output('model-emocion-ct', 'value'),
    dash.dependencies.Output('model-tendencia-ct', 'value')],
    
    [dash.dependencies.Input('model-boton-ct', 'n_clicks')],

    [dash.dependencies.State('model-emocion-ct', 'value'),
    dash.dependencies.State('model-tendencia-ct', 'value')]

    )


def update_tweet(n_clicks, emocion, tendencia):
    #changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    try:
        if n_clicks > 0:
            while 1:
                try:
                    _id, user, tweet, reply_or_quote = get_random_tweet()
                    break
                except TypeError as e:
                    sleep(5)
                    continue

            tweet_render = tweet
            respuesta = reply_or_quote
            if (len(str(emocion)) > 0) and (len(str(tendencia)) > 0):
                update_tweet_dataset(_id, emocion, tendencia)
                return tweet_render, respuesta, '', ''

    except dash.exceptions.InvalidCallbackReturnValue as e:
        pass
     
    

@app.callback(
    [dash.dependencies.Output('model-boton-ct', 'disabled')],

    [dash.dependencies.Input('model-emocion-ct', 'value'),
    dash.dependencies.Input('model-tendencia-ct', 'value')]
    )


def update_tweet(emocion, tendencia):
    if ((emocion == '') or (tendencia == '')):
        disable = True,
    else:
        disable = False,
    
    return disable
    
    

### Mostrar tweets para calificar tweet semántica

@app.callback(
    [dash.dependencies.Output('model-tweet', 'children'),
    dash.dependencies.Output('model-emocion-t', 'value')],
    
    [dash.dependencies.Input('model-boton-t', 'n_clicks')],

    [dash.dependencies.State('model-emocion-t', 'value')]

    )


def update_tweet(n_clicks, emocion):
    #changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    try:
        if n_clicks > 0:
            _id, user, tweet, reply_or_quote = get_random_tweet()
            tweet_render = tweet
            respuesta = reply_or_quote
            if (len(str(emocion)) > 0) and (len(str(tendencia)) > 0):
                update_tweet_dataset(_id, emocion, '')
                return tweet_render, ''

    except dash.exceptions.InvalidCallbackReturnValue as e:
        pass
     
    

@app.callback(
    [dash.dependencies.Output('model-boton-t', 'disabled')],

    [dash.dependencies.Input('model-emocion-t', 'value')]
    )


def update_tweet(emocion):
    if (emocion == ''):
        disable = True,
    else:
        disable = False,
    
    return disable


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=False)
