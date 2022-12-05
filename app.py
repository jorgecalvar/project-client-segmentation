
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


load_figure_template('yeti')



df_clustered = None
def get_df_for_cluster_for_plots():
    global df_clustered
    if df_clustered is None:
        df_clustered = pd.read_csv('df_clustered.csv')
    return df_clustered


def generate_cluster_histogram():
    fig = px.bar(
        get_df_for_cluster_for_plots()['cluster'].value_counts(),
        y='cluster',
        labels={'index': 'cluster', 'cluster': '#'}
    )
    return fig


def generate_cluster_3dscatter():
    fig = px.scatter_3d(
        get_df_for_cluster_for_plots(),
        x='Income',
        y='NumAllPurchases',
        z='AverageCheck',
        color='cluster'
    )
    fig.update_layout(height=800)
    return fig


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





def build_tab_2():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.B('Cluster Histogram'),
                    html.Hr(),
                    dcc.Graph(id='cluster_histogram', figure=generate_cluster_histogram())
                ],
                width=6
            ),
            dbc.Col(
                [
                    html.B('3D Scatter'),
                    html.Hr(),
                    dcc.Graph(id='cluster_3dscatter', figure=generate_cluster_3dscatter())
                ],
                width=6
            )
        ]
    )


def build_tab_3():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H4('Selection'),
                    html.P('Here, you may select the cluster that you want to explore:'),
                    html.Hr(),
                    dcc.Dropdown(['Bad', 'Good', 'Excellent', 'Elite'], 'Elite')
                ],
                width=4,
                className='p-5'
            ),
            dbc.Col(
                [

                ],
                width=8
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

