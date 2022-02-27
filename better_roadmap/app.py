import os
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, Input, Output, State


from .chart import RoadmapChart
from .features import Feature, FeatureList
from .layout import layout
from .parameters import Parameters
from .scheduler import Scheduler
from .span import FeatureDateSpans, GraphSegment

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
ASSETS_FOLDER = APP_DIR / "assets"

app = Dash(
    __name__,
    title="Better Roadmap",
    assets_folder=ASSETS_FOLDER,
    external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.BOOTSTRAP],
)


def configure_app(someapp: Dash):
    fig = RoadmapChart().figure
    someapp.layout = layout(
        fig,
        FeatureList.get_default_features_text(),
        Parameters.get_default_parameters_text(),
    )


@app.callback(
    Output("roadmap-graph", "figure"),
    Input("features-update-button", "n_clicks"),
    State("features-textarea", "value"),
    Input("parameters-update-button", "n_clicks"),
    State("parameters-textarea", "value"),
)
def update_graph_callback(_a, features_text, _b, parameters_text):
    # Horrid code necessary because dash does not allow me to register 2
    # callbacks to the same Output.
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if not trigger_id:
        # app load
        return RoadmapChart(features_text, parameters_text).figure
    if trigger_id == "parameters-update-button":
        return RoadmapChart(parameters_text=parameters_text).figure
    else:
        return RoadmapChart(features_text=features_text).figure


@app.callback(
    Output("features-download", "data"),
    Input("features-download-button", "n_clicks"),
    State("features-textarea", "value"),
    prevent_initial_call=True,
)
def download_features(_, features_text: str):
    now = datetime.now()
    filename = f"features_{now:%Y%m%dT%H%M}.yml"
    return {"content": features_text, "filename": filename}


@app.callback(
    Output("parameters-download", "data"),
    Input("parameters-download-button", "n_clicks"),
    State("parameters-textarea", "value"),
    prevent_initial_call=True,
)
def download_parameters(_, parameters_text: str):
    now = datetime.now()
    filename = f"parameters_{now:%Y%m%dT%H%M}.yml"
    return {"content": parameters_text, "filename": filename}


@app.callback(
    Output("features-textarea", "value"),
    Input("features-upload", "contents"),
    prevent_initial_call=True,
)
def upload_features(content):
    if not content:
        return
    _content_type, content_string = content.split(",")
    return b64decode(content_string).decode("utf-8")


@app.callback(
    Output("parameters-textarea", "value"),
    Input("parameters-upload", "contents"),
    prevent_initial_call=True,
)
def upload_parameters(content):
    if not content:
        return
    _content_type, content_string = content.split(",")
    return b64decode(content_string).decode("utf-8")


configure_app(app)
