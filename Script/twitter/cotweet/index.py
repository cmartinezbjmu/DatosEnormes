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
from assets.pys.modelo_tweet_emocion_col import main as main_col
from assets.pys.modelo_tweet_emocion_col import quitar_cuentas
from sklearn.feature_extraction.text import CountVectorizer
from joblib import dump, load
from assets.pys.modelo_top_temas import top_temas_funcion
from assets.pys.evol_hashtags import evol_hastags_main
import pickle

cwd = os.getcwd()

# Librería para nube de temas
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

## Importar aplicaciones
from app import app
# Paǵinas de la app
from apps import homepage, model, tendencia, prediccion, top_temas
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


## Cargar modelo de preficción de colombia
clf_col = load(cwd+'/assets/pys/modelo_sentimientos_col.joblib') 
loaded_vec_col = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_sentimientos_col.pkl", "rb")))

clf_arg = load(cwd+'/assets/pys/modelo_sentimientos_arg.joblib') 
loaded_vec_arg = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_sentimientos_arg.pkl", "rb")))



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
    
def yellow_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % randint(0, 10)

maskArray = np.array(Image.open(cwd+"/assets/images/cloud_1.png"))     
wordcloud = WordCloud(background_color="white", collocations=False, max_words = 500, mask=maskArray)
#wordcloud.recolor(color_func = yellow_color_func)
wordcloud.generate(" ".join(data))
wordcloud.to_file(cwd+"/assets/images/home-nube.png")

### Extrae tweet aleatorio
def get_random_tweet(pais):
    _id = None
    while True:
        try:
            client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
            client.server_info()
            db = client.Grupo03
            collection_dataset = database[pais + "_dataset"]
            query = dict()
            query["id_reply_or_quote"] = {
                u"$exists": True
            }
            query["emocion"] = u""
            query["tendencia"] = u""
            projection = dict()
            projection["_id"] = 1.0
            projection["user"] = 1.0
            projection["tweet"] = 1.0
            projection["reply_or_quote"] = 1.0
            cursor = collection_dataset.find(query, projection=projection)
            total_sin_etiquetar = collection_dataset.count_documents(query)
            total_documents = collection_dataset.estimated_document_count()
            r = randint(0,total_documents)
            randomElement = collection_dataset.find(query, projection=projection).limit(-1).skip(r).next()
            _id = randomElement['_id']
            user = randomElement['user']
            tweet = randomElement['tweet']
            reply_or_quote = randomElement['reply_or_quote']

        except errors.ServerSelectionTimeoutError as err:        
            print(err)
            continue
        
        except StopIteration as e:
            print(e)

        finally:
            if _id:                
                client.close()
                break
    return _id, user, tweet, reply_or_quote


### Actualiza emoción y tendencia del tweet
def update_tweet_dataset(id_document, emocion, tendencia, coherencia, pais):
    try:
        client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        client.server_info()
        db = client.Grupo03
        collection_dataset = database[pais + "_dataset"]
        query = {}
        query['_id'] = ObjectId(id_document)
        print(id_document)
        update = {
                    "$set": { 
                        "emocion": emocion,
                        "tendencia": tendencia,
                        "coherencia": coherencia},
                        
                }
        return collection_dataset.update_one(query, update)
 
    except errors.ServerSelectionTimeoutError as err:        
        print(err)

    finally:
        client.close()


### Total etiquetados
def get_tweet_count(pais):
    try:
        client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        client.server_info()
        db = client.Grupo03
        collection_dataset = database[pais + "_dataset"]
        query = dict()
        query["id_reply_or_quote"] = {
            u"$exists": True
        }
        query["emocion"] = u""
        query["tendencia"] = u""
        projection = dict()
        projection["_id"] = 1.0
        projection["user"] = 1.0
        projection["tweet"] = 1.0
        projection["reply_or_quote"] = 1.0
        cursor = collection_dataset.find(query, projection=projection)
        total_sin_etiquetar = collection_dataset.count_documents(query)
        total_documents = collection_dataset.estimated_document_count()
        
        return total_sin_etiquetar,total_documents

    except errors.ServerSelectionTimeoutError as err:        
        print(err)

    finally:
        client.close()


