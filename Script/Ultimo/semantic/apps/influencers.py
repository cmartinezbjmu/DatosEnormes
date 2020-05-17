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

app.titulo = "Análisis de influencers"

app.explanation = '''Análisis de tendencias de apoyo, emociones y coherencia en
                     las interacciones de los usuarios de twitter y las cuentas
                     consideradas de importancia (influencers) para este estudio.
                    '''

app.layout = html.Div([    
])
