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

app.titulo = "Distribución de noticias o tweets en Colombia"

app.explanation = '''Análisis de la distribución de las noticias o tweets por las diferentes
                    regiones del pais. Teniendo en cuenta las menciones que hacen de las ciudades 
                    dentro de cada texto.
                    '''

app.layout = html.Div([ 
                html.Div([   
                    dcc.RadioItems(id='seleccion_data',
                                    options=[
                                            {'label': 'Tweets', 'value': 0},
                                            {'label': 'Noticias', 'value': 1}
                                        ],
                                        labelStyle={'display': 'inline-block'}
                                )
                ]),
                html.Div([
                    dcc.Graph(id='mapa_distribucion_noticias_fig')
                ])
])