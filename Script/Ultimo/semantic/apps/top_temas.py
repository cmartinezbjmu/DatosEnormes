import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app
from scripts.similaridad_entidades import similitud_influencers
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
                  dcc.Graph(id='similitud_influencers_fig', figure=similitud_influencers())
])