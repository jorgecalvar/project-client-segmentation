
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

import pandas as pd

from maindash import app, CLUSTER_MAPPINGS, CLUSTER_ORDER, CLUSTER_COLORS_MAP



# DATA =======================

df_clustered = None
def get_df_for_cluster_for_plots():
    global df_clustered
    if df_clustered is None:
        df_clustered = pd.read_csv('data/df_clustered.csv')
        df_clustered['cluster'] = df_clustered['cluster'].replace({v: k for k, v in CLUSTER_MAPPINGS.items()})
        df_clustered = df_clustered.sort_values('cluster', key=lambda s: s.apply(lambda x: CLUSTER_ORDER.index(x)))
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
    column_pretty_mapping = {
        'NumAllPurchases': '# Purchases',
        'AverageCheck': 'Avg check',
        'Income': 'Income',
        'Age': 'Age',
        'days_enrolled': 'Days enrolled'
    }
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
    df_for_radar['variable'] = df_for_radar['variable'].replace(column_pretty_mapping)
    return df_for_radar


# GRAPHS ===========

def generate_numpurchases_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)

    labels = df['cluster'].unique()
    hist_data = []
    for cluster in labels:
        hist_data.append(list(df.loc[df['cluster'] == cluster, 'NumAllPurchases']))
    fig = ff.create_distplot(hist_data, labels, show_hist=False, colors=[CLUSTER_COLORS_MAP[x] for x in labels])
    fig.update_layout(title='Number of purchases', showlegend=False)
    fig.update_traces(fill='toself')

    """
    fig = px.box(
        df,
        x='cluster',
        y='NumAllPurchases',
        title='Number of purchases',
        color_discrete_map=CLUSTER_COLORS_MAP
    )
    fig.update_yaxes(title='')
    """

    return fig


def generate_check_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)

    labels = df['cluster'].unique()
    hist_data = []
    for cluster in labels:
        hist_data.append(list(df.loc[df['cluster'] == cluster, 'AverageCheck']))
    fig = ff.create_distplot(hist_data, labels, show_hist=False, colors=[CLUSTER_COLORS_MAP[x] for x in labels])
    fig.update_layout(title='Average check', showlegend=False)
    fig.update_traces(fill='toself')

    """
    fig = px.box(
        df,
        x='cluster',
        y='AverageCheck',
        title='Average check',
        color='cluster',
        color_discrete_map=CLUSTER_COLORS_MAP
    )
    fig.update_yaxes(title='')
    """
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

    labels = df['cluster'].unique()
    hist_data = []
    for cluster in labels:
        hist_data.append(list(df.loc[df['cluster'] == cluster, 'Income']))
    fig = ff.create_distplot(hist_data, labels, show_hist=False, colors=[CLUSTER_COLORS_MAP[x] for x in labels])
    fig.update_layout(title='Income', showlegend=False)
    fig.update_traces(fill='toself')

    """
    fig = px.box(
        df,
        x='cluster',
        y='Income',
        title='Income',
        color_discrete_map=CLUSTER_COLORS_MAP
    )
    fig.update_yaxes(title='')
    """

    return fig


def generate_age_boxplot(cluster):
    df = get_df_by_cluster_for_plots(cluster)

    labels = df['cluster'].unique()
    hist_data = []
    for cluster in labels:
        hist_data.append(list(df.loc[df['cluster'] == cluster, 'Age']))
    fig = ff.create_distplot(hist_data, labels, show_hist=False, colors=[CLUSTER_COLORS_MAP[x] for x in labels])
    fig.update_layout(title='Age', showlegend=False)
    fig.update_traces(fill='toself')


    """
    fig = px.box(
        df,
        x='cluster',
        y='Age',
        title='Age',
        color_discrete_map=CLUSTER_COLORS_MAP
    )
    fig.update_yaxes(title='')
    """
    return fig


