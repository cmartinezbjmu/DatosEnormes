import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app
# from index import get_random_tweet
from time import sleep
from bson.objectid import ObjectId


app = dash.Dash(__name__)

app.titulo = "Análisis de influencers"

app.explanation = '''Análisis de tendencias de apoyo, emociones y coherencia en
                     las interacciones de los usuarios de twitter y las cuentas
                     consideradas de importancia (influencers) para este estudio.
                    '''

app.layout = html.Div([    
    html.Div(
        dcc.Tabs(id='tabs-influencers', value='tendencias', children=[
        dcc.Tab(label='Tendencias de Apoyo', value='tendencias', children=[
            html.Div([
                dcc.RadioItems(id='tendencia-seleccion',
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
                dcc.Graph(id='tendencia-general'
                        )
            ]), 
            html.Div([
                dcc.Graph(id='tendencia-user'
                        )
            ]),    
                ]),
        dcc.Tab(label='Emociones', value='emociones', children=[
            html.Div([
            dcc.RadioItems(id='emociones-seleccion',
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
                dcc.Graph(id='emociones-general')
            ]), 
            html.Div([
                dcc.Graph(id='emociones-user')
            ]),
            html.H5('Análisis de polaridad de como se sienten los twitteros respecto al avance del virus respecto a los tweets del Ministerio de Salud'),
            html.Div([
                dcc.Graph(id='emociones-minsalud')
            ]),            
        ]),
        dcc.Tab(label='Coherencia', value='coherencia', children=[
            html.Div([
            dcc.RadioItems(id='coherencia-seleccion',
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
                dcc.Graph(id='coherencia-general')
            ]), 
            html.Div([
                dcc.Graph(id='coherencia-user')
            ]),
        ]),
    ]),
    )
])
