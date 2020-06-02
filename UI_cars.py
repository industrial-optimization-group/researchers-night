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


data = pd.read_csv("./data/car_data_processed.csv", header=0)

maxi = data.loc[0]
data = data.loc[1:]

front = data.loc[nds(data.values * maxi.values)[0][2]].reset_index(drop=True)
print(len(front))

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
                                        "Choose attributes to be plotted",
                                        className="card-title",
                                    ),
                                    dcc.Dropdown(
                                        id="attributes-dropdown",
                                        options=[
                                            {"label": attr, "value": attr}
                                            for attr in front.columns
                                        ],
                                        clearable=True,
                                        searchable=True,
                                        multi=True,
                                        value=front.columns,
                                    ),
                                    dbc.Button(
                                        id="clear-brush", children="Clear brushing"
                                    ),
                                ],
                            ),
                            dbc.Card(
                                children=[
                                    dcc.Graph(
                                        id="bar", config={"displayModeBar": False}
                                    )
                                ]
                            ),
                        ],
                    ),
                    width=2,
                ),
                dbc.Col(
                    children=dcc.Graph(id="graph", style={"height": "720px"}), width=9,
                ),
            ]
        ),
        dbc.Row([html.Div(id="callback-dump")]),
    ],
)


@app.callback(
    Output("graph", "figure"),
    [Input("attributes-dropdown", "value"), Input("clear-brush", "n_clicks")],
)
def create_figure(chosen_attrs, _):
    fig = ex.scatter_matrix(front, dimensions=chosen_attrs)
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
