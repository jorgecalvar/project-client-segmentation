
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

def get_df_by_cluster_for_plots(cluster):
    df = get_df_for_cluster_for_plots()
    if cluster is not None:
        return df.loc[df['cluster'].apply(lambda x: x in cluster), :]
    else:
        return df


df_for_radar = None
def get_df_for_radar(clusters):
    global df_for_radar
    selected_columns = ['NumAllPurchases', 'AverageCheck', 'Income', 'Age', 'days_enrolled']
    df = get_df_by_cluster_for_plots(clusters)
    df2 = df.loc[:, selected_columns+['cluster']]
    for c in selected_columns:
        min_value = df2[c].min()
        max_value = df2[c].max()
        df2[c] = (df2[c]-min_value)/(max_value-min_value)*10
    df3 = df2.groupby('cluster').mean().reset_index()
    df_for_radar = pd.melt(
        df3,
        id_vars=['cluster']
    )
    return df_for_radar


# GRAPHS ===========

def generate_numpurchases_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)
    fig = px.box(
        df,
        x='cluster',
        y='NumAllPurchases',
        title='Number of purchases'
    )
    fig.update_yaxes(title='')
    return fig


def generate_check_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)
    fig = px.box(
        df,
        x='cluster',
        y='AverageCheck',
        title='Average check'
    )
    fig.update_yaxes(title='')
    return fig


def generate_relationship_pie(cluster):
    df = get_df_by_cluster_for_plots(cluster)
    fig = px.pie(
        df,
        'Relationship',
        title='Relationship status'
    )
    return fig

def generate_education_pie(cluster):
    df = get_df_by_cluster_for_plots(cluster)
    fig = px.pie(
        df,
        'GradorPost',
        title='Education'
    )
    return fig


def generate_income_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)
    fig = px.box(
        df,
        x='cluster',
        y='Income',
        title='Income'
    )
    fig.update_yaxes(title='')
    return fig


def generate_age_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)
    fig = px.box(
        df,
        x='cluster',
        y='Age',
        title='Age'
    )
    fig.update_yaxes(title='')
    return fig


def generate_radar(clusters):
    df = get_df_for_radar(clusters)
    fig = px.line_polar(
        df,
        theta='variable',
        r='value',
        color='cluster',
        line_close=True
    )
    fig.update_traces(fill='toself')
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
                    dcc.Dropdown(
                        id='cluster-select',
                        options=list(CLUSTER_MAPPINGS.keys()),
                        value='Elite',
                        multi=True
                    ),
                    html.Hr(),
                    dcc.Graph(id='radar-graph')
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

def process_cluster_input(cluster):
    if type(cluster) != list:
        return [cluster]
    return cluster


def create_callbacks_for_tab3():

    #Radar Plot
    @app.callback(
        Output('radar-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_radar_graph(cluster):
        return generate_radar(process_cluster_input(cluster))

    @app.callback(
        Output('numpurchases-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_numpurchases_graph(cluster):
        return generate_numpurchases_boxplot(process_cluster_input(cluster))


    @app.callback(
        Output('check-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_check_graph(cluster):
        return generate_check_boxplot(process_cluster_input(cluster))


    @app.callback(
        Output('relationship-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_relationship_graph(cluster):
        return generate_relationship_pie(process_cluster_input(cluster))

    @app.callback(
        Output('education-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_education_graph(cluster):
        return generate_education_pie(process_cluster_input(cluster))

    @app.callback(
        Output('income-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_income_graph(cluster):
        return generate_income_boxplot(process_cluster_input(cluster))

    @app.callback(
        Output('age-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_age_graph(cluster):
        return generate_age_boxplot(process_cluster_input(cluster))
        






