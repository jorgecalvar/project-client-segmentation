import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import logging
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots
import math

from maindash import app

df_selectedvariables = pd.read_csv("data/df_selectedvariables.csv")

# Crear opciones para Marital_Status
statuses = df_selectedvariables["Marital_Status"].unique().tolist()
statuses.sort()
options_dropdown_status = []
for status in statuses:
    options_dropdown_status.append({'label': status, 'value': status})

# Crear opciones para Relationship
relations = df_selectedvariables["Relationship"].unique().tolist()
relations.sort()
options_dropdown_relation = []
for relation in relations:
    options_dropdown_relation.append({'label': relation, 'value': relation})

# Crear opciones para Education
educations = df_selectedvariables["Education"].unique().tolist()
educations.sort()
options_dropdown_education = []
for education in educations:
    options_dropdown_education.append({'label': education, 'value': education})

# Crear opciones para GradorPost
degrees = df_selectedvariables["GradorPost"].unique().tolist()
degrees.sort()
options_dropdown_degree = []
for degree in degrees:
    options_dropdown_degree.append({'label': degree, 'value': degree})

df_num = df_selectedvariables.iloc[:, 6:15]
num_features = df_num.columns.to_list()
df_cat = df_selectedvariables.iloc[:, 1:5]
cat_features = df_cat.columns.to_list()


