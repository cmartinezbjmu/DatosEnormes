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

app.titulo = "Temas"

app.explanation = '''

                    '''


app.layout = html.Div([
    html.Div([
        dcc.RadioItems(id='prediccion-seleccion',
                options=[
                        {'label': 'Colombia', 'value': 'COL'},
                        {'label': 'Argentina', 'value': 'ARG'},
                        {'label': 'Mixto', 'value': 'CA'}
                    ],
                    value='C',
                    labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        dcc.Graph(id='prediccion-pie'
                  )
    ]),
    html.Button('Calibrar modelo', id='prediccion-correr-modelo',className='drop-izq'),
    html.Div(
        dcc.Dropdown(
                    id='prediccion-drop',
                        options=[
                            {'label': 'Naive Bayes Multinomial', 'value': 'NB'},
                            {'label': 'Random Forest', 'value': 'RF'},
                            {'label': 'Regresión Logística', 'value': 'LR'},
                            {'label': 'Soporte Vectorial', 'value': 'SV'}
                        ],
                        value='NB',
                        clearable=False
        ),
    className='drop-der'),
    html.H5(id='prediccion-exito-modelo'),
    html.H4('Clasificador de tweets'),
    html.P(id='prediccion-tweet'),
    html.H5(id='prediccion-emocion'),
    dcc.Interval(
        id='prediccion-interval',
        interval=3*1000, # in milliseconds
        n_intervals=0
    )
    
    
])
