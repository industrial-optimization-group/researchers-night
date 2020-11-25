import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.express as ex
import pandas as pd

data = pd.read_csv("./data/data.csv", header=0)
data.drop(columns="id", inplace=True)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id="attributes-dropdown",
            options=[{"label": attr, "value": attr} for attr in data.columns],
            multi=True,
        ),
        dcc.Graph(id="graph-sklearn-svm", style={"height": "720px"}),
    ]
)


@app.callback(
    Output("graph-sklearn-svm", "figure"), [Input("attributes-dropdown", "value")],
)
def create_figure(chosen_attrs):
    if chosen_attrs is None:
        raise PreventUpdate()
    return ex.scatter_matrix(data, dimensions=chosen_attrs, color=data.columns[0])


app.run_server()
