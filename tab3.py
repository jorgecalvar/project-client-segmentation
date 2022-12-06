
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

def generate_numpurchases_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='NumAllPurchases'
    )
    return fig


def generate_check_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='AverageCheck'
    )
    return fig


def generate_relationship_pie(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.pie(
        df.loc[df['cluster'] == cluster, :],
        'Relationship'
    )
    return fig

def generate_education_pie(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.pie(
        df.loc[df['cluster'] == cluster, :],
        'GradorPost'
    )
    return fig


def generate_income_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='Income'
    )
    return fig


def generate_age_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='Age'
    )
    return fig



# HELP FUNCTIONS =========================

def build_purchase_row():
    return dbc.Container(
        [
            html.H5('Purchasing Info'),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_numpurchases_boxplot(0))
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_check_boxplot(0))
                        ],
                        width=6
                    )
                ]
            )
        ],
        className='mt-4'
    )


def build_categoricalinfo_row():
    return dbc.Container(
        [
            html.H5('Categorical Info'),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_relationship_pie(0))
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_education_pie(0))
                        ],
                        width=6
                    )
                ]
            )
        ],
        className='mt-4'
    )


def build_profile_row():
    return dbc.Container(
        [
            html.H5('User profile'),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_income_boxplot(0))
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_age_boxplot(0))
                        ],
                        width=6
                    )
                ]
            )
        ],
        className='mt-4'
    )



# MAIN =============================

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
                    build_purchase_row(),
                    build_categoricalinfo_row(),
                    build_profile_row()
                ],
                width=8
            )
        ]
    )