def generate_days_graph(clusters):
    df = get_df_by_cluster_for_plots(clusters)

    labels = df['cluster'].unique()
    hist_data = []
    for cluster in labels:
        hist_data.append(list(df.loc[df['cluster'] == cluster, 'days_enrolled']))
    fig = ff.create_distplot(hist_data, labels, show_hist=False, colors=[CLUSTER_COLORS_MAP[x] for x in labels])
    fig.update_layout(title='Days enrolled', showlegend=False)
    fig.update_traces(fill='toself')

    return fig



def generate_radar(clusters):
    df = get_df_for_radar(clusters)
    fig = px.line_polar(
        df,
        theta='variable',
        r='value',
        color='cluster',
        line_close=True,
        color_discrete_map=CLUSTER_COLORS_MAP
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

def generate_cluster_cards():
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(
                                    [
                                        html.H4(html.B('Elite')), html.Br(),
                                        'The most valuable customers. They spend a lot and many times.'
                                    ],
                                )
                            ]
                        ),
                        className='bg-primary text-white translate-middle start-50 top-50',
                        style={'width': '80%', 'height': '100%'}
                    ),
                ],
                width=3,
                className='px-3'
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(
                                    [
                                        html.H4(html.B('High Potential')), html.Br(),
                                        'The second most valuable segment. They buy a lot of times, but they have the capability to spend more.'
                                    ],
                                )
                            ]
                        ),
                        className='bg-primary text-white translate-middle start-50 top-50',
                        style={'width': '80%', 'height': '100%'}
                    ),
                ],
                width=3,
                className='px-3'
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(
                                    [
                                        html.H4(html.B('Low Recent')), html.Br(),
                                        'They are recent customers who do not spend much, as they are young and do not have money.'
                                    ],
                                )
                            ]
                        ),
                        className='bg-primary text-white translate-middle start-50 top-50',
                        style={'width': '80%', 'height': '100%'}
                    ),
                ],
                width=3,
                className='px-3'
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(
                                    [
                                        html.H4(html.B('Low Old')), html.Br(),
                                        'Despite being long-time customers, their value has not increased.'
                                    ],
                                )
                            ]
                        ),
                        className='bg-primary text-white translate-middle start-50 top-50',
                        style={'width': '80%', 'height': '100%'}
                    ),
                ],
                width=3,
                className='px-3'
            ),
        ]
    )



# MAIN =============================

def build_tab_3():
    return html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(' Cluster Selection'),
                        html.P('Here, you may select the customer segment that you want to explore:'),
                        dcc.Dropdown(
                            id='cluster-select',
                            options=list(CLUSTER_MAPPINGS.keys()),
                            value=['Elite', 'High Potential'],
                            multi=True
                        )
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        generate_cluster_cards()
                    ],
                    width=8
                )
            ],
            className='p-5'
        ),
        html.Hr(className='mx-3'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='radar-graph')
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='numpurchases-graph')
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='check-graph')
                    ],
                    width=4
                ),
            ],
            className='p-5'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='days-graph')
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='income-graph')
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='age-graph')
                    ],
                    width=4
                ),
            ],
            className='px-5 pb-5'
        ),
    ])




# CALLBACKS ===================================

def process_cluster_input(cluster):
    if type(cluster) != list:
        return [cluster]
    return cluster


def create_callbacks_for_tab3():

    @app.callback(
        Output('radar-graph', 'figure'),
        Output('numpurchases-graph', 'figure'),
        Output('check-graph', 'figure'),
        #Output('relationship-graph', 'figure'),
        #Output('education-graph', 'figure'),
        Output('income-graph', 'figure'),
        Output('days-graph', 'figure'),
        Output('age-graph', 'figure'),
        Input('cluster-select', 'value')
    )
    def update_graphs(cluster):
        processed_cluster = process_cluster_input(cluster)
        if not cluster:
            return (px.scatter(title='Enter at east one cluster to display...'),)*6
        return (generate_radar(processed_cluster),
                generate_numpurchases_boxplot(processed_cluster),
                generate_check_boxplot(processed_cluster),
                # generate_relationship_pie(processed_cluster),
                # generate_education_pie(processed_cluster),
                generate_income_boxplot(processed_cluster),
                generate_days_graph(processed_cluster),
                generate_age_boxplot(processed_cluster))

    """
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
        
    """


