import os
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State

from better_roadmap.models.actuals import ActualFeatureList
from better_roadmap.models.charts import RoadmapChart
from better_roadmap.models.features import FeatureList
from better_roadmap.models.parameters import Parameters

from .layout import layout

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
        ActualFeatureList.get_default_actuals_text(),
        Parameters.get_default_parameters_text(),
    )


@app.callback(
    Output("roadmap-graph", "figure"),
    State("actuals-textarea", "value"),
    State("features-textarea", "value"),
    State("parameters-textarea", "value"),
    Input("actuals-update-button", "n_clicks"),
    Input("features-update-button", "n_clicks"),
    Input("parameters-update-button", "n_clicks"),
)
def update_graph(
    actuals_text,
    features_text,
    parameters_text,
    _actuals_clicks,
    _features_clicks,
    _parameters_clicks,
):
    return RoadmapChart(actuals_text, features_text, parameters_text).figure


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