def build_tab_1():
    return html.Div(
        children=[
            dbc.Row(  # Primera fila
                [
                   dbc.Col(
                        [
                            dbc.Container(  # Primera fila
                                [
                                html.P("""
                                A company has collected data about its customers and their recent purchases 
                                in order to create customized products or targeted marketing campaigns to find customer profiles that may resemble each other. """,
                                ),
                                ]
                            ),
                            dbc.Container(  # Primera fila
                                [
                                    dbc.Button(
                                        "Info", id="popover-bottom-target", color="info",
                                        className='m-2'
                                    ),
                                    dbc.Popover(
                                        [
                                            dbc.PopoverHeader("Info"),
                                            dbc.PopoverBody("""With this data the company asks you to:
Perform a descriptive analysis of the data looking for common patterns among customers.
Build a clustering model for the different types of customers by selecting the variables considered most appropriate for the study.
Using a dashboard, visualize the most relevant aspects of the descriptive together with the possibility of grouping a new customer with one of the previous clusters"""),
                                        ],
                                        id="popover",
                                        target="popover-bottom-target",  # needs to be the same as dbc.Button id
                                        placement="bottom",
                                        is_open=False,
                                    )
                                    ,
                                ]
                            )                        ],
                        width=4,
                        className='p-4'
                    ),

                    dbc.Col(  # Bloque derecho
                        [
                            dbc.Row(
                                [
                                    dbc.Col(  # Filtros 1
                                        [
                                            dcc.Dropdown(
                                                options=options_dropdown_status,
                                                placeholder="Marital Status",
                                                id="status_dropdown_1",
                                                className='mb-1',
                                            ),
                                            dcc.Dropdown(
                                                options=options_dropdown_relation,
                                                placeholder="Relation ",
                                                id="relation_dropdown_1",
                                                className='mb-1',
                                            ),
                                            dcc.Dropdown(
                                                options=options_dropdown_education,
                                                placeholder="Education",
                                                id="education_dropdown_1",
                                                className='mb-1',
                                            ),
                                            dcc.Dropdown(
                                                options=options_dropdown_degree,
                                                placeholder="Degree",
                                                id="degree_dropdown_1",
                                                className='mb-3',
                                            ),
                                            # html.P("Relation & Degree are simplified versions of M_Status & Educ"),
                                        ],
                                        width=2
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("Age")
                                                        ],
                                                        width=3
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.Age),
                                                                max=max(df_selectedvariables.Age),
                                                                value=[min(df_selectedvariables.Age),
                                                                       max(df_selectedvariables.Age)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='Age_slider_1')
                                                        ],
                                                        width=9
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("Days")
                                                        ],
                                                        width=3
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.days_enrolled),
                                                                max=max(df_selectedvariables.days_enrolled),
                                                                value=[min(df_selectedvariables.days_enrolled),
                                                                       max(df_selectedvariables.days_enrolled)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='days_enrolled_slider_1')
                                                        ],
                                                        width=9
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("Income")
                                                        ],
                                                        width=3
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.Income),
                                                                max=max(df_selectedvariables.Income),
                                                                value=[min(df_selectedvariables.Income),
                                                                       max(df_selectedvariables.Income)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='Income_slider_1')
                                                        ],
                                                        width=9
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("Spent")
                                                        ],
                                                        width=3
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.Total_Spent),
                                                                max=max(df_selectedvariables.Total_Spent),
                                                                value=[min(df_selectedvariables.Total_Spent),
                                                                       max(df_selectedvariables.Total_Spent)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='Total_Spent_slider_1')
                                                        ],
                                                        width=9
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                        ],
                                        width=5
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("# Purchases")
                                                        ],
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.NumAllPurchases),
                                                                max=max(df_selectedvariables.NumAllPurchases),
                                                                value=[min(df_selectedvariables.NumAllPurchases),
                                                                       max(df_selectedvariables.NumAllPurchases)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='NumAllPurchases_slider_1')
                                                        ],
                                                        width=7
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("Avg check")
                                                        ],
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.AverageCheck),
                                                                max=max(df_selectedvariables.AverageCheck),
                                                                value=[min(df_selectedvariables.AverageCheck),
                                                                       max(df_selectedvariables.AverageCheck)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='AverageCheck_slider_1')
                                                        ],
                                                        width=7
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("% Discounted")
                                                        ],
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.ShareDealsPurchases),
                                                                max=max(df_selectedvariables.ShareDealsPurchases),
                                                                value=[min(df_selectedvariables.ShareDealsPurchases),
                                                                       max(df_selectedvariables.ShareDealsPurchases)],
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='ShareDealsPurchases_slider_1')
                                                        ],
                                                        width=7
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("# Kids")
                                                        ],
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RangeSlider(
                                                                min=min(df_selectedvariables.kidsteenHome),
                                                                max=max(df_selectedvariables.kidsteenHome),
                                                                value=[min(df_selectedvariables.kidsteenHome),
                                                                       max(df_selectedvariables.kidsteenHome)],
                                                                step=1,
                                                                tooltip={"placement": "bottom", "always_visible": True},
                                                                id='kidsteenHome_slider_1')
                                                        ],
                                                        width=7
                                                    ),
                                                ],
                                                className='mb-3',
                                            ),
                                        ],
                                        width=5
                                    )
                                ]
                            )],
                        style={
                            "border-right": "solid gray"
                        },
                        width=8,
                        className='p-4'
                    )
                    ]),

            dbc.Row(  # Primera fila
                [


                    dbc.Col(  # Primera fila
                        [
                                dcc.Graph(id='figure_2')
                        ],
                        width=4,
                        className='p-4'
                    ),


                    dbc.Col(  # Primera fila
                        [
                            dcc.Graph(id='figure_1')
                        ],
                        style={
                            "border-right": "solid gray"
                        },
                        width=8,
                        className='p-4'
                    ),


                ]
            ),
            html.Hr(
                style={'border': 'solid gray'}
            ),

            dbc.Row(  # tercera fila
                [
                    dbc.Col(  # Bloque abajo Izquierda
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            options=num_features,
                                            placeholder="X axis",
                                            id="x_scat"
                                        ),
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=num_features,
                                                placeholder="Y axis",
                                                id="y_scat"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=num_features,
                                                placeholder="By Size",
                                                id="size_scat"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=cat_features,
                                                placeholder="Category by Color",
                                                id="color_scat"
                                            )
                                        ],
                                        width=3
                                    )
                                ],
                                className='mb-3'
                            ),
                            dcc.Graph(
                                id="figure_3",
                                style={
                                    "display": "none"
                                }
                            )
                        ],
                        style={
                            "border-right": "solid gray",
                        },
                        width=6,
                        className='p-4'
                    ),

                    dbc.Col(  # Bloque abajo derecha
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=cat_features,
                                                placeholder="X axis",
                                                id="x_box"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=num_features,
                                                placeholder="Y axis",
                                                id="y_box"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=cat_features,
                                                placeholder="Category by Color",
                                                id="color_box"
                                            )
                                        ],
                                        width=3
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Dropdown(
                                                options=cat_features,
                                                placeholder="Column separator",
                                                id="facet_col_box"
                                            )
                                        ],
                                        width=3
                                    ),
                                ],
                                className='mb-3'
                            ),


                            dcc.Graph(
                                id="figure_4",
                                style={
                                    "display": "none"
                                }
                            )
                        ],
                        style={
                            "border-left": "solid gray",
                        },
                        width=6,
                        className='p-4'
                    ),
                ]
            ),
        ]
    )


