
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from maindash import app, CLUSTER_MAPPINGS, CLUSTER_COLORS, CLUSTER_ORDER

# DATA =======================

df_clustered = None
def get_df_for_cluster_for_plots():
    global df_clustered
    if df_clustered is None:
        df_clustered = pd.read_csv('data/df_clustered.csv')
        df_clustered['cluster'] = df_clustered['cluster'].replace({v: k for k, v in CLUSTER_MAPPINGS.items()})
        df_clustered = df_clustered.sort_values('cluster', key=lambda s: s.apply(lambda x: CLUSTER_ORDER.index(x)))
    return df_clustered


df_elbow = None
def get_df_for_elbow():
    global df_elbow
    if df_elbow is None:
        df_elbow = pd.read_csv('data/df_elbow.csv', index_col=0)
    return df_elbow


# GRAPHS ===========

df_for_hist = None
def generate_cluster_histogram():
    global df_for_hist
    if df_for_hist is None:
        df_for_hist = get_df_for_cluster_for_plots().copy().loc[:, ['cluster']]
        df_for_hist.loc[:, 'count'] = 1
        df_for_hist = df_for_hist.groupby('cluster').count().reset_index()
        df_for_hist = df_for_hist.sort_values('cluster', key=lambda s: s.apply(lambda x: CLUSTER_ORDER.index(x)))

    fig = px.bar(
        df_for_hist,
        y='cluster',
        x='count',
        color='cluster',
        labels={'index': 'cluster', 'cluster': '#'},
        title='Histograms of clusters',
        color_discrete_sequence=CLUSTER_COLORS,
        orientation='h'
    )
    fig.update_layout(showlegend=False)
    return fig


def generate_cluster_3dscatter():
    fig = px.scatter_3d(
        get_df_for_cluster_for_plots(),
        x='Income',
        y='NumAllPurchases',
        z='AverageCheck',
        color='cluster',
        color_discrete_sequence=CLUSTER_COLORS
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
                    dcc.Graph(id='cluster_histogram', figure=generate_cluster_histogram()),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(id='elbow_graph', figure=generate_elbow_graph())
                ],
                width=6,
                className='p-5'
            ),
            dbc.Col(
                [
                    html.H4('Methodology'),
                    html.P('To create the customer segments, we have finally decided to use KMeans. Results with other '
                           'models (such as agglomerative clustering) were very similar. Instead of passing all the '
                           'variables to the model, we have created a few very meaningful variables and used only those '
                           'to create the segments.'),
                    dcc.Graph(id='cluster_3dscatter', figure=generate_cluster_3dscatter())
                ],
                width=6,
                className='p-5'
            )
        ]
    )