def obtener_base(Pais):
    # data = None
    # while True:
    #     try:
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    collection_dataset = database[Pais + "_dataset"]
    data = pd.DataFrame(list(collection_dataset.find()))
            # col = ['reply_or_quote', 'emocion']
            # data=data[col]
        # except errors.ServerSelectionTimeoutError as err:
        #     print(err)
        # finally:
        #     if data.empty():
        #         continue
        #     else: break
    
    return data
        







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
    if pathname == '/apps/tendencia':
        return tendencia.app.layout
    if pathname == '/apps/prediccion':
        return prediccion.app.layout
    if pathname == '/apps/top_temas':
        return top_temas.app.layout

### Título de las páginas

@app.callback(Output('titulo','children', ),
    [Input('url', 'pathname')])
def display_title(pathname):
    if pathname == '/':
        return homepage.app.titulo
    if pathname == '/apps/model':
        return model.app.titulo
    if pathname == '/apps/tendencia':
        return tendencia.app.titulo
    if pathname == '/apps/prediccion':
        return prediccion.app.titulo
    if pathname == '/apps/top_temas':
        return top_temas.app.titulo

### Explicación de las páginas

@app.callback(Output('explanation','children', ),
    [Input('url', 'pathname')])
def display_explanation(pathname):
    if pathname == '/':
        return homepage.app.explanation
    if pathname == '/apps/model':
        return model.app.explanation
    if pathname == '/apps/tendencia':
        return tendencia.app.explanation
    if pathname == '/apps/prediccion':
        return prediccion.app.explanation
    if pathname == '/apps/top_temas':
        return top_temas.app.explanation
########################################################
########Funciones de las paǵinas########################
########################################################


### Mostrar tweets para calificar cuenta - respuesta

@app.callback(
    [dash.dependencies.Output('model-cuenta', 'children'),
    dash.dependencies.Output('model-respuesta', 'children'),
    dash.dependencies.Output('model-emocion-ct', 'value'),
    dash.dependencies.Output('model-tendencia-ct', 'value'),
    dash.dependencies.Output('model-idtweet', 'children'),
    dash.dependencies.Output('model-user', 'children'),
    dash.dependencies.Output('model-coherencia-ct', 'value')],
    
    [dash.dependencies.Input('model-boton-ct', 'n_clicks'),
    dash.dependencies.Input('model-seleccion', 'value')],

    [dash.dependencies.State('model-emocion-ct', 'value'),
    dash.dependencies.State('model-tendencia-ct', 'value'),
    dash.dependencies.State('model-coherencia-ct', 'value'),
    dash.dependencies.State('model-idtweet', 'children')]

    )


def update_tweet(n_clicks, pais, emocion, tendencia, coherencia, id_anterior):
    _id = None
    try:
        if n_clicks > 0:
            while True:
                try:
                    _id, user, tweet, reply_or_quote = get_random_tweet(pais)
                except TypeError as e:
                    print(e)
                finally:
                    if _id:
                        tweet_render = tweet
                        respuesta = reply_or_quote
                        break
            if (len(str(emocion)) > 0) and (len(str(tendencia)) > 0):
                while True:
                    resultado_update = update_tweet_dataset(id_anterior[0], emocion, tendencia, coherencia, pais)
                    if resultado_update:
                        break
                print(str(ObjectId(_id)))
            return tweet_render, respuesta, '', '', [str(ObjectId(_id))],'Tweet de '+ user, ''
    
    except dash.exceptions.InvalidCallbackReturnValue as e:
        print('Error callback')
     
    
## Función para deshabilitar botón de carga de tweets

