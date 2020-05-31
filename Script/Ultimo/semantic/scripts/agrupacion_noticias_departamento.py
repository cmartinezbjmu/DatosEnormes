import spacy
from spacy import displacy
from collections import Counter
import es_core_news_sm
nlp = es_core_news_sm.load()

from pymongo import MongoClient
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import json
import os

cwd = os.getcwd()
json1_file = open(cwd + '/colombia.json')
json1_str = json1_file.read()
departamentos = json.loads(json1_str)

def obtener_tweets():
    client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/")
    database = client["Grupo03"]
    collection = database["COL_tweets"]
    
    query = {}
    projection = {}
    projection["created_at"] = 1.0
    projection["user"] = 1.0
    projection["full_text"] = 1.0
    projection["hashtags"] = 1.0
    projection["id"] = 1.0
    
    cursor = collection.find(query, projection = projection)
    data = []
    hashtag = []
    try:
        for doc in cursor:
            for i in range(len(doc['hashtags'])):
                hashtag.append(doc['hashtags'][i]['text'])
            data.append([doc['id'], doc['created_at'], doc['user']['screen_name'], doc['full_text'], hashtag])
            hashtag = []
    finally:
        client.close()
    
    df = pd.DataFrame(data,columns=['id', 'created_at', 'screen_name', 'tweet', 'hastags'])
    df = df.drop_duplicates(['id'], keep='last')
    return df, data

def buscar_entidades(data):
    ciudades = []
    for tweet in range(len(data)):
        doc = nlp(data[tweet][3])
        tuplas = [(X.text, X.label_) for X in doc.ents]
        for tupla in tuplas:
            if tupla[1] == 'LOC':
                ciudades.append(tupla[0])
    return ciudades

def buscar_ciudad(city):
    for i in range(len(departamentos)):
        departamento = departamentos[i]['departamento']
        ciudades = departamentos[i]['ciudades']
        for ciudad in ciudades:
            if ciudad == city:
                departamento_salida = departamento
                break
    return departamento_salida

def crear_mapa(df):
    limits = [(0,10),(11,30),(31,80),(81,150),(151,500), (501, 2000), (2001, 5000)]
    colors = ["royalblue","crimson","rgb(0,72,186)","orange","rgb(189,215,231)", "rgb(239,222,205)", "rgb(178,132,190)"]
    cities = []
    scale = 50
    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        rango = list(range(lim[0],lim[1]))    
        df_sub = df.loc[df['Cantidad'].isin(rango)]
        fig.add_trace(go.Scattergeo(
            locationmode = 'country names',
            lon = df_sub['Longitud'],
            lat = df_sub['Latitud'],
            text = df_sub['Texto'],
            marker = dict(
                size = df_sub['Cantidad'],
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))

    fig.update_layout(
            title_text = 'Distribución de noticias por departamento',
            showlegend = True,
            geo = dict(
                scope = 'south america',
                landcolor = 'rgb(217, 217, 217)',
            )
        )
    return fig    

def generar_mapa():
    df, data = obtener_tweets()
    ciudades = buscar_entidades(data)
    diccionario = []
    for ciudad in ciudades:  
        try:
            dep = buscar_ciudad(ciudad)
            diccionario.append(dep)
        except:
            pass
    repeticiones = Counter(diccionario)
    data = pd.read_csv (r'coordenadas_colombia.csv')
    df = pd.DataFrame(data, columns= ['Departamento','Latitud','Longitud'])
    cantidad = []
    for index, row in df.iterrows():
        cantidad.append(repeticiones[row['Departamento'].strip()])
    df['Cantidad'] = cantidad
    df['Texto'] = df['Departamento'] + '<br>' + 'No. de repeticiones: ' + df['Cantidad'].astype(str)
    fig = crear_mapa(df)
    return fig