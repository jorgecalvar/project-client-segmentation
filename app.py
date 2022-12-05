
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

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
                        id='tab-1',
                        label='EDA'
                    ),
                    dcc.Tab(
                        id='tab-2',
                        label='Customer Segments'
                    )
                ]
            )
        ]
    )


def build_tab_1():
    return html.Div(
        id='tab-1',
        children=[
            html.P("Tab 1")
        ]
    )

def build_tab_2():
    return html.Div(
        id='tab-2',
        children=[
            html.P("Tab 2")
        ]
    )


app.layout = html.Div(
    id='big-app-container',
    children=[
        build_banner(),
        build_tabs(),
        html.Div(id='app-content')
    ],
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
    else:
        raise ValueError(tab)

if __name__ == '__main__':
    app.run_server(debug=True, port=8736)

