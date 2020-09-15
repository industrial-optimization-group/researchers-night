import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import utils.dash_reusable_components as drc
import dash_table
import plotly.express as ex
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pygmo import fast_non_dominated_sorting as nds


data = pd.read_csv("./data/car_data_v2_processed.csv", header=0)
details = pd.read_csv("./data/car_details_v2_processed.csv", header=0)

names = details.loc[0]
maxi = details.loc[1].astype(int)
details_on_card = details.loc[2].astype(int)

details_on_card = details.columns[details_on_card == 1]

sort_columns = details.columns[maxi != 0]
sort_data = data[sort_columns].values * maxi[sort_columns].values
front = data.loc[nds(sort_data)[0][0]].reset_index(drop=True)

numeric_cols = [
    attr
    for attr in data
    if data.dtypes[attr] == "int64" or data.dtypes[attr] == "float64"
]

other_cols = [attr for attr in data if data.dtypes[attr] == "object"]


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
                            # Top card with details(?)
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
                            # Attributes drowdown
                            dbc.Card(
                                children=[
                                    html.H4(
                                        "Choose attributes to be plotted",
                                        className="card-title",
                                    ),
                                    dcc.Dropdown(
                                        id="attributes-dropdown",
                                        options=[
                                            {
                                                "label": f"{attr}: {'non_numeric' if front.dtypes[attr]=='object' else 'numeric'}",
                                                "value": attr,
                                            }
                                            for attr in front.columns
                                        ],
                                        clearable=True,
                                        searchable=True,
                                        multi=True,
                                        value=numeric_cols,
                                    ),
                                    dbc.Button(
                                        id="clear-brush", children="Clear brushing"
                                    ),
                                ],
                            ),
                            # Selection of which solutions to plot
                            *[
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            f"Choose range of {attr}",
                                            className="card-title",
                                        ),
                                        dcc.RangeSlider(
                                            id=f"slider-{attr}",
                                            min=0,
                                            max=1,
                                            step=1 / (len(front[attr].unique()) * 10),
                                            marks={
                                                0: f"{1 * front[attr].min()}",
                                                0.2: f"{0.8 * front[attr].min() + 0.2 * front[attr].max()}",
                                                0.4: f"{0.6 * front[attr].min() + 0.4 * front[attr].max()}",
                                                0.6: f"{0.4 * front[attr].min() + 0.6 * front[attr].max()}",
                                                0.8: f"{0.2 * front[attr].min() + 0.8 * front[attr].max()}",
                                                1: f"{front[attr].max()}",
                                            },
                                            value=[0, 1],
                                            allowCross=False,
                                        ),
                                    ]
                                )
                                for attr in numeric_cols
                            ],
                            *[
                                dbc.Card(
                                    children=[
                                        html.H4(
                                            f"Choose types of {attr}",
                                            className="card-title",
                                        ),
                                        dcc.Checklist(
                                            id=f"checklist-{attr}",
                                            options=[
                                                {"label": val, "value": val}
                                                for val in front[attr].unique()
                                            ],
                                            value=front[attr].unique(),
                                        ),
                                    ]
                                )
                                for attr in other_cols
                            ],
                            dbc.Card(
                                children=[
                                    dcc.Graph(
                                        id="bar", config={"displayModeBar": False}
                                    )
                                ]
                            ),
                        ],
                        style={"maxHeight": "810px", "overflow": "scroll"},
                    ),
                    width={"size": 3, "offset": 1},
                    className="ml-4 mr-4",
                ),
                dbc.Col(
                    children=dcc.Graph(id="graph", style={"height": "810px"}),
                    width={"size": 7, "offset": 1},
                ),
            ]
        ),
        dbc.Row([html.Div(id="callback-dump")]),
    ],
)


@app.callback(
    Output("graph", "figure"),
    [
        Input("attributes-dropdown", "value"),
        Input("clear-brush", "n_clicks"),
        *[Input(f"slider-{attr}", "value") for attr in numeric_cols],
        *[Input(f"checklist-{attr}", "value") for attr in other_cols],
    ],
)
def create_figure(chosen_attrs, clear_brush, *userchoice):
    numeric_choices = userchoice[0 : len(numeric_cols)]
    non_numeric_choices = userchoice[len(numeric_choices) :]
    data_to_plot = front
    for ranges, attr in zip(numeric_choices, numeric_cols):
        attrmin = (1 - ranges[0]) * front[attr].min() + ranges[0] * front[attr].max()
        attrmax = (1 - ranges[1]) * front[attr].min() + ranges[1] * front[attr].max()
        data_to_plot = data_to_plot[data_to_plot[attr] >= attrmin]
        data_to_plot = data_to_plot[data_to_plot[attr] <= attrmax]
    for (classes, attr) in zip(non_numeric_choices, other_cols):
        data_to_plot = data_to_plot[data_to_plot[attr].isin(classes)]
    fig = ex.scatter_matrix(
        data_to_plot, dimensions=chosen_attrs, hover_data=details_on_card
    )
    return fig


@app.callback(
    Output("bar", "figure"), [Input("graph", "clickData")], [State("bar", "figure")]
)
def bar(selectedData, fig):
    if selectedData is None:
        raise PreventUpdate
    point_id = selectedData["points"][0]["pointIndex"]
    point = front.loc[point_id]
    y_new = point.values

    if fig is not None:
        if len(fig["data"]) == 1:
            y = np.asarray(fig["data"][0]["y"])
        else:
            y = np.asarray(fig["data"][0]["y"]) + np.asarray(fig["data"][1]["y"])
    else:
        y = np.zeros_like(y_new)

    y_delta = y_new - y
    color = np.sign(y_delta)
    color = ["green" if x > 0 else "red" for x in color]
    fig = go.Figure(
        data=[
            go.Bar(x=data.columns, y=y, name="Old choice"),
            go.Bar(
                x=data.columns, y=y_delta, marker_color=color, name="Delta from old"
            ),
        ]
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), barmode="stack")
    fig.update_yaxes(range=[0, front.max().max()])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
