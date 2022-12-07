
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from maindash import app, CLUSTER_MAPPINGS

# DATA =======================

df_clustered = None
def get_df_for_cluster_for_plots():
    global df_clustered
    if df_clustered is None:
        df_clustered = pd.read_csv('df_clustered.csv')
        df_clustered['cluster'] = df_clustered['cluster'].replace({v: k for k, v in CLUSTER_MAPPINGS.items()})
    return df_clustered


df_elbow = None
def get_df_for_elbow():
    global df_elbow
    if df_elbow is None:
        df_elbow = pd.read_csv('df_elbow.csv', index_col=0)
    return df_elbow


# GRAPHS ===========

def generate_cluster_histogram():
    fig = px.bar(
        get_df_for_cluster_for_plots()['cluster'].value_counts(),
        y='cluster',
        labels={'index': 'cluster', 'cluster': '#'},
        title='Histograms of clusters'
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


def generate_elbow_graph():
    fig = px.line(
        get_df_for_elbow(),
        y='wcss',
        title='Elbow method'
    )
    fig.add_vline(x=4, line_dash='dash')
    fig.update_xaxes(title='Number of clusters')
    return fig


# MAIN =============================

def build_tab_2():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H4('Methodology'),
                    dcc.Graph(id='cluster_histogram', figure=generate_cluster_histogram()),
                    dcc.Graph(id='elbow_graph', figure=generate_elbow_graph())
                ],
                width=6,
                className='p-5'
            ),
            dbc.Col(
                [
                    html.H4('3D Scatter'),
                    dcc.Graph(id='cluster_3dscatter', figure=generate_cluster_3dscatter())
                ],
                width=6,
                className='p-5'
            )
        ]
    )

