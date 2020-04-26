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
    html.Div([
        dcc.RadioItems(id='top-temas-seleccion',
                options=[
                        {'label': 'Colombia', 'value': 'C'},
                        {'label': 'Argentina', 'value': 'A'},
                        {'label': 'Mixto', 'value': 'CA'}
                    ],
                    value='C',
                    labelStyle={'display': 'inline-block'}
        )
    ]),
    html.Div([
        dcc.Graph(id='evol-hashtags-pie'
                  )
    ]), 
    html.Div([
        dcc.Graph(id='top-temas-pie'
                  )
    ]),   
    
])