def create_callbacks_for_tab1():


    @app.callback(
        Output("figure_1", "figure"),
        Output("figure_1", "style"),
        Input("status_dropdown_1", "value"),
        Input("relation_dropdown_1", "value"),
        Input("education_dropdown_1", "value"),
        Input("degree_dropdown_1", 'value'),
        [Input("Age_slider_1", "value")],
        [Input("days_enrolled_slider_1", "value")],
        [Input("Income_slider_1", "value")],
        [Input("Total_Spent_slider_1", "value")],
        [Input("NumAllPurchases_slider_1", "value")],
        [Input("AverageCheck_slider_1", "value")],
        [Input("ShareDealsPurchases_slider_1", "value")],
        [Input("kidsteenHome_slider_1", "value")]
    )
    def figure1(stat, rel, edu, deg, ag, day, inco, spen, purch, check, share, kids):

        df = df_selectedvariables


        dff = df.loc[
            (df.Age >= ag[0]) & (df.Age <= ag[1]) & # Age
            (df.days_enrolled >= day[0]) & (df.days_enrolled <= day[1]) & # Days enrolled
            (df.Income >= inco[0]) & (df.Income <= inco[1]) & # Income
            (df.Total_Spent >= spen[0]) & (df.Total_Spent <= spen[1]) & # Total Spent
            (df.NumAllPurchases >= purch[0]) & (df.NumAllPurchases <= purch[1]) & # Numm All purchases
            (df.AverageCheck >= check[0]) & (df.AverageCheck <= check[1]) & # Average check
            (df.ShareDealsPurchases >= share[0]) & (df.ShareDealsPurchases <= share[1]) & # Share deals
            (df.kidsteenHome >= kids[0]) & (df.kidsteenHome <= kids[1]) # Kids
            ]
        if stat is not None:
            dff = dff.loc[dff.Marital_Status == stat]
        if rel is not None:
            dff = dff.loc[dff.Relationship == rel]
        if edu is not None:
            dff = dff.loc[dff.Education == edu]
        if deg is not None:
            dff = dff.loc[dff.GradorPost == deg]

        #df_num = df_selectedvariables.iloc[:, 5:14]
        df_num = dff.iloc[:, 5:14]
        features = [x for x in df_num.columns]

        fig = make_subplots(rows=3,
                            cols=3,
                            subplot_titles=features)

        # Preparo la estructura de filas y columnas para asignar
        rows = np.repeat([1, 2, 3], 3)
        cols = [1, 2, 3] * 3

        # Creo secuencialmente la figura con un loop
        for feature, row, col in zip(features, rows, cols):
            if feature == features[-1]:
                showlegend = True
            else:
                showlegend = False
            fig.add_trace(
                go.Histogram(
                    x=df_num[feature],
                    name=feature, showlegend=False
                ),
                row=row,
                col=col
            )
        fig.update_layout(title="Histograms ", bargap=0.1, barmode="overlay",
                          height=600)
        return (fig, {"display": "block"})




    @app.callback(
        Output("figure_2", "figure"),
        Output("figure_2", "style"),
        Input("status_dropdown_1", "value"),
        Input("relation_dropdown_1", "value"),
        Input("education_dropdown_1", "value"),
        Input("degree_dropdown_1", 'value'),
        [Input("Age_slider_1", "value")],
        [Input("days_enrolled_slider_1", "value")],
        [Input("Income_slider_1", "value")],
        [Input("Total_Spent_slider_1", "value")],
        [Input("NumAllPurchases_slider_1", "value")],
        [Input("AverageCheck_slider_1", "value")],
        [Input("ShareDealsPurchases_slider_1", "value")],
        [Input("kidsteenHome_slider_1", "value")]
    )
    def figure2(stat, rel, edu, deg, ag, day, inco, spen, purch, check, share, kids):

        df = df_selectedvariables

        dff = df.loc[
            (df.Age >= ag[0]) & (df.Age <= ag[1]) & # Age
            (df.days_enrolled >= day[0]) & (df.days_enrolled <= day[1]) & # Days enrolled
            (df.Income >= inco[0]) & (df.Income <= inco[1]) & # Income
            (df.Total_Spent >= spen[0]) & (df.Total_Spent <= spen[1]) & # Total Spent
            (df.NumAllPurchases >= purch[0]) & (df.NumAllPurchases <= purch[1]) & # Numm All purchases
            (df.AverageCheck >= check[0]) & (df.AverageCheck <= check[1]) & # Average check
            (df.ShareDealsPurchases >= share[0]) & (df.ShareDealsPurchases <= share[1]) & # Share deals
            (df.kidsteenHome >= kids[0]) & (df.kidsteenHome <= kids[1]) # Kids
            ]
        if stat is not None:
            dff = dff.loc[dff.Marital_Status == stat]
        if rel is not None:
            dff = dff.loc[dff.Relationship == rel]
        if edu is not None:
            dff = dff.loc[dff.Education == edu]
        if deg is not None:
            dff = dff.loc[dff.GradorPost == deg]

        df_cat=dff.iloc[:, 1:5]

        fig = make_subplots(rows=2,
                            cols=2,
                            specs=[[{"type": "pie"}, {"type": "pie"}],[{"type": "pie"}, {"type": "pie"}]],
                            subplot_titles=["Relationship",  "Type of Relationship","Grad or PostGrad", "Specific Education"])

        fig.add_trace(
            go.Pie(
                labels=df_cat.Relationship.value_counts().index.tolist(),
                values=df_cat.Relationship.value_counts().tolist(),
                textinfo='label+percent', insidetextorientation='radial', hole=.4
            ),
            row=1,
            col=1
        )
        fig.add_trace(
            go.Pie(
                labels=df_cat.GradorPost.value_counts().index.tolist(),
                values=df_cat.GradorPost.value_counts().tolist(),
                textinfo='label+percent', insidetextorientation='radial',hole=.4

            ),
            row=2,
            col=1
        )
        fig.add_trace(
            go.Pie(
                labels=df_cat.Marital_Status.value_counts().index.tolist(),
                values=df_cat.Marital_Status.value_counts().tolist(),
                textinfo='label+percent', insidetextorientation='radial'
            ),
            row=1,
            col=2
        )
        fig.add_trace(
            go.Pie(
                labels=df_cat.Education.value_counts().index.tolist(),
                values=df_cat.Education.value_counts().tolist(),
                textinfo='label+percent', insidetextorientation='radial'

            ),
            row=2,
            col=2
        )
        fig.update(layout_title_text='Categorical variables',layout_showlegend=False)
        fig.update_layout(height=600)
        return (fig, {"display": "block"})





    @app.callback(
        Output("figure_3", "figure"),
        Output("figure_3", "style"),
        Input("x_scat", "value"),
        Input("y_scat", "value"),
        Input("size_scat", "value"),
        Input("color_scat", 'value'),

    )



    def figure3(x, y, size, colr):
        #if x is None and y is None and colr is None and size is None:
         #   x=y=colr=size="_"
        #title=str("Scatterplot of " + x+" vs " + y + " where color=" + colr +" and size="+size)
        if x is None or y is None:
            return px.scatter(title='Please, enter the variables you want to display!'), {'display': 'block'}

        fig = px.scatter(df_selectedvariables, x=x, y=y, color=colr, size=size,
                         title="Scatterplot by size and color")
        fig.update_layout()

        return (fig, {"display": "block"})

    @app.callback(
        Output("figure_4", "figure"),
        Output("figure_4", "style"),
        Input("x_box", "value"),
        Input("y_box", "value"),
        Input("color_box", "value"),
        Input("facet_col_box", 'value'),
    )
    def figure4(x_box, y_box, color_box,facet_col_box):
        #if x_box is None and y_box is None and color_box is None and facet_col_box is None:
            #x_box=y_box=color_box=facet_col_box="_"
        #title = str("Boxplots by " + x_box+" of " + y_box + " divided by color=" + color_box +" and separated in columns by "+facet_col_box)
        if x_box is None or y_box is None:
            return px.scatter(title='Please, enter the variables you want to display!'), {'display': 'block'}

        fig = px.box(df_selectedvariables, x=x_box, y=y_box, color=color_box, facet_col=facet_col_box,
                         title="Boxplots by category, color and possible column separation")
        fig.update_layout()

        return (fig, {"display": "block"})

    @app.callback(
        Output("popover", "is_open"),
        [Input("popover-bottom-target", "n_clicks")],
        [State("popover", "is_open")],
    )
    def toggle_popover(n, is_open):
        if n:
            return not is_open
        return is_open
