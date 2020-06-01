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

app.titulo = "Similitud de entidades"

app.explanation = '''Análisis de similitud entre entidades selecionadas 
                     (políticos y periodistas) consultados en DBpedia.
                  '''
app.layout = html.Div([ 
                  html.Button(id='similitud_influencers_button',children="Generar gráfico"),
                  dcc.Graph(id='similitud_influencers_fig'
                           )
])