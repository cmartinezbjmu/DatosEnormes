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

clf_arg = load(cwd+'/assets/pys/modelo_sentimientos_arg.joblib') 
loaded_vec_arg = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_sentimientos_arg.pkl", "rb")))

clf_mix = load(cwd+'/assets/pys/modelo_sentimientos_mix.joblib') 
loaded_vec_mix = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_sentimientos_mix.pkl", "rb")))


clf_t_col = load(cwd+'/assets/pys/modelo_tendencia_col.joblib') 
loaded_vec_t_col = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_tendencia_col.pkl", "rb")))

clf_t_arg = load(cwd+'/assets/pys/modelo_tendencia_arg.joblib') 
loaded_vec_t_arg = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_tendencia_arg.pkl", "rb")))

clf_t_mix = load(cwd+'/assets/pys/modelo_tendencia_mix.joblib') 
loaded_vec_t_mix = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_tendencia_mix.pkl", "rb")))

clf_c_col = load(cwd+'/assets/pys/modelo_coherencia_col.joblib') 
loaded_vec_c_col = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_coherencia_col.pkl", "rb")))

clf_c_arg = load(cwd+'/assets/pys/modelo_coherencia_arg.joblib') 
loaded_vec_c_arg = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_coherencia_arg.pkl", "rb")))

clf_c_mix = load(cwd+'/assets/pys/modelo_coherencia_mix.joblib') 
loaded_vec_c_mix = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_coherencia_mix.pkl", "rb")))





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
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    collection_dataset = database[Pais + "_dataset"]
    data = pd.DataFrame(list(collection_dataset.find()))
    
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
    [dash.dependencies.Input('prediccion-interval', 'n_intervals')])
def update_tweet_live(n):
    paises=['COL','ARG']
    pais=paises[random.randint(0,1)]  
    tweet=get_random_tweet(pais)[3]
    if pais=='COL':
        emocion_num=int(clf_col.predict(loaded_vec_col.transform([quitar_cuentas(tweet)]))[0])
        emocion=label_emocion(emocion_num)
        return tweet, emocion
    elif pais=='ARG':
        emocion_num=int(clf_arg.predict(loaded_vec_arg.transform([quitar_cuentas(tweet)]))[0])
        emocion=label_emocion(emocion_num)
        return tweet, emocion


########## Modelo Emociones ################
# Pie para mostrar el porcentaje de emociones frente a los tweets
@app.callback(
    dash.dependencies.Output('prediccion-pie', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    if pais=='MIX':
        data_col= obtener_base('COL')
        data_arg= obtener_base('ARG')
        data=pd.concat([data_arg,data_col])
    else:
        data = obtener_base(pais)
    if pais=='COL':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_col.predict(loaded_vec_col.transform([quitar_cuentas(x)]))[0])))
    if pais=='ARG':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_arg.predict(loaded_vec_arg.transform([quitar_cuentas(x)]))[0])))
    if pais=='MIX':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_mix.predict(loaded_vec_mix.transform([quitar_cuentas(x)]))[0])))
    res = data.groupby('prediccion').reply_or_quote.count().reset_index()
    fig = px.pie(res, values='reply_or_quote', names='prediccion')
    return fig

# Pintar matriz de confusión
@app.callback(
    dash.dependencies.Output('prediccion-matriz', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    if pais=='MIX':
        data_col= obtener_base('COL')
        data_arg= obtener_base('ARG')
        data=pd.concat([data_arg,data_col])
    else:
        data = obtener_base(pais)
    if pais=='COL':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_col.predict(loaded_vec_col.transform([quitar_cuentas(x)]))[0])))
    if pais=='ARG':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_arg.predict(loaded_vec_arg.transform([quitar_cuentas(x)]))[0])))
    if pais=='MIX':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_emocion(int(clf_mix.predict(loaded_vec_mix.transform([quitar_cuentas(x)]))[0])))
    data['emocion'] = data['emocion'].apply(lambda x: label_emocion(x))
    data=data[data["emocion"]!='']
    res = data.groupby(['prediccion','emocion']).count().reset_index()
    res = res[['prediccion','emocion','id']]
    res.columns=['prediccion','emocion','clasificación']
    fig = go.Figure(data=go.Heatmap(z=res['clasificación'],x=res['emocion'],y=res['prediccion'],colorscale='Viridis'))
    return fig



