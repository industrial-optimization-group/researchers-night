import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np


data = pd.read_csv("./data/node_data.csv")
print(data.head())

names = data.columns

"""
maxi = details.loc[1].astype(int)
details_on_card = details.loc[2].astype(int)

details_on_card = details.columns[details_on_card == 1]
"""
maxi = [1, 1, 1]
details_on_card = ["Cover", "Efficiency", "Activation", "Node combo"]


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LITERA],
    eager_loading=True,
    suppress_callback_exceptions=True,
)


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        children="Selecting a combination of nodes",
                        className="text-center mt-4",
                    )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        dbc.Form(
                            [
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Cover",
                                            html_for="cover",
                                        ),
                                        dcc.Slider(
                                            id="cover",
                                            min=7,
                                            max=12,
                                            step=None,
                                            included=False,
                                            value=7,
                                            marks={
                                                7: "7",
                                                8: "8",
                                                9: "9",
                                                10: "10",
                                                11: "11",
                                                12: "12",
                                            },
                                            # className="text-center mt-5",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Efficiency",
                                            html_for="efficiency",
                                        ),
                                        dcc.Slider(
                                            id="efficiency",
                                            min=8,
                                            max=14,
                                            step=1,
                                            value=14,
                                            included=False,
                                            marks={
                                                8: "8",
                                                9: "9",
                                                10: "10",
                                                11: "11",
                                                12: "12",
                                                13: "13",
                                                14: "14",
                                            },
                                            className="text-center mt-5",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Activation",
                                            html_for="activation",
                                        ),
                                        dcc.Slider(
                                            id="activation",
                                            min=8,
                                            max=15,
                                            step=1,
                                            included=False,
                                            value=15,
                                            marks={
                                                8: "8",
                                                9: "9",
                                                10: "10",
                                                11: "11",
                                                12: "12",
                                                13: "13",
                                                14: "14",
                                                15: "15",
                                            },
                                            className="text-center mt-5",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                            ],
                            style={"maxHeight": "560px", "overflow": "auto"},
                        ),
                    ],
                    width={"size": 5, "offset": 1},
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            children=[
                                dbc.CardHeader(
                                    "The best combination of nodes with the given preferences:"
                                ),
                                dbc.CardBody(id="results"),
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            children=[
                                dbc.CardHeader("Other closely matching combinations:"),
                                dbc.CardBody(
                                    id="other-results",
                                    children=(
                                        [
                                            html.P(
                                                html.Span(
                                                    f"{i}. ",
                                                    id=f"other-results-list-{i}",
                                                )
                                            )
                                            for i in range(2, 6)
                                        ]
                                        + [
                                            dbc.Tooltip(
                                                id=f"other-results-tooltip-{i}",
                                                target=f"other-results-list-{i}",
                                                placement="right",
                                                style={
                                                    "maxWidth": 700,
                                                    "background-color": "white",
                                                    "color": "white",
                                                    "border-style": "solid",
                                                    "border-color": "black",
                                                },
                                            )
                                            for i in range(2, 6)
                                        ]
                                    ),
                                ),
                            ],
                            className="mt-4",
                        ),
                        html.Div(id="tooltips"),
                    ],
                    width={"size": 5, "offset": 0},
                    className="mb-2 mt-2",
                ),
            ]
        ),
        dbc.Row([html.Div(id="callback-dump")]),
    ],
)


@app.callback(
    [
        Output("results", "children"),
        *[Output(f"other-results-list-{i}", "children") for i in range(2, 6)],
        *[Output(f"other-results-tooltip-{i}", "children") for i in range(2, 6)],
    ],
    [Input(f"{attr}", "value") for attr in ["cover", "efficiency", "activation"]],
)
def results(*choices):
    choice_data = data
    relevant_data = choice_data[["Cover", "Efficiency", "Activation"]].reset_index(
        drop=True
    )
    card_data = choice_data[details_on_card].reset_index(drop=True)
    maxi = np.asarray([1, 1, 1])
    relevant_data = relevant_data * maxi
    ideal = relevant_data.min().values
    nadir = relevant_data.max().values
    aspirations = choices * maxi
    distance = (aspirations - relevant_data) / (ideal - nadir)
    distance = distance.max(axis=1)
    distance_order = np.argsort(distance)
    tmp = card_data.loc[distance_order.values[0]]
    print(f"{tmp=}")
    best = table_from_data(card_data.loc[distance_order.values[0]], choices)
    total_number = len(distance_order)
    if total_number >= 4:
        others, tooltips = other_options(card_data.loc[distance_order.values[1:5]])
    else:
        others, tooltips = other_options(
            card_data.loc[distance_order.values[1:total_number]]
        )
        others = others + [f"{i}. -" for i in range(len(others) + 2, 6)]
        tooltips = tooltips + [None for i in range(len(tooltips) + 2, 6)]
    return (best, *others, *tooltips)


def table_from_data(data, choices):
    # print(choices)
    to_compare = ["Cover", "Efficiency", "Activation"]
    # print(data[to_compare].values)
    diff = (data[to_compare].values - choices) * [1, 1, 1]
    colors = ["green" if x >= 0 else "red" for x in diff]
    # print(np.sign(diff))
    return dbc.Table(
        [
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Th(col),
                            html.Td(
                                [
                                    str(data[col]),
                                ],
                            ),
                            html.Td(
                                [
                                    html.Span(
                                        " ▉",
                                        style={
                                            "color": c,
                                        },
                                    )
                                ],
                            ),
                        ]
                    )
                    for (col, c) in zip(data.index, colors)
                    if col != "Node combo"
                ]
            )
        ]
    )


def table_from_data_horizontal(data):
    header = [html.Thead(html.Tr([html.Th(col) for col in data.index]))]
    body = [html.Tbody([html.Tr([html.Td(data[col]) for col in data.index])])]
    return dbc.Table(header + body)


def other_options(data):
    contents = []
    tables = []
    ids = []
    i = 2
    for index, row in data.iterrows():
        contents.append(f"{i}. {row['Node combo']}")
        tables.append(table_from_data_horizontal(row))
        i = i + 1
    return contents, tables


if __name__ == "__main__":
    app.run_server(debug=True)
