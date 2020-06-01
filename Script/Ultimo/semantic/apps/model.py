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
from assets.pys.correlacion_temas import get_base as base_documentos

df=base_documentos()
personas=df.screen_name.value_counts().index.tolist()


app = dash.Dash(__name__)

app.titulo = "Modelos de Similitud Semántica"

app.explanation = '''
                    En la siguiente aplicación en la primera parte se puede obtener todos los temas relevantes 
                    de los que se han mencionado durante la captura de información, solamente de debe hacer CLICK
                    en el botón.
                    En la segunda gráfica es posible obtener los modelos de similitud entre documentos
                    recolectados a través de tweets y RSS, esto se puede realizar eligiendo la persona de interés
                    en la caja de personas, además es posible ajustar el nivel de similitud del modelo
                    arrastrando el slider entre más a la izquierda menos nivel de similitud por lo tanto más
                    redes, entre más a la derecha la similitud es mayor, por lo tanto se tienen menos redes. 
                    Pasando el mouse encima del nodo se puede ver el documento, al hacer click podrás ver todas las 
                    relaciones que tiene este documento
                    '''


app.layout = html.Div([
    html.Datalist(id='model-vector'),
    html.Div([
        html.H3('Distribución de temas'),
        dcc.Graph(
            id='model-pietemas'
        ),
        html.Button(id='model-buttemas',children="Calibrar Temas")
    ]),
    # html.Div([
    #     html.H3('Distribución de lugares'),
    #     dcc.Graph(
    #         id='model-pieciudades'
    #     ),
    #     html.Button(id='model-butciudades',children="Calibrar Lugares")
    # ],className='drop-izq'),
    html.H5("Seleccione la sensibilidad de la similitud"),     
    dcc.Slider(
        id='model-slider',
        min=0.25,
        max=0.50,
        step=0.01,
        value=0.35
    ),
    dcc.Tabs(children=[
        dcc.Tab(id='model-documentos',label='Documentos',children=[
            dcc.Dropdown(
                id='model-dropdown',
                options=[
                    {'label': i, 'value': i} for i in personas
                ],
            ),
            dcc.Graph(
                id='model-figura-documentos'
            ),
            html.H3("Documento:"),
            html.P(id="model-texto-documentos"),
            html.Div(id="model-texto-lista")
            
        ])
    ])
])