## Correr el modelo de nuevo
@app.callback(
    dash.dependencies.Output('prediccion-exito-modelo', 'children'),
    [dash.dependencies.Input('prediccion-correr-modelo', 'n_clicks'),
     dash.dependencies.Input('prediccion-drop', 'value'),
     dash.dependencies.Input('prediccion-balance', 'value'),
     dash.dependencies.Input('prediccion-seleccion', 'value')])
def displayPage(n_clicks,drop,balance,pais):
    if n_clicks:
        entrenar_modelo(drop,pais,'emocion',balance)
        exito='El modelo ha sido calibrado - Recargar página por favor'
        return exito
    
    
# Box plot del mejor modelo
@app.callback(
    dash.dependencies.Output('prediccion-modelos', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def displayPage(pais):
    data_precision= mejor_modelo(pais,'emocion')
    fig = px.box(data_precision, x="model_name", y="accuracy")
    return fig



# ########## Modelo tendencia ################
# Pie para mostrar el porcentaje de emociones frente a los tweets
@app.callback(
    dash.dependencies.Output('prediccion-pie-t', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    if pais=='MIX':
        data_col= obtener_base('COL')
        data_arg= obtener_base('ARG')
        data=pd.concat([data_arg,data_col])
    else:
        data = obtener_base(pais)
    if pais=='COL':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_tendencia(int(clf_t_col.predict(loaded_vec_t_col.transform([quitar_cuentas(x)]))[0])))
    if pais=='ARG':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_tendencia(int(clf_t_arg.predict(loaded_vec_t_arg.transform([quitar_cuentas(x)]))[0])))
    if pais=='MIX':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_tendencia(int(clf_t_mix.predict(loaded_vec_t_mix.transform([quitar_cuentas(x)]))[0])))
    res = data.groupby('prediccion').reply_or_quote.count().reset_index()
    fig = px.pie(res, values='reply_or_quote', names='prediccion')
    return fig

# Pintar matriz de confusión
@app.callback(
    dash.dependencies.Output('prediccion-matriz-t', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    if pais=='MIX':
        data_col= obtener_base('COL')
        data_arg= obtener_base('ARG')
        data=pd.concat([data_arg,data_col])
    else:
        data = obtener_base(pais)
    if pais=='COL':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_tendencia(int(clf_t_col.predict(loaded_vec_t_col.transform([quitar_cuentas(x)]))[0])))
    if pais=='ARG':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_tendencia(int(clf_t_arg.predict(loaded_vec_t_arg.transform([quitar_cuentas(x)]))[0])))
    if pais=='MIX':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_tendencia(int(clf_t_mix.predict(loaded_vec_t_mix.transform([quitar_cuentas(x)]))[0])))
    data['tendencia'] = data['tendencia'].apply(lambda x: label_tendencia(x))
    data=data[data["tendencia"]!='']
    res = data.groupby(['prediccion','tendencia']).count().reset_index()
    res = res[['prediccion','tendencia','id']]
    res.columns=['prediccion','tendencia','clasificación']
    fig = go.Figure(data=go.Heatmap(z=res['clasificación'],x=res['tendencia'],y=res['prediccion'],colorscale='Viridis'))
    return fig



## Correr el modelo de nuevo
@app.callback(
    dash.dependencies.Output('prediccion-exito-modelo-t', 'children'),
    [dash.dependencies.Input('prediccion-correr-modelo-t', 'n_clicks'),
     dash.dependencies.Input('prediccion-drop-t', 'value'),
     dash.dependencies.Input('prediccion-balance-t', 'value'),
     dash.dependencies.Input('prediccion-seleccion', 'value')])
def displayPage(n_clicks,drop,balance,pais):
    if n_clicks:
        entrenar_modelo(drop,pais,'tendencia',balance)
        exito='El modelo ha sido calibrado - Recargar página por favor'
        return exito
    
    