@app.callback(
    [dash.dependencies.Output('model-boton-ct', 'disabled')],

    [dash.dependencies.Input('model-emocion-ct', 'value'),
    dash.dependencies.Input('model-tendencia-ct', 'value'),
    dash.dependencies.Input('model-coherencia-ct', 'value')]
    )


def update_tweet(emocion, tendencia, coherencia):
    if ((emocion == '') or (tendencia == '') or (coherencia == '')):
        disable = True,
    else:
        disable = False,
    return disable
    


## Función para actualizar el gráfico de torta de tweets calificados

@app.callback(
    dash.dependencies.Output('model-pie', 'figure'),
    [dash.dependencies.Input('model-boton-ct', 'n_clicks'),
    dash.dependencies.Input('model-seleccion', 'value')]
    )
def update_tweet(n_clicks, pais):
    total_sin, total_tweets = get_tweet_count(pais)
    fig = go.Figure(data=[go.Pie(labels=['Clasificado','Sin Clasificar'], values=[total_tweets - total_sin, total_sin])])
    return fig

@app.callback(
    dash.dependencies.Output('model-muestra', 'children'),
    [dash.dependencies.Input('model-seleccion', 'value')]
    )
def update_tweet(pais):
    salida = "Muestra esperada:"+str((1/6)*(1-(1/6))*int(get_tweet_count(pais)[1]))
    return salida

###################################
#### Página de predicción #########
###################################

# Intervalo para mostrar tweets cada 5 segundos
@app.callback(
    [dash.dependencies.Output('prediccion-tweet', 'children'),
     dash.dependencies.Output('prediccion-emocion', 'children')],
    [dash.dependencies.Input('prediccion-interval', 'n_intervals'),
    dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_tweet_live(n, pais):
    tweet=get_random_tweet(pais)[3]
    if pais=='COL':
        emocion_num=clf_col.predict(loaded_vec_col.transform([quitar_cuentas(tweet)]))[0]
        emocion=label_emocion(emocion_num)
        return tweet, emocion
    elif pais=='ARG':
        emocion_num=clf_arg.predict(loaded_vec_arg.transform([quitar_cuentas(tweet)]))[0]
        emocion=label_emocion(emocion_num)
        return tweet, emocion

# Pie para mostrar el porcentaje de emociones frente a los tweets
@app.callback(
    dash.dependencies.Output('prediccion-pie', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    data = obtener_base(pais)
    data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_col.predict(loaded_vec_col.transform([quitar_cuentas(x)]))[0])))
    res = data.groupby('prediccion').reply_or_quote.count().reset_index()
    fig = px.pie(res, values='reply_or_quote', names='prediccion')
    return fig

## Correr el modelo de nuevo
@app.callback(
    dash.dependencies.Output('prediccion-exito-modelo', 'children'),
    [dash.dependencies.Input('prediccion-correr-modelo', 'n_clicks')])
def displayPage(n_clicks):
    if n_clicks:
        main_col()
        exito='El modelo ha sido calibrado - Recargar página por favor'
        return exito

##################################
#### Página Top temas ############
##################################


# Pie para mostrar grafica de top temas
@app.callback(
    dash.dependencies.Output('top-temas-pie', 'figure'),
    [dash.dependencies.Input('top-temas-seleccion', 'value')])
def update_top_temas(pais):
    fig = top_temas_funcion(pais)
    return fig

# Pie para mostrar grafica de evolucion de hashtags
@app.callback(
    dash.dependencies.Output('evol-hashtags-pie', 'figure'),
    [dash.dependencies.Input('top-temas-seleccion', 'value')])
def update_top_temas(pais):
    fig = evol_hastags_main(pais)
    return fig


##################################
#### Página Tendencia ############
##################################


# Grafica de tendencias
@app.callback(
    [dash.dependencies.Output('tendencia-general', 'figure'),
     dash.dependencies.Output('tendencia-user', 'figure')],
    [dash.dependencies.Input('tendencia-seleccion', 'value')])
def update_top_temas(pais):
    fig1, fig2 = top_temas_funcion(pais)
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=True)
