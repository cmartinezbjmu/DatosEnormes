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

emociones=[["Neutro",0],
           ["Optimista",1],
           ["Triste",2],
           ["Enojo",3],
           ["Sorprendido",4],
           ["Orgulloso",5]]


app = dash.Dash(__name__)
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
app.scripts.append_script({ 'external_url' : mathjax })


app.titulo = "Tamaño Muestral"

app.explanation = '''

                    '''


app.layout = html.Div([
    html.H1("Tamaño muestral"),
    html.P('''
           El tamaño muestral se determina por la probabilidad de inclusión
           de la variable en cuestión, que para el objetivo del análisis
           es la probabilidad de obtener alguna de las emociones posibles'''),
    html.H3("Sentimientos de predicción"),
    html.Ul([html.Li(x) for x in emociones]),
    html.Div(children=['$p=\frac{1}{20}$'])
    
    
])
