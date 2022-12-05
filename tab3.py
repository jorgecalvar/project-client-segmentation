
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
    pass


def generate_check_boxplot(cluster):
    pass


def generate_relationship_pie(cluster):
    pass

def generate_education_pie(cluster):
    pass


def generate_income_boxplot(cluster):
    pass


def generate_age_boxplot(cluster):
    pass



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

                ],
                width=8
            )
        ]
    )
