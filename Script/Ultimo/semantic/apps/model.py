import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app
from time import sleep
from bson.objectid import ObjectId



app = dash.Dash(__name__)

app.titulo = "Modelos de Similitud Semántica"

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
    html.Div([
        html.H3('Distribución de lugares'),
        dcc.Graph(
            id='model-pietemas',
        ),
        html.Button(id='model-buttemas',children="Calibrar Lugares")
    ],className='drop-der-test'),
    html.Div([
        html.H3('Distribución de lugares'),
        dcc.Graph(
            id='model-pieciudades'
        ),
        html.Button(id='model-butciudades',children="Calibrar Lugares")
    ],className='drop-izq'),    
    

])
