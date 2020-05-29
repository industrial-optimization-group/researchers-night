import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import utils.dash_reusable_components as drc
import dash_table
import plotly.express as ex
import pandas as pd
import numpy as np

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

data = pd.read_csv("./data/data.csv", header=0)
data.drop(columns="id", inplace=True)

var = data[data.columns[1:]]
target = data[data.columns[0]]

# apply SelectKBest class to extract top 10 best features
bestfeatures = SelectKBest(score_func=chi2, k=10)
fit = bestfeatures.fit(var, target)

dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(var.columns)

# concat two dataframes for better visualization
featureScores = pd.concat([dfcolumns, dfscores], axis=1)
featureScores.columns = ["Specs", "Score"]  # naming the dataframe columns
# print(featureScores.nlargest(10, "Score"))  # print 10 best features


top_ten_attrs = [
    a
    for lis in [
        [x, html.Br()]
        for x in list(featureScores.nlargest(10, "Score")["Specs"].values)
    ]
    for a in lis
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        dbc.Row([dbc.Col(html.H1(children="Optimization Group"))]),
        dbc.Row(
            [
                dbc.Col(
                    children=html.Div(
                        [
                            dbc.Card(
                                [
                                    html.H4(
                                        "Researcher's Night Event",
                                        className="card-title",
                                    ),
                                    html.P(
                                        (
                                            "Dummy text Lorem ipsum dolor sit amet,"
                                            " consectetur adipiscing elit. Donec ante odio,"
                                            " ultricies cursus pulvinar nec, pretium vitae"
                                            " quam. Sed eget placerat leo, feugiat"
                                            " efficitur felis. Nullam consequat dui a"
                                            " dictum ultrices. Quisque ultricies convallis"
                                            " tristique. Mauris aliquet orci at sapien"
                                            " fringilla ultricies. Quisque egestas in"
                                            " libero at porta. Praesent eget magna dapibus."
                                        ),
                                        className="card-text",
                                    ),
                                ]
                            ),
                            dbc.Card(
                                children=[
                                    html.H4(
                                        "Top 10 attributes:", className="card-title"
                                    ),
                                    # Because I could
                                    html.P(top_ten_attrs, className="card-text",),
                                ],
                            ),
                            dbc.Card(
                                children=[
                                    html.H4(
                                        "Choose attributes to be plotted",
                                        className="card-title",
                                    ),
                                    dcc.Dropdown(
                                        id="attributes-dropdown",
                                        options=[
                                            {"label": attr, "value": attr}
                                            for attr in var.columns
                                        ],
                                        clearable=True,
                                        searchable=True,
                                        multi=True,
                                        value=featureScores.nlargest(5, "Score")[
                                            "Specs"
                                        ].values,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    width=2,
                ),
                dbc.Col(
                    children=dcc.Graph(
                        id="graph-sklearn-svm", style={"height": "720px"}
                    ),
                    width=9,
                ),
            ]
        ),
    ],
)


@app.callback(
    Output("graph-sklearn-svm", "figure"), [Input("attributes-dropdown", "value")],
)
def create_figure(chosen_attrs):
    return ex.scatter_matrix(data, dimensions=chosen_attrs, color=data.columns[0])


if __name__ == "__main__":
    app.run_server(debug=True)
