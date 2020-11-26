import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc

from app import app

data = pd.read_csv("./data/Phone_dataset_new.csv", header=0)
details = pd.read_csv("./data/Phone_details.csv", header=0)

names = details.loc[0]

data = data.rename(columns=names)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

'''
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LITERA],
    eager_loading=True,
    suppress_callback_exceptions=True,
)
'''

layout = html.Div(
    dbc.Col(
        dash_table.DataTable(
            id="datatable-interactivity",
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True}
                for i in data.columns
            ],
            data=data.to_dict("records"),
            filter_action="native",
            sort_action="native",
        ),
        width={"size": 10, "offset": 1},
        className="mt-4",
    )
)

if __name__ == "__main__":
    app.run_server(debug=False)
