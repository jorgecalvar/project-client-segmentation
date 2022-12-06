
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from maindash import app



def build_tab_1():
    return html.Div(
        id='tab-1-content',
        children=[
            html.P("Tabasdf 1")
        ]
    )


