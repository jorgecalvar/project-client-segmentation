
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from maindash import app

# DATA =======================

df_clustered = None
def get_df_for_cluster_for_plots():
    global df_clustered
    if df_clustered is None:
        df_clustered = pd.read_csv('df_clustered.csv')
    return df_clustered


# GRAPHS ===========

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


# MAIN =============================

def build_tab_2():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.B('Cluster Histogram'),
                    html.Hr(),
                    dcc.Graph(id='cluster_histogram', figure=generate_cluster_histogram())
                ],
                width=6,
                className='p-5'
            ),
            dbc.Col(
                [
                    html.B('3D Scatter'),
                    html.Hr(),
                    dcc.Graph(id='cluster_3dscatter', figure=generate_cluster_3dscatter())
                ],
                width=6,
                className='p-5'
            )
        ]
    )

