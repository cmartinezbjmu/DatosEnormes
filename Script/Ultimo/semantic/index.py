import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash_table
from sqlalchemy import create_engine
import plotly.express as px
import re
import json
import os
from pymongo import MongoClient, errors
from random import randint
from bson.objectid import ObjectId
from time import sleep
from PIL import Image
from assets.pys.read_rss import  main as read_rss
from assets.pys.modelo_tweet import quitar_cuentas
from sklearn.feature_extraction.text import CountVectorizer
from scripts.grafica_por_partido_politico import crear_network_map
from scripts.treemap_politico import crear_figura_treemap_network
from scripts.agrupacion_noticias_departamento import generar_mapa
from joblib import dump, load
import pickle
import random

cwd = os.getcwd()

# Librería para nube de temas
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

## Importar aplicaciones
from app import app
# Paǵinas de la app
from apps import homepage, model, prediccion, top_temas, influencers, panel
# Barra izquierda
from navbar import Navbar



# Relizar consultas a la base de datos

from pymongo import MongoClient
import pandas as pd
import random


client = MongoClient("mongodb://bigdata-mongodb-04.virtual.uniandes.edu.co:8087/", retryWrites=False)
database = client["Grupo03"]
## Cargar modelo de predicción
#Emociones
# clf_col = load(cwd+'/assets/pys/modelo_sentimientos_col.joblib') 
# loaded_vec_col = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(cwd+"/assets/pys/vocabulario_sentimientos_col.pkl", "rb")))


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config['suppress_callback_exceptions'] = True

nav = Navbar()
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(
        [
            html.Div(
                [
                    html.Img(src="/assets/images/Semantic-banner.png",style={'width': '100%'}),
                    html.H2(id='titulo'),
                    html.P(id='explanation'),           
                    html.H6('Juan Camilo Cardenas'),
                    html.H6('j.cardenasc@uniandes.edu.co'),
                    html.H6('Cristian Martinez'),
                    html.H6('c.martinezb1@uniandes.edu.co'),
                    html.H6('David Ocampo'),
                    html.H6('d.ocampo@uniandes.edu.co'),
                ],
                className="div_izq_home",
            ),
            html.Div(
                [
                    html.Div(id='page-content')
                ],
                className="div_der_home",
            )
        ],
    ),   
])



### Layout de las páginas

@app.callback(Output('page-content','children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return homepage.app.layout
    if pathname == '/apps/model':
        return model.app.layout
    if pathname == '/apps/analisis':
        return influencers.app.layout
    if pathname == '/apps/prediccion':
        return prediccion.app.layout
    if pathname == '/apps/top_temas':
        return top_temas.app.layout
    if pathname == '/apps/panel':
        return panel.app.layout

### Título de las páginas

@app.callback(Output('titulo','children', ),
    [Input('url', 'pathname')])
def display_title(pathname):
    if pathname == '/':
        return homepage.app.titulo
    if pathname == '/apps/model':
        return model.app.titulo
    if pathname == '/apps/analisis':
        return influencers.app.titulo
    if pathname == '/apps/prediccion':
        return prediccion.app.titulo    
    if pathname == '/apps/top_temas':
        return top_temas.app.titulo
    if pathname == '/apps/panel':
        return panel.app.titulo

### Explicación de las páginas

@app.callback(Output('explanation','children', ),
    [Input('url', 'pathname')])
def display_explanation(pathname):
    if pathname == '/':
        return homepage.app.explanation
    if pathname == '/apps/model':
        return model.app.explanation
    if pathname == '/apps/analisis':
        return influencers.app.explanation
    if pathname == '/apps/prediccion':
        return prediccion.app.explanation    
    if pathname == '/apps/top_temas':
        return top_temas.app.explanation
    if pathname == '/apps/panel':
        return panel.app.explanation
########################################################
########Funciones de las paǵinas########################
########################################################

##############################
##### Panel de control #######
##############################


############
# Botón RSS

@app.callback(
    dash.dependencies.Output('panel-exito', 'children'),
    [dash.dependencies.Input('panel-rss', 'n_clicks'),
     dash.dependencies.Input('panel-tweets', 'n_clicks')])
def displayPage(n_rss,n_recolectar,drop,balance,pais,tipo_modelo):
    if n_rss:
        read_rss()
        exito='Recargar página por favor'
        return exito
    if n_recolectar:
        recolectar_tweets(pais)
        exito='Recargar página por favor'
        return exito


##########################################
# Network politicos completo

@app.callback(
    dash.dependencies.Output('network_politicos_fig', 'figure'),
    [dash.dependencies.Input('network_politicos_button', 'n_clicks')]
)
def network_politicos_figura(n_clicks):
    if n_clicks:
        politicos = ["Gustavo_Petro", "Sergio_Fajardo", "Álvaro_Uribe", "Armando_Benedetti", "Juan_Fernando_Cristo", "Luis_Fernando_Velasco",
            "Germán_Navas_Talero", "Angélica_Lozano", "Roy_Barreras", "Gustavo_Bolívar",
            "María_José_Pizarro", "Jorge_Enrique_Robledo", "Iván_Duque_Márquez", "Claudia_López_Hernández",
            "Jorge_Iván_Ospina", "Daniel_Quintero"]
        fig = crear_network_map(politicos)
        return fig

# Treemap politico

@app.callback(
    dash.dependencies.Output('network_treemap_fig', 'figure'),
    [dash.dependencies.Input('network_politicos_fig', 'clickData')]
)
def network_politicos_seleccion(clickData):
    points=json.dumps(clickData, indent=2)
    texto=json.loads(points)["points"][0]["text"]
    fig = crear_figura_treemap_network(texto)
    return fig
    
##########################################
# Network politico

@app.callback(
    dash.dependencies.Output('network_politico_fig', 'figure'),
    [dash.dependencies.Input('ddown_politicos_1', 'value'),
    dash.dependencies.Input('ddown_politicos_2', 'value')]
)
def network_politicos_figura(select1, select2):
    if (select1 != '') and (select2 != ''):
        politicos = [select1, select2]
        fig = crear_network_map(politicos)
        return fig

# Treemap politico

@app.callback(
    dash.dependencies.Output('politico_network_treemap_fig', 'figure'),
    [dash.dependencies.Input('network_politico_fig', 'clickData')]
)
def network_politicos_seleccion(clickData):
    points=json.dumps(clickData, indent=2)
    texto=json.loads(points)["points"][0]["text"]
    fig = crear_figura_treemap_network(texto)
    return fig

##########################################
# Distribucion noticias por departamento

@app.callback(
    dash.dependencies.Output('network_politico_fig', 'figure'),
    [dash.dependencies.Input('ddown_politicos_1', 'value'),
    dash.dependencies.Input('ddown_politicos_2', 'value')]
)
def network_politicos_figura(select1, select2):
    if (select1 != '') and (select2 != ''):
        politicos = [select1, select2]
        fig = crear_network_map(politicos)
        return fig 

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8000, debug=True)
