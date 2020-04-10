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
import random
import os
cwd = os.getcwd()

# Librería para nube de temas
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

## Importar aplicaciones
from app import app
# Paǵinas de la app
from apps import homepage, model
# Barra izquierda
from navbar import Navbar


#### Crear nube de temas del home
read='/home/davidsaw/uniandes-mongo/Grupo03/COL_tweets/find_query.json'

data = []
with open(read) as f:
    for line in f:
        data.append(json.loads(line))

temas=[]        
for i in range(len(data)):
    ht=data[i]['hashtags']
    for i in range(len(ht)):
        temas.append(ht[i]['text'])

def yellow_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 10)
        
wordcloud = WordCloud(background_color="white",width=4096, height=2160).generate(" ".join(temas))
wordcloud.recolor(color_func = yellow_color_func)
wordcloud.to_file(cwd+"/assets/images/home-nube.png")


### Base de calificacion
calificacion=pd.read_csv('/home/davidsaw/uniandes-bigdata/Taller2/export_dataframe.csv')



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
                    html.Img(src="/assets/images/co-tweet-banner.png",style={'width': '100%'}),
                    html.H2(id='titulo'),
                    html.P(id='explanation'),           
                    html.H5('Juan Camilo Cardenas'),
                    html.H6('j.cardenasc@uniandes.edu.co'),
                    html.H5('Cristian Martinez'),
                    html.H6('c.martinezb1@uniandes.edu.co'),
                    html.H5('David Ocampo'),
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
 

### Título de las páginas

@app.callback(Output('titulo','children', ),
    [Input('url', 'pathname')])
def display_title(pathname):
    if pathname == '/':
        return homepage.app.titulo
    if pathname == '/apps/model':
        return model.app.titulo

### Explicación de las páginas

@app.callback(Output('explanation','children', ),
    [Input('url', 'pathname')])
def display_explanation(pathname):
    if pathname == '/':
        return homepage.app.explanation
    if pathname == '/apps/model':
        return model.app.explanation

########################################################
########Funciones de las paǵinas########################
########################################################


### Mostrar tweets para calificar cuenta - respuesta

@app.callback(
    [dash.dependencies.Output('model-cuenta', 'children'),
    dash.dependencies.Output('model-respuesta', 'children'),
    dash.dependencies.Output('model-emocion-ct', 'value'),
    dash.dependencies.Output('model-tendencia-ct', 'value'),],
    [dash.dependencies.Input('model-boton-ct', 'n_clicks')]
    )
def update_tweet(n_clicks):
    if n_clicks>=0:
        tweet=calificacion.at[n_clicks,'tweet']
        respuesta=calificacion.at[n_clicks,'reply_and_quote']
    else:
        tweet=calificacion.at[0,'tweet']
        respuesta=calificacion.at[0,'reply_and_quote']
    return tweet , respuesta,'',''

### Mostrar tweets para calificar tweet semántica

@app.callback(
    [dash.dependencies.Output('model-tweet', 'children'),
    dash.dependencies.Output('model-emocion-t', 'value'),
    ],
    [dash.dependencies.Input('model-boton-t', 'n_clicks')]
    )
def update_tweet(n_clicks):
    if n_clicks>=0:
        tweet=calificacion.at[n_clicks,'tweet']
    else:
        tweet=calificacion.at[0,'tweet']
    return tweet ,''









if __name__ == '__main__':
    app.run_server(debug=True)
