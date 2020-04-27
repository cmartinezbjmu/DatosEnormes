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

app.titulo = "Panel de control"

app.explanation = '''
                  Desde esta página podras obtener los datos más relevantes de la
                  base de datos, así como actualizar la base de datos obteniendo 
                  más tweets, también puedes calibrar los modelos de predicción
                  que corresponden al análisis de sentiemientos, tendencia y coherencia
                    '''


app.layout =  html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Escoja el país para obtener los datos más relevantes",
                            className="control_label",
                        ),
                        dcc.RadioItems(
                            id="panel-seleccion",
                            options=[
                                {"label": "Colombia ", "value": "COL"},
                                {"label": "Argentina ", "value": "ARG"},
                            ],
                            value="active",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Checklist(
                            id="panel-balanceo",
                            options=[{"label": "Balancear muestra", "value": 1}],
                            className="dcc_control",
                            value=[],
                        ),
                        dcc.Dropdown(
                            id="panel-tipo-modelo",
                            options=[
                                {'label': 'Modelo de Sentimientos', 'value': 'emocion'},
                                {'label': 'Modelo de Tendencia', 'value': 'tendencia'},
                                {'label': 'Modelo de coherencia', 'value': 'coherencia'},
                            ],
                            placeholder="¿Qué modelo quieres re-entrenar?",
                            clearable=False,
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="panel-modelos",
                            options=[
                                {'label': 'Naive Bayes Multinomial', 'value': 'NB'},
                                {'label': 'Random Forest', 'value': 'RF'},
                                {'label': 'Regresión Logística', 'value': 'LR'},
                                {'label': 'Soporte Vectorial', 'value': 'SV'}
                            ],
                            placeholder="Escoje el algoritmo ",
                            clearable=False,
                            className="dcc_control",
                        ),
                        html.P(
                            "Pare re - entrenar los modelos haga click en el botón",
                            className="control_label",
                        ),
                        html.Button("Calibrar modelo", id="panel-correr-modelo"),
                        html.P(
                            "Pare obtener más tweets para el estudio hace click en el botón",
                            className="control_label",
                        ),

                        html.Button("Recolectar tweets", id="panel-recolectar"),
                        html.P(
                            id='panel-exito',
                            className="control_label",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="panel-cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                ############################
                                ### Mini containers ########
                                ############################
                                
                                
                                html.Div(
                                    [html.H6(id="panel-tweets"), html.P("No. de Tweets")],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="panel-cuentas"), html.P("No. de Usuarios")],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="panel-comentarios"), html.P("Comentarios")],
                                    className="mini_container",
                                ),
                                                                html.Div(
                                    [html.H6(id="panel-citas"), html.P("Citas")],
                                    className="mini_container",
                                ),

                            ],
                            id="panel-info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="panel-count_graph")],
                            id="panel-countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="panel-right-column",
                    className="seven columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="panel-mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)
