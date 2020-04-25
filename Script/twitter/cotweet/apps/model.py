import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app
from index import get_random_tweet, get_tweet_count
from time import sleep
from bson.objectid import ObjectId


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

coherencia=[
    ["Si",0],
    ["No",1]
]



_id = None

while True:
    try:
        _id, user, tweet, reply_or_quote = get_random_tweet('COL')
    except TypeError as e:
        print(e)
    finally:
        if _id: 
            _id = str(ObjectId(_id))
            break

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
    html.Datalist(id='model-idtweet',
                    children=[_id]
                    ),
    html.Div([
        dcc.RadioItems(id='model-seleccion',
                options=[
                        {'label': 'Colombia', 'value': 'COL'},
                        {'label': 'Argentina', 'value': 'ARG'}
                        
                    ],
                    value = 'COL',
                    labelStyle={'display': 'inline-block'}
        )
    ]),
    dcc.Tabs([
        dcc.Tab(label='Tweet - Respuesta', children=[
            html.H4('Tweet de ' + user,id='model-user'),
            html.P(id='model-cuenta',
                   children=tweet),
            html.H4('Respuesta del tweet'),
            html.H5('Tweet para clasificar'),
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
            html.Div([
                dcc.Dropdown(
                    id='model-coherencia-ct',
                    options=[{'label': coherencia[i][0], 'value': coherencia[i][1]} for i in range(len(coherencia))],
                    placeholder="¿Es coherente la respuesta?",
                )
            ]),
            html.Button('Entrenar modelo - Siguiente tweet', id='model-boton-ct', disabled=True, n_clicks=0)
        ]),
         
	]),
    
    html.Div([
        dcc.Graph(
            id='model-pie'
        )
    ]),
    html.H1("Tamaño muestral para etiquetar"),
    html.P('''
           El tamaño muestral se determina por la probabilidad de inclusión
           de la variable en cuestión, que para el objetivo del análisis
           es la probabilidad de obtener alguna de las emociones posibles'''),
    html.H3("Sentimientos de predicción"),
    html.Ul([html.Li(x[0]) for x in emociones]),
    html.P('''
           Por lo tanto la probabilidad de inclusión de cada emoción es de 
           1/6, así, como es un muestreo en una prueba piloto se asume que 
           las variables objetivo siguen una distribución binomial, entonces, 
           es posible utilizar la fórmula para calcular el tamaño muestral óptimo
           para la calibración del modelo
           '''),
    html.Img(src='/assets/images/muestra.png'),
    html.P('''
            np : tamaño de la muestra piloto; 
            p: proporción patrón o norma de la población; 
            e: error esperado; 
            t: estadístico de distribución t
           '''),
    html.H3(id = 'mode-muestra')
    
    

])
