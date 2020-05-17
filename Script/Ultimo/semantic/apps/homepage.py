import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

app = dash.Dash(__name__)

app.titulo = "Taller 3"

app.explanation = ''' Análisis de la coyuntura del Covid-19 y la percepción de las
		     personas que interactuan con la red social Twitter en Colombia
		     y Argentina. La aplicación establece los principales temas, influenciadores
		     e información relevante y cómo los usuarios de la red social perciben la información
		     a traves de algoritmos de Inteligencia Artifical y herramientas de Big Data  '''

app.layout = html.Div(
    [
    ])
