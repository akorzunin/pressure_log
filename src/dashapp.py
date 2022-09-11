import json
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import plotly.express as px

# import flask
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objects as go

from src.db_conn import users
from src import crud
from src.fig_handler import render_fig


def create_dash_app(
    html_layout: int,
    prefix: str = None,
) -> dash.Dash:

    user_id: int = 1
    data = crud.get_user(users, user_id)

    fig = render_fig(data)

    app = dash.Dash(
        __name__,
        server=True,
        requests_pathname_prefix=prefix,
    )

    app.index_string = html_layout

    app.scripts.config.serve_locally = False
    dcc._js_dist[0][
        "external_url"
    ] = "https://cdn.plot.ly/plotly-basic-latest.min.js"

    app.layout = html.Div(
        [
            html.H1("Pressure Data"),
            dcc.Graph(id="pressure-graph", figure=fig),
        ],
        className="container",
    )

    @app.callback(
        Output("pressure-graph", "figure"),
        [Input("form", "value")],
    )
    def update_graph(form):
        ...
        # return get_fig(form, "Stats")

    return app
