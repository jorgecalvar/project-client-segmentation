
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import pickle

import numpy as np
from pathlib import Path

from maindash import app, CLUSTER_MAPPINGS


# DATA =======================

df_clustered = None
def get_df_for_cluster_for_plots():
    global df_clustered
    if df_clustered is None:
        df_clustered = pd.read_csv('data/df_clustered_all.csv')
    return df_clustered


df_for_products = None
def get_df_for_products():
    global df_for_products
    if df_for_products is None:
        df = get_df_for_cluster_for_plots()
        df = df.loc[:, ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds', 'cluster']]
        df_melted = pd.melt(
            df,
            id_vars=['cluster']
        )
        final_df = df_melted.groupby(['cluster', 'variable']).mean().reset_index()
        final_df['cluster'] = final_df['cluster'].replace({v: k for k, v in CLUSTER_MAPPINGS.items()})
        final_df['variable'] = final_df['variable'].replace({
            'MntWines': 'Wines',
            'MntFruits': 'Fruits',
            'MntMeatProducts': 'Meat',
            'MntFishProducts': 'Fish',
            'MntSweetProducts': 'Sweet',
            'MntGoldProds': 'Gold'
        })
        df_for_products = final_df
    return df_for_products


df_for_places = None
def get_df_for_places():
    global df_for_places
    if df_for_places is None:
        df = get_df_for_cluster_for_plots()
        df = df.loc[:,
             ['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'cluster']]
        df_melted = pd.melt(
            df,
            id_vars=['cluster']
        )
        final_df = df_melted.groupby(['cluster', 'variable']).mean().reset_index()
        final_df['cluster'] = final_df['cluster'].replace({v: k for k, v in CLUSTER_MAPPINGS.items()})
        final_df['variable'] = final_df['variable'].replace({
            'NumDealsPurchases': 'Discount',
            'NumWebPurchases': 'Web',
            'NumCatalogPurchases': 'Catalog',
            'NumStorePurchases': 'Store',
        })
        df_for_places = final_df
    return df_for_places



scaler = None
model = None
def predict_cluster(*args):
    global scaler, model
    if scaler is None:
        scaler = pickle.load(Path('data/scaler_selected.obj').open('rb'))
    if model is None:
        model = pickle.load(Path('data/final_model.obj').open('rb'))
    scaled = scaler.transform(
            np.array(
                [list(map(lambda x: 0 if x is None else x, args))]
            )
        )
    for i, v in enumerate(args):
        if v is None:
            scaled[0, i] = 0
    cluster_i = model.predict(
        scaled
    )
    return {v: k for k, v in CLUSTER_MAPPINGS.items()}[cluster_i[0]]


# GRAPHS =======================

def generate_products_graph():
    fig = px.bar(
        get_df_for_products(),
        x='cluster',
        y='value',
        color='variable',
        barmode='group',
        title='Amount spent in each product category'
    )
    return fig


def generate_places_graph():
    fig = px.bar(
        get_df_for_places(),
        x='cluster',
        y='value',
        color='variable',
        barmode='group',
        title='Purchases made in each category'
    )
    return fig


# MAIN ========================


def build_tab_4():
    return html.Div(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P(
                                            [
                                                'The top value customer segments (',
                                                html.B('High potential'), ' and ', html.B(' Elite'),
                                                ') spend a lot on ',
                                                html.B('Wines'), ' and ',  html.B('Meat.')
                                            ],
                                        className='blockquote'
                                        )
                                    ]
                                ),
                                className='bg-primary text-white translate-middle start-50 top-50',
                                style={'width': '60%'}
                            )
                        ],
                        width=4
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_products_graph()),
                        ],
                        width=8,
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P(
                                            [
                                                'Increasing prices on the ',
                                                html.B('Catalog'),
                                                ' may be a good strategy to increase profits.'
                                            ],
                                            className='blockquote'
                                        )
                                    ]
                                ),
                                className='bg-primary text-white translate-middle start-50 top-50',
                                style={'width': '60%'}
                            )
                        ],
                        width=4
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=generate_places_graph())
                        ],
                        width=8,
                    )
                ],
                className='mt-4'
            ),
            html.Hr(className='my-3'),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5('Predict a new customer'),
                            dbc.InputGroup(
                                [
                                    dbc.Input(
                                        id='input-days',
                                        placeholder='Days enrolled'
                                    )
                                ],
                                className='mt-3'
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.Input(
                                        id='input-totalspent',
                                        placeholder='Total spent'
                                    )
                                ],
                                className='mt-3'
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.Input(
                                        id='input-purchases',
                                        placeholder='# Purchases'
                                    )
                                ],
                                className='mt-3'
                            ),
                            dbc.InputGroup(
                                [
                                    dbc.Input(
                                        id='input-check',
                                        placeholder='Avg check'
                                    )
                                ],
                                className='mt-3'
                            ),
                        ],
                        width=4
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P(
                                            [
                                                html.I('Please, complete at least one field to obtain a prediction.'),
                                            ],
                                            id='prediction-paragraph',
                                            className='blockquote'
                                        )
                                    ]
                                ),
                                className='bg-primary text-white translate-middle start-50 top-50',
                                style={'width': '40%'}
                            )
                        ],
                        width=8
                    )
                ]
            )
        ],
        className='p-5'
    )


# CALLBACKS

def create_callbacks_for_tab4():
    @app.callback(
        Output('prediction-paragraph', 'children'),
        Input('input-days', 'value'),
        Input('input-totalspent', 'value'),
        Input('input-purchases', 'value'),
        Input('input-check', 'value')
    )
    def update_prediction(*args):
        if all(map(lambda x: not x, args)):
            return [html.I('Please, complete at least one field to obtain a prediction.')]
        try:
            args_int = list(map(lambda x: None if not x else int(x), args))
        except:
            return [html.I('All input must be integers')]
        cluster = predict_cluster(*args_int)
        return [
            'The predicted cluster is:', html.Br(),
            html.H3(html.B(cluster))
        ]


