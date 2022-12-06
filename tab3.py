
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from maindash import app

CLUSTER_MAPPINGS = {
    'Elite': 1,
    'High Potential': 2,
    'Low Old': 0,
    'Low Recent': 3
}

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
        y='NumAllPurchases',
        title='Number of purchases'
    )
    fig.update_yaxes(title='')
    return fig


def generate_check_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='AverageCheck',
        title='Average check'
    )
    fig.update_yaxes(title='')
    return fig


def generate_relationship_pie(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.pie(
        df.loc[df['cluster'] == cluster, :],
        'Relationship',
        title='Relationship status'
    )
    return fig

def generate_education_pie(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.pie(
        df.loc[df['cluster'] == cluster, :],
        'GradorPost',
        title='Education'
    )
    return fig


def generate_income_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='Income',
        title='Income'
    )
    fig.update_yaxes(title='')
    return fig


def generate_age_boxplot(cluster):
    df = get_df_for_cluster_for_plots()
    fig = px.box(
        df.loc[df['cluster'] == cluster, :],
        y='Age',
        title='Age'
    )
    fig.update_yaxes(title='')
    return fig



# HELP FUNCTIONS =========================

def build_purchase_row():
    return dbc.Container(
        [
            html.H5('Customer profile'),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id='numpurchases-graph')
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id='check-graph')
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
                            dcc.Graph(id='relationship-graph')
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id='education-graph')
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
                            dcc.Graph(id='income-graph')
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(id='age-graph')
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
                    html.H3(' Cluster Selection'),
                    html.P('Here, you may select the customer segment that you want to explore:'),
                    html.Hr(),
                    dcc.Dropdown(
                        id='cluster-select',
                        options=list(CLUSTER_MAPPINGS.keys()),
                        value='Elite'
                    )
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


# CALLBACKS ===================================

def create_callbacks_for_tab3():
    @app.callback(
        Output('numpurchases-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_numpurchases_graph(cluster):
        return generate_numpurchases_boxplot(CLUSTER_MAPPINGS[cluster])


    @app.callback(
        Output('check-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_check_graph(cluster):
        return generate_check_boxplot(CLUSTER_MAPPINGS[cluster])


    @app.callback(
        Output('relationship-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_relationship_graph(cluster):
        return generate_relationship_pie(CLUSTER_MAPPINGS[cluster])

    @app.callback(
        Output('education-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_education_graph(cluster):
        return generate_education_pie(CLUSTER_MAPPINGS[cluster])

    @app.callback(
        Output('income-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_income_graph(cluster):
        return generate_income_boxplot(CLUSTER_MAPPINGS[cluster])

    @app.callback(
        Output('age-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_age_graph(cluster):
        return generate_age_boxplot(CLUSTER_MAPPINGS[cluster])
        






