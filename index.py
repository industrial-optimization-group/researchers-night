import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import UI_phone_csv, UI_phone_traditional, UI_phone_mcdm

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/phone_example/csv":
        return UI_phone_csv.layout
    elif pathname == "/phone_example/traditional":
        return UI_phone_traditional.layout
    elif pathname == "/phone_example/mcdm":
        return UI_phone_mcdm.layout
    else:
        return "404"

if __name__ == "__main__":
    app.run_server(debug=True)
