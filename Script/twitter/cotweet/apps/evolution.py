import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import re
import psycopg2
from app import app


app = dash.Dash(__name__)

app.titulo = "CREDIT CARD EVOLUTION IN COLOMBIA"

app.explanation = " The growth of the credit card coverage in Colombia has maintained a constant behavior exceeding 15 million issued cards. \
    The behavior of the canceled cards has been growing during the last year but even with this behavior we can \
    see that the default interest are controlled in lower ranges  "

app.layout = html.Div([
            
		])
