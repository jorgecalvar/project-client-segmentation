
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
        df_clustered = pd.read_csv('df_clustered_all.csv')
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
    return dbc.Container(
        [
            dcc.Graph(figure=generate_products_graph()),
            dcc.Graph(figure=generate_places_graph())
        ],
        className='p-5'
    )



