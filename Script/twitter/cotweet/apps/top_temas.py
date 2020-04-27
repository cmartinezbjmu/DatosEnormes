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

app.explanation = '''

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
                html.Div([
                    dcc.Graph(id='evol-hashtags-pie')
                ]), 
                html.Div([
                    dcc.Graph(id='top-temas-pie')
                ]), 
            ]),
            dcc.Tab(label='Medios de comunicación', value='temas_medios', children=[
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