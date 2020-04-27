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

app.titulo = "Modelos de predicción"

app.explanation = ''' En esta página se encuentran los resúmenes 
                      básicos de los modelos que conciernen a 
                      Sentimientos, Tendencia y Coherencia de los
                      tweet calificados, además se pueden re entrenar 
                      los modelos desde la parte inferior de la página
                      eligiendo los parámetros de tipo de modelo y que
                      tratamiento se realizará con las muestras tomadas 
                      (balancear o mantener base original)

                    '''


app.layout = html.Div([
    html.Div([
        dcc.RadioItems(id='prediccion-seleccion',
                options=[
                        {'label': 'Colombia', 'value': 'COL'},
                        {'label': 'Argentina', 'value': 'ARG'},
                        {'label': 'Mixto', 'value': 'MIX'}
                    ],
                    value='COL',
                    labelStyle={'display': 'inline-block'}
        )
    ]),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
    ####################################
    #### Tab 1 Emociones ###############
    ####################################
    
    dcc.Tab(label='Sentimientos', children=[
        html.H4('Distribución de sentimientos de los usuarios en sus comentarios o citas'),
        html.Div([
            dcc.Graph(id='prediccion-pie'
                    )
        ]),
        html.H4('Box plot de precisón según los diferentes modelos'),
        html.Div([
            dcc.Graph(
                id='prediccion-modelos'
            )
        ]),
        html.H4('Matriz de confunsión del modelo'),
        html.Div([
            dcc.Graph(
                id='prediccion-matriz'
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
        className='drop-der-test'),
        html.Div([
        dcc.RadioItems(id='prediccion-balance',
                options=[
                        {'label': 'Balanceado', 'value': 1},
                        {'label': 'Original', 'value': 0}
                    ],

                    labelStyle={'display': 'inline-block'}
        ),
        ]),
        html.H5(id='prediccion-exito-modelo'),


        ]),
    
    ####################################
    #### Tab 2 Tendencia ###############
    ####################################
    
    
    dcc.Tab(label='Tendencia', children=[
        html.H4('Distribución de tendencia de los usuarios en sus comentarios o citas'),
        html.Div([
            dcc.Graph(id='prediccion-pie-t'
                    )
        ]),
        html.H4('Box plot de precisón según los diferentes modelos'),
        html.Div([
            dcc.Graph(
                id='prediccion-modelos-t'
            )
        ]),
        html.H4('Matriz de confunsión del modelo'),
        html.Div([
            dcc.Graph(
                id='prediccion-matriz-t'
            )
        ]),
        html.Button('Calibrar modelo', id='prediccion-correr-modelo-t',className='drop-izq'),
        html.Div(
            dcc.Dropdown(
                        id='prediccion-drop-t',
                            options=[
                                {'label': 'Naive Bayes Multinomial', 'value': 'NB'},
                                {'label': 'Random Forest', 'value': 'RF'},
                                {'label': 'Regresión Logística', 'value': 'LR'},
                                {'label': 'Soporte Vectorial', 'value': 'SV'}
                            ],
                            value='NB',
                            clearable=False
            ),
        className='drop-der-test'),
        html.Div([
        dcc.RadioItems(id='prediccion-balance-t',
                options=[
                        {'label': 'Balanceado', 'value': 1},
                        {'label': 'Original', 'value': 0}
                    ],

                    labelStyle={'display': 'inline-block'}
        ),
        ]),
        html.H5(id='prediccion-exito-modelo-t'), 
        
        ]),
    ####################################
    #### Tab 3 Coherencia ##############
    ####################################
    
    dcc.Tab(label='Coherencia', children=[
        html.H4('Distribución de coherencia de los usuarios en sus comentarios o citas'),
        html.Div([
            dcc.Graph(id='prediccion-pie-c'
                    )
        ]),
        html.H4('Box plot de precisón según los diferentes modelos'),
        html.Div([
            dcc.Graph(
                id='prediccion-modelos-c'
            )
        ]),
        html.H4('Matriz de confunsión del modelo'),
        html.Div([
            dcc.Graph(
                id='prediccion-matriz-c'
            )
        ]),
        html.Button('Calibrar modelo', id='prediccion-correr-modelo-c',className='drop-izq'),
        html.Div(
            dcc.Dropdown(
                        id='prediccion-drop-c',
                            options=[
                                {'label': 'Naive Bayes Multinomial', 'value': 'NB'},
                                {'label': 'Random Forest', 'value': 'RF'},
                                {'label': 'Regresión Logística', 'value': 'LR'},
                                {'label': 'Soporte Vectorial', 'value': 'SV'}
                            ],
                            value='NB',
                            clearable=False
            ),
        className='drop-der-test'),
        html.Div([
        dcc.RadioItems(id='prediccion-balance-c',
                options=[
                        {'label': 'Balanceado', 'value': 1},
                        {'label': 'Original', 'value': 0}
                    ],

                    labelStyle={'display': 'inline-block'}
        ),
        ]),
        html.H5(id='prediccion-exito-modelo-c'), 
        
    ])
    ])
])
