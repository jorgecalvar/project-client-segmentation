
import dash
from dash import html, dcc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = 'Client Segmentation Dashboard'


def build_banner():
    return html.Div(
        id='banner',
        children=[
            html.H4('Cient Segmentation Project'),
            html.H5('Dash Project')
        ]
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
                        id='eda-tab',
                        label='EDA'
                    ),
                    dcc.Tab(
                        id='clustering-tab',
                        label='Customer Segments'
                    )
                ]
            )
        ]
    )


app.layout = html.Div(
    id='big-app-container',
    children=[
        build_banner(),
        build_tabs()
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8736)