# Box plot del mejor modelo
@app.callback(
    dash.dependencies.Output('prediccion-modelos-t', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def displayPage(pais):
    data_precision= mejor_modelo(pais,'tendencia')
    fig = px.box(data_precision, x="model_name", y="accuracy")
    return fig

############## Modelo coherencia #################################
# Pie para mostrar el porcentaje de emociones frente a los tweets
@app.callback(
    dash.dependencies.Output('prediccion-pie-c', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    if pais=='MIX':
        data_col= obtener_base('COL')
        data_arg= obtener_base('ARG')
        data=pd.concat([data_arg,data_col])
    else:
        data = obtener_base(pais)
    if pais=='COL':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_coherencia(int(clf_c_col.predict(loaded_vec_c_col.transform([quitar_cuentas(x)]))[0])))
    if pais=='ARG':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_coherencia(int(clf_c_arg.predict(loaded_vec_c_arg.transform([quitar_cuentas(x)]))[0])))
    if pais=='MIX':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_coherencia(int(clf_c_mix.predict(loaded_vec_c_mix.transform([quitar_cuentas(x)]))[0])))
    res = data.groupby('prediccion').reply_or_quote.count().reset_index()
    fig = px.pie(res, values='reply_or_quote', names='prediccion')
    return fig

# Pintar matriz de confusión
@app.callback(
    dash.dependencies.Output('prediccion-matriz-c', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def update_graph_live(pais):
    if pais=='MIX':
        data_col= obtener_base('COL')
        data_arg= obtener_base('ARG')
        data=pd.concat([data_arg,data_col])
    else:
        data = obtener_base(pais)
    if pais=='COL':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_coherencia(int(clf_c_col.predict(loaded_vec_c_col.transform([quitar_cuentas(x)]))[0])))
    if pais=='ARG':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_coherencia(int(clf_c_arg.predict(loaded_vec_c_arg.transform([quitar_cuentas(x)]))[0])))
    if pais=='MIX':
        data['prediccion'] = data['reply_or_quote'].apply(lambda x: label_coherencia(int(clf_c_mix.predict(loaded_vec_c_mix.transform([quitar_cuentas(x)]))[0])))
    data['coherencia'] = data['coherencia'].apply(lambda x: label_coherencia(x))
    data=data[data["coherencia"]!='']
    res = data.groupby(['prediccion','coherencia']).count().reset_index()
    res = res[['prediccion','coherencia','id']]
    res.columns=['prediccion','coherencia','clasificación']
    fig = go.Figure(data=go.Heatmap(z=res['clasificación'],x=res['coherencia'],y=res['prediccion'],colorscale='Viridis'))
    return fig



## Correr el modelo de nuevo
@app.callback(
    dash.dependencies.Output('prediccion-exito-modelo-c', 'children'),
    [dash.dependencies.Input('prediccion-correr-modelo-c', 'n_clicks'),
     dash.dependencies.Input('prediccion-drop-c', 'value'),
     dash.dependencies.Input('prediccion-balance-c', 'value'),
     dash.dependencies.Input('prediccion-seleccion', 'value')])
def displayPage(n_clicks,drop,balance,pais):
    if n_clicks:
        entrenar_modelo(drop,pais,'coherencia',balance)
        exito='El modelo ha sido calibrado - Recargar página por favor'
        return exito
    
    
# Box plot del mejor modelo
@app.callback(
    dash.dependencies.Output('prediccion-modelos-c', 'figure'),
    [dash.dependencies.Input('prediccion-seleccion', 'value')])
def displayPage(pais):
    data_precision= mejor_modelo(pais,'coherencia')
    fig = px.box(data_precision, x="model_name", y="accuracy")
    return fig
   

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
def update_top_evol_temas(pais):
    fig = evol_hastags_main(pais)
    return fig

# Pie para mostrar grafica de temas mencionados en noticieros
@app.callback(
    dash.dependencies.Output('noticieros-temas-pie', 'figure'),
    [dash.dependencies.Input('medios-seleccion', 'value')])
def update_top_temas(pais):
    fig = top_temas_noticieros_funcion(pais)
    return fig

##################################
#### Página Tendencia ############
##################################


# Grafica de tendencias
@app.callback(
    [dash.dependencies.Output('tendencia-general', 'figure'),
     dash.dependencies.Output('tendencia-user', 'figure')],
    [dash.dependencies.Input('tendencia-seleccion', 'value')])
def update_tendencia(pais):
    fig1, fig2 = plot_tendencia(pais)
    return fig1, fig2

##################################
#### Página Emociones ############
##################################


# Grafica de emociones
@app.callback(
    [dash.dependencies.Output('emociones-general', 'figure'),
     dash.dependencies.Output('emociones-user', 'figure'),
     dash.dependencies.Output('emociones-minsalud', 'figure')],
    [dash.dependencies.Input('emociones-seleccion', 'value')])
def update_emociones(pais):
    fig1, fig2, fig3 = plot_emociones(pais)
    return fig1, fig2, fig3

##################################
#### Página Coherencia ###########
##################################

# Grafica de coherencia
@app.callback(
    [dash.dependencies.Output('coherencia-general', 'figure'),
     dash.dependencies.Output('coherencia-user', 'figure')],
    [dash.dependencies.Input('coherencia-seleccion', 'value')])
def update_coherencia(pais):
    fig1, fig2 = plot_coherencia(pais)
    return fig1, fig2

##################################
#### Página Panel de control######
##################################

## Correr el modelo de nuevo desde el panel
@app.callback(
    dash.dependencies.Output('panel-exito', 'children'),
    [dash.dependencies.Input('panel-correr-modelo', 'n_clicks'),
     dash.dependencies.Input('panel-recolectar', 'n_clicks'),
     dash.dependencies.Input('panel-modelos', 'value'),
     dash.dependencies.Input('panel-balanceo', 'value'),
     dash.dependencies.Input('panel-seleccion', 'value'),
     dash.dependencies.Input('panel-tipo-modelo', 'value')])
def displayPage(n_clicks,n_recolectar,drop,balance,pais,tipo_modelo):
    if n_clicks:
        entrenar_modelo(drop,pais,tipo_modelo,balance)
        exito='Recargar página por favor'
        return exito
    if n_recolectar:
        recolectar_tweets(pais)
        exito='Recargar página por favor'
        return exito
    
## Correr el modelo de nuevo desde el panel
@app.callback(
    dash.dependencies.Output('panel-graph', 'figure'),
    [dash.dependencies.Input('panel-seleccion', 'value')])
def displayPage(pais):
    data = obtener_base(pais)
    res=data.groupby('user').count().reset_index()
    fig = px.bar(res, y='tweet', x='user', text='tweet', title='Respuestas por usuario')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    return fig    

## Aliementar cifras de la base de datos
@app.callback(
    [dash.dependencies.Output('panel-tweets', 'children'),
     dash.dependencies.Output('panel-cuentas', 'children'),
     dash.dependencies.Output('panel-comentarios', 'children'),
     dash.dependencies.Output('panel-citas', 'children')
     ],
    [dash.dependencies.Input('panel-seleccion', 'value')])
def displayPage(pais):
    if pais=='COL':
        total=cuenta_col()[3]
        total_inf=cuenta_col()[0]
        comentario=cuenta_col()[1]
        cita=cuenta_col()[2]
        return total,total_inf,comentario,cita
    if pais=='ARG':
        total=cuenta_arg()[3]
        total_inf=cuenta_arg()[0]
        comentario=cuenta_arg()[1]
        cita=cuenta_arg()[2]
        return total,total_inf,comentario,cita
    
    
##################################
#### Página Seguidores ###########
##################################

# Lista de usuarios
@app.callback(
    dash.dependencies.Output('seguidores-list', 'options'),    
    [dash.dependencies.Input('seguidores-seleccion', 'value')])
def update_seguidores_list(pais):    
    return [{'label':i,'value':i} for i in lista_usuarios(pais)]

# Grafica de followers
@app.callback(
    dash.dependencies.Output('seguidores-fig', 'figure'),    
    [dash.dependencies.Input('seguidores-seleccion', 'value'),
    dash.dependencies.Input('seguidores-list', 'value')])
def update_seguidores_fig(pais, user):    
    return plot_followers(pais, user)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=True)
