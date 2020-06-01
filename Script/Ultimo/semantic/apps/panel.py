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
from scripts.datos_panel import get_data as cifras_panel


app = dash.Dash(__name__)

app.titulo = "Panel de control"

app.explanation = '''
                  Desde esta página podras obtener los datos más relevantes de la
                  base de datos, así como actualizar la base de datos obteniendo 
                  más tweets, o más RSS
                  '''


app.layout =  html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Click en el botón correspondiente para obtener los datos más relevantes",
                            className="control_label",
                        ),
                        html.Button("Recolectar RSS", id="panel-rss", className='dcc_control'),
                        html.P(
                            "Seleccione el volumen de captura y click en el botón para obtener los datos más relevantes",
                            className="control_label",
                        ),
                        dcc.Slider(
                            id="panel-slider-tw",
                            min=0,
                            max=20,
                            step=0.5,
                            value=10,
                            className="dcc_control",
                        ),
                        html.Button("Recolectar tweets", id="panel-tweet", className='dcc_control'),
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
                                    [html.H6(id="panel-documentos",children= cifras_panel()[2]), html.P("No. de Documentos")],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="panel-temas",children= cifras_panel()[0]), html.P("No. de Tweets")],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="panel-fuentes",children= cifras_panel()[1]), html.P("No de Noticias")],
                                    className="mini_container",
                                ),
                                #                                 html.Div(
                                #     [html.H6(id="panel-lugares"), html.P("Lugares")],
                                #     className="mini_container",
                                # ),

                            ],
                            id="panel-info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="panel-graph",
                                       figure = go.Figure(data=[go.Pie(labels=['Tweets','Noticias'], values=[cifras_panel()[0],cifras_panel()[1]], hole=.5)])
                                       )],
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
    style={"display": "flex", "flex-direction": "column"}
)
