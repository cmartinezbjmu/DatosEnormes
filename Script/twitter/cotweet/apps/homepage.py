import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

app = dash.Dash(__name__)

app.titulo = "Taller 2"

app.explanation = ''' Análisis de la coyuntura del Covid-19 y la percepción de las
		     personas que interactuan con la red social Twitter en Colombia
		     y Argentina. La aplicación establece los principales temas, influenciadores
		     e información relevante y cómo los usuarios de la red social perciben la información
		     a traves de algoritmos de Inteligencia Artifical y herramientas de Big Data  '''

app.layout = html.Div(
    [
        html.H2('Temas relacionados con el Covid-19'),
        html.P('Nube de palabras con los Hashtags que se trinaron durante la toma de los datos'),
        html.Iframe(src="https://twitframe.com/show?url=https://twitter.com/ValentinaO3009/status/1247718893109628928",
                        style={'width':'100%',
                               'height': 'auto'
                               } 
                    ),
        html.Img(src="/assets/images/home-nube.png")
    ]
    )
