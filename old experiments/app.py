import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

import plotly.express as ex
import plotly.graph_objects as go
import pandas as pd
import numpy as np


data = pd.read_csv("./data/Phone_dataset.csv", header=0)
details = pd.read_csv("./data/Phone_details.csv", header=0)

names = details.loc[0]

data = data.rename(columns=names)
details = details.rename(columns=names)

maxi = details.loc[1].astype(int)
details_on_card = details.loc[2].astype(int)

details_on_card = details.columns[details_on_card == 1]


fitness_columns = details.columns[maxi != 0]
fitness_data = data[fitness_columns].values * maxi[fitness_columns].values


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

states = ["OS", "Memory", "RAM", "Camera", "Cost", "Results"]

prev_states = {
    "OS": None,
    "Memory": "OS",
    "RAM": "Memory",
    "Camera": "RAM",
    "Cost": "Camera",
    "Results": "Cost",
}

next_states = {
    "OS": "Memory",
    "Memory": "RAM",
    "RAM": "Camera",
    "Camera": "Cost",
    "Cost": "Results",
    "Results": None,
}

prev_button = [
    dbc.Col(
        dbc.Button("Previous", id="prev", block=True, color="primary"),
        width={"size": 1, "offset": 0},
        align="end",
    ),
]

next_button = [
    dbc.Col(
        dbc.Button("Next", id="next", block=True, color="primary"),
        width={"size": 1, "offset": 2},
        align="end",
    ),
]

os_state = [
    dbc.Col(
        children=[
            html.H2(
                "Choose desired operating system",
                className="text-center mt-5",
            ),
            dbc.RadioItems(
                options=[
                    {"label": "Android", "value": "Android"},
                    {"label": "iOS", "value": "IOS"},
                    {"label": "No preference", "value": "both"},
                ],
                id="os-choice",
                className="text-center mt-4",
            ),
        ],
        width={"size": 6, "offset": 2},
    )
]

memory_state = [
    dbc.Col(
        children=[
            html.H2(
                "Choose desired Memory capacity (GB)",
                className="text-center mt-5",
            ),
            dcc.Slider(
                id="memory-choice",
                min=16,
                max=128,
                step=None,
                included=False,
                value=128,
                marks={16: "16", 32: "32", 64: "64", 128: "128"},
                className="text-center mt-5",
            ),
        ],
        width={"size": 6, "offset": 2},
    )
]

ram_state = [
    dbc.Col(
        children=[
            html.H2(
                "Choose desired RAM capacity (GB)",
                className="text-center mt-5",
            ),
            dcc.Slider(
                id="ram-choice",
                min=1,
                max=8,
                step=1,
                value=8,
                included=False,
                marks={1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8"},
                className="text-center mt-5",
            ),
        ],
        width={"size": 6, "offset": 2},
    )
]


cam_state = [
    dbc.Col(
        children=[
            html.H2(
                "Choose desired camera resolution",
                className="text-center mt-5",
            ),
            dcc.Slider(
                id="cam-choice",
                min=10,
                max=70,
                step=1,
                included=False,
                value=70,
                marks={
                    10: "10",
                    20: "20",
                    30: "30",
                    40: "40",
                    50: "50",
                    60: "60",
                    70: "70",
                },
                className="text-center mt-5",
            ),
        ],
        width={"size": 6, "offset": 2},
    )
]

cost_state = [
    dbc.Col(
        children=[
            html.H2(
                "Choose desired budget (Euros)",
                className="text-center mt-5",
            ),
            dcc.Slider(
                id="cost-choice",
                min=100,
                max=700,
                step=1,
                included=False,
                value=100,
                marks={
                    100: "100",
                    200: "200",
                    300: "300",
                    400: "400",
                    500: "500",
                    600: "600",
                    700: "700",
                },
                className="text-center mt-5",
            ),
        ],
        width={"size": 6, "offset": 2},
    )
]


state_layouts = {
    "OS": prev_button + os_state + next_button,
    "Memory": prev_button + memory_state + next_button,
    "RAM": prev_button + ram_state + next_button,
    "Camera": prev_button + cam_state + next_button,
    "Cost": prev_button + cost_state + next_button,
}


app.layout = html.Div(
    [
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
        # Empty location for question/results
        dbc.Row(children=state_layouts["OS"], id="empty-slot"),
        html.Div(children=[], id="os_pref"),
        html.Div(children=[], id="memory_pref"),
        html.Div(children=[], id="ram_pref"),
        html.Div(children=[], id="cam_pref"),
        html.Div(children=[], id="cost_pref"),
        html.Div("OS", id="state", hidden=True),
    ]
)


@app.callback(
    [Output("empty-slot", "children"), Output("state", "children")],
    [Input("next", "n_clicks"), Input("prev", "n_clicks")],
    [State("state", "children")],
    prevent_initial_call=True,
)
def press_next(press_next, press_prev, current_page):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger == "next":
        next_page = next_states[current_page]
        if next_page is None:
            raise PreventUpdate
        return (state_layouts[next_page], next_page)
    elif trigger == "prev":
        prev_page = prev_states[current_page]
        if prev_page is None:
            raise PreventUpdate
        return (state_layouts[prev_page], prev_page)
    else:
        raise PreventUpdate


"""@app.callback(
    [Output("empty-slot", "children"), Output("state", "children")],
    [Input("prev", "n_clicks")],
    [State("state", "children")],
    prevent_initial_call=True,
)
def press_prev(press, current_page):
    prev_page = prev_states[current_page]
    if prev_page is None:
        raise PreventUpdate
    return (state_layouts[prev_page], prev_page)"""


app.run_server(debug=True)