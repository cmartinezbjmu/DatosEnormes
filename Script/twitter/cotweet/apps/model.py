import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app
from index import get_random_tweet
from time import sleep


emociones=[["Neutro",0],
           ["Optimista",1],
           ["Triste",2],
           ["Enojo",3],
           ["Sorprendido",4],
           ["Orgulloso",5]]


tendencia=[
    ["Apoyo",0],
    ["Contradicción",1],
    ["Matoneo",2] 
]
while 1:
    try:
        _id, user, tweet, reply_or_quote = get_random_tweet()
        break
    except TypeError as e:
        sleep(5)
        continue


app = dash.Dash(__name__)

app.titulo = "Entrenamiento del modelo"

app.explanation = '''
                    En la siguiente aplicación podrás darnos tus opiniones y ayudar a entrenar el modelo de inteligencia artificial
                    con el cual se puede predecir la percepción de las personas respecto a los tweets más sonados en estos momentos.
                    En la primera pestaña de la página (TWEET - RESPUESTA) encuentras los tweets que personas influyentes de
                    Colombia y Argentina escriben y las respuestas que tienen de sus seguidores en tweeter.
                    En la segunda (TWEET) encontrarás los tweets de las personas influyentes de cada país, para así,
                    poder dar tu opinión acerca de la percepción emocional que tienes respecto a lo que se escribe.
                    Selecciona en los menús desplegables tu percepción acerca de los tweets y dale click al botón para obtener
                    mas tweets. ¡GRACIAS POR TU APOYO!
                    '''


app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Tweet - Respuesta', children=[
            html.H4('Tweet de ' + user),
            html.P(id='model-cuenta',
                   children=tweet),
            html.H4('Respuesta del tweet'),
            html.H6('Tweet para clasificar'),
            html.P(id='model-respuesta',
                   children=reply_or_quote),
            html.Div([
                dcc.Dropdown(
                    id='model-emocion-ct',
                    options=[{'label': emociones[i][0], 'value': emociones[i][1]} for i in range(len(emociones))],
                    placeholder="¿Qué sientes con el tweet?",
                )
            ]),
            html.Div([
                dcc.Dropdown(
                    id='model-tendencia-ct',
                    options=[{'label': tendencia[i][0], 'value': tendencia[i][1]} for i in range(len(tendencia))],
                    placeholder="¿Qué posición tiene la respuesta?",
                )
            ]),
            html.Button('Entrenar modelo - Siguiente tweet', id='model-boton-ct', disabled=True, n_clicks=0)
        ]),
         dcc.Tab(label='Tweet', children=[
            html.H4('Tweet'),
            html.P(id='model-tweet',
                   children=""),
            html.Div([
                dcc.Dropdown(
                    id='model-emocion-t',
                    options=[{'label': emociones[i][0], 'value': emociones[i][1]} for i in range(len(emociones))],
                    placeholder="¿Qué sientes con el tweet?",
                )
            ]),
            html.Button('Entrenar modelo - Siguiente tweet', id='model-boton-t', n_clicks=0)
        ]),
	])
])
