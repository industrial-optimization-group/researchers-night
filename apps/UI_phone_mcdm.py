import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import dash_table
import plotly.express as ex
import plotly.graph_objects as go
import pandas as pd
import numpy as np


data = pd.read_csv("./data/Phone_dataset_new.csv", header=0)
details = pd.read_csv("./data/Phone_details.csv", header=0)

names = details.loc[0]

data = data.rename(columns=names)
details = details.rename(columns=names)

maxi = details.loc[1].astype(int)
details_on_card = details.loc[2].astype(int)

details_on_card = details.columns[details_on_card == 1]


fitness_columns = {
    "Memory": -1,
    "RAM": -1,
    "Camera (MP)": -1,
    "Price (Euros)": 1,
}

fitness_data = data[fitness_columns] * maxi[fitness_columns].values


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
                        children="What is your optimal phone?",
                        className="text-center mt-4",
                    )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        # Top card with details(?)
                        dbc.Card(
                            children=[
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            "Researcher's Night Event",
                                            className="card-title text-center",
                                        ),
                                        html.P(
                                            (
                                                "This app uses decision support tools to "
                                                "quickly and easily find phones which reflect "
                                                "the user's desires. Input your preferences "
                                                "below. The box on top right shows the phone "
                                                "which matches the preferences the best. "
                                                "The box on bottom right provides some "
                                                "close alternatives."
                                            ),
                                            className="card-text",
                                        ),
                                    ]
                                )
                            ],
                            className="mr-3 ml-3 mb-2 mt-2",
                        ),
                        dbc.Form(
                            [
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Choose desired operating system",
                                            html_for="os-choice",
                                        ),
                                        dbc.RadioItems(
                                            options=[
                                                {
                                                    "label": "Android",
                                                    "value": "Android",
                                                },
                                                {"label": "iOS", "value": "IOS"},
                                                {
                                                    "label": "No preference",
                                                    "value": "both",
                                                },
                                            ],
                                            id="os-choice",
                                            value="both",
                                            inline=True,
                                            # className="text-center mt-4",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Choose desired Memory capacity (GB)",
                                            html_for="memory-choice",
                                        ),
                                        dcc.Slider(
                                            id="memory-choice",
                                            min=16,
                                            max=256,
                                            step=None,
                                            included=False,
                                            value=256,
                                            marks={
                                                16: "16",
                                                32: "32",
                                                64: "64",
                                                128: "128",
                                                256: "256",
                                            },
                                            # className="text-center mt-5",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Choose desired RAM capacity (GB)",
                                            html_for="ram-choice",
                                        ),
                                        dcc.Slider(
                                            id="ram-choice",
                                            min=2,
                                            max=12,
                                            step=1,
                                            value=12,
                                            included=False,
                                            marks={
                                                2: "2",
                                                3: "3",
                                                4: "4",
                                                5: "5",
                                                6: "6",
                                                7: "7",
                                                8: "8",
                                                9: "9",
                                                10: "10",
                                                11: "11",
                                                12: "12",
                                            },
                                            className="text-center mt-5",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Choose desired camera resolution (MP)",
                                            html_for="cam-choice",
                                        ),
                                        dcc.Slider(
                                            id="cam-choice",
                                            min=0,
                                            max=130,
                                            step=1,
                                            included=False,
                                            value=70,
                                            marks={
                                                0: "0",
                                                10: "10",
                                                30: "30",
                                                50: "50",
                                                70: "70",
                                                90: "90",
                                                110: "110",
                                                130: "130",
                                            },
                                            className="text-center mt-5",
                                        ),
                                    ],
                                    className="mr-3 ml-3 mb-2 mt-2",
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label(
                                            "Choose desired budget (Euros)",
                                            html_for="cost-choice",
                                        ),
                                        dcc.Slider(
                                            id="cost-choice",
                                            min=0,
                                            max=1400,
                                            step=1,
                                            included=False,
                                            value=100,
                                            marks={
                                                0: "0",
                                                200: "200",
                                                400: "400",
                                                600: "600",
                                                800: "800",
                                                1000: "1000",
                                                1200: "1200",
                                                1400: "1400",
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
                                dbc.CardHeader("The best phone for you is:"),
                                dbc.CardBody(id="results"),
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            children=[
                                dbc.CardHeader("Other great phones:"),
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
    [
        Input(f"{attr}-choice", "value")
        for attr in ["os", "memory", "ram", "cam", "cost"]
    ],
)
def results(*choices):
    if choices[0] == "both":
        choice_data = data
    elif choices[0] == "IOS":
        choice_data = data[[True if "IOS" in st else False for st in data["OS"]]]
    if choices[0] == "Android":
        choice_data = data[[True if "Android" in st else False for st in data["OS"]]]
    relevant_data = choice_data[
        ["Memory", "RAM", "Camera (MP)", "Price (Euros)",]
    ].reset_index(drop=True)
    card_data = choice_data[details_on_card].reset_index(drop=True)
    maxi = np.asarray([-1, -1, -1, 1])
    relevant_data = relevant_data * maxi
    ideal = relevant_data.min().values
    nadir = relevant_data.max().values
    aspirations = choices[1:] * maxi
    distance = (aspirations - relevant_data) / (ideal - nadir)
    distance = distance.max(axis=1)
    distance_order = np.argsort(distance)
    best = table_from_data(card_data.loc[distance_order.values[0]], choices[1:])
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


"""@app.callback(Output("tooltips", "children"), [Input("callback-dump", "children")])
def tooltips(tooldict):
    num = len(tooldict["ids"])
    content = []
    for i in range(num):
        content.append(dbc.Tooltip(tooldict["tables"][i], target=tooldict["ids"][i]))
    return content"""


def table_from_data(data, choices):
    # print(choices)
    to_compare = ["Memory", "RAM", "Camera (MP)", "Price (Euros)"]
    # print(data[to_compare].values)
    diff = (data[to_compare].values - choices) * [1, 1, 1, -1]
    colors = [None, None, None] + ["green" if x >= 0 else "red" for x in diff]
    # print(np.sign(diff))
    return dbc.Table(
        [
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Th(col),
                            html.Td([str(data[col]),],),
                            html.Td([html.Span(" ▉", style={"color": c,},)],),
                        ]
                    )
                    for (col, c) in zip(data.index, colors)
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
        contents.append(f"{i}. {row['Model']}")
        tables.append(table_from_data_horizontal(row))
        i = i + 1
    return contents, tables


if __name__ == "__main__":
    app.run_server(debug=False)
