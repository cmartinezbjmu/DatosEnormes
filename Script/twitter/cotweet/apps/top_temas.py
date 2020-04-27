import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app
# from index import get_random_tweet, get_tweet_count
from time import sleep
from bson.objectid import ObjectId

app = dash.Dash(__name__)

app.titulo = "Top temas y hashtags"

app.explanation = ''' En esta página se encuentra el análisis realizado a 
                      los hashtags durante la etapa de recolección de tweets,
                      para así analizar la duración de los hashtag más comentados
                      y los temas más relevantes en la red. Por otra parte, 
                      se encuentrar los top 10 temas que sehan comentado en los tweet,
                      estos temas fueron obtenidos con el contenido de las palabras de
                      los tweets
                      

                    '''

app.layout = html.Div([ 
    html.Div(
        dcc.Tabs(id='tabs-temas', value='temas', children=[
            dcc.Tab(label='Temas y hashtags', value='temas', children=[
                html.Div([
                    dcc.RadioItems(id='top-temas-seleccion',
                        options=[
                                {'label': 'Colombia', 'value': 'COL'},
                                {'label': 'Argentina', 'value': 'ARG'},
                                {'label': 'Mixto', 'value': 'CA'}
                        ],
                        value='COL',
                        labelStyle={'display': 'inline-block'}
                    )
                ]),
                html.H4('Evolución de los hashtags más comentados en el último més'),
                html.Div([
                    dcc.Graph(id='evol-hashtags-pie')
                ]), 
                html.H4('Top 10 de los temas más comentados en el texto de los tweets'),
                html.Div([
                    dcc.Graph(id='top-temas-pie')
                ]), 
            ]),
            dcc.Tab(label='Medios de comunicación', value='temas_medios', children=[
                html.H4('Temas relacionados con medios de comunicación'),
                html.P('Observamos la relación de los temas elegidos y que son comentados por medios de comunicación'),
                html.Div([
                    dcc.RadioItems(id='medios-seleccion',
                        options=[
                                {'label': 'Colombia', 'value': 'COL'},
                                {'label': 'Argentina', 'value': 'ARG'},
                                {'label': 'Mixto', 'value': 'CA'}
                        ],
                        value='COL',
                        labelStyle={'display': 'inline-block'}
                    )
                ]),
                html.Div([
                    dcc.Graph(id='noticieros-temas-pie')
                ]), 
            ]),
        ]),
    )
])