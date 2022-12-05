
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from maindash import app
from tab1 import build_tab_1
from tab2 import build_tab_2
from tab3 import build_tab_3


load_figure_template('yeti')


def build_banner():
    return html.Div(
        id='banner',
        children=[
            html.H4('Cient Segmentation Project'),
            html.H5('Dash Project')
        ],
        className='p-4'
    )


def build_tabs():
    return html.Div(
        id='tabs',
        className='tabs',
        children=[
            dcc.Tabs(
                id='app-tabs',
                children=[
                    dcc.Tab(
                        id='tab-1',
                        label='EDA'
                    ),
                    dcc.Tab(
                        id='tab-2',
                        label='Clustering'
                    ),
                    dcc.Tab(
                        id='tab-3',
                        label='Explore segments'
                    )
                ]
            )
        ]
    )










app.layout = dbc.Container(
    [
        build_banner(),
        build_tabs(),
        html.Div(id='app-content')
    ],
    className='dbc',
    fluid=True
)


@app.callback(
    Output('app-content', 'children'),
    Input('app-tabs', 'value')
)
def update_tabs(tab):
    if tab == 'tab-1':
        return build_tab_1()
    elif tab == 'tab-2':
        return build_tab_2()
    elif tab == 'tab-3':
        return build_tab_3()
    else:
        raise ValueError(tab)


if __name__ == '__main__':
    app.run_server(debug=True, port=8736)

