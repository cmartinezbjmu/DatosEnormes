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
    dcc.Tabs(id='network_tabs', children=[
        dcc.Tab(label='Red de políticos', children=[
          html.Button(id='network_politicos_button',children="Generar gráfico"),
          dcc.Graph(id='network_politicos_fig'),
          dcc.Graph(id='network_treemap_fig')]), 
        dcc.Tab(label='Relación entre políticos', children=[
          # Empezar html acá
          
          ]),
    ]),
  ])
