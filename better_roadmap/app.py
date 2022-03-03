import os
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State
from pydantic import ValidationError

from better_roadmap.models.elapsed import ElapsedFeatureList
from better_roadmap.models.features import FeatureList
from better_roadmap.models.parameters import Parameters
from better_roadmap.services.roadmap_chart import RoadmapChart

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
        ElapsedFeatureList.get_default_elapsed_text(),
        FeatureList.get_default_features_text(),
        Parameters.get_default_parameters_text(),
    )


@app.callback(
    Output("roadmap-graph", "figure"),
    State("elapsed-textarea", "value"),
    State("features-textarea", "value"),
    State("parameters-textarea", "value"),
    Input("elapsed-update-button", "n_clicks"),
    Input("features-update-button", "n_clicks"),
    Input("parameters-update-button", "n_clicks"),
    Input("select-chart-height", "value"),
)
def update_graph(
    elapsed_text,
    features_text,
    parameters_text,
    _elapsed_clicks,
    _features_clicks,
    _parameters_clicks,
    chart_height,
):
    fig = RoadmapChart(elapsed_text, features_text, parameters_text).figure
    fig.update_layout(height=int(chart_height))
    return fig


@app.callback(
    Output("elapsed-download", "data"),
    Input("elapsed-download-button", "n_clicks"),
    State("elapsed-textarea", "value"),
    prevent_initial_call=True,
)
def download_elapsed(_, elapsed_text: str):
    now = datetime.now()
    filename = f"elapsed_{now:%Y%m%dT%H%M}.yml"
    return {"content": elapsed_text, "filename": filename}


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
    Output("elapsed-textarea", "value"),
    Input("elapsed-upload", "contents"),
    prevent_initial_call=True,
)
def upload_elapsed(content):
    if not content:
        return
    _content_type, content_string = content.split(",")
    return b64decode(content_string).decode("utf-8")


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


@app.callback(
    Output("elapsed-textarea", "valid"),
    Output("elapsed-textarea", "invalid"),
    State("elapsed-textarea", "value"),
    Input("elapsed-textarea", "n_blur"),
)
def validate_elapsed_text(elapsed_text, _):
    try:
        ElapsedFeatureList.from_text(elapsed_text)
    except ValidationError as e:
        print(e)
        return False, True
    return True, False


@app.callback(
    Output("features-textarea", "valid"),
    Output("features-textarea", "invalid"),
    State("features-textarea", "value"),
    Input("features-textarea", "n_blur"),
)
def validate_features_text(features_text, _):
    try:
        FeatureList.from_text(features_text)
    except ValidationError as e:
        print(e)
        return False, True
    return True, False


@app.callback(
    Output("parameters-textarea", "valid"),
    Output("parameters-textarea", "invalid"),
    State("parameters-textarea", "value"),
    Input("parameters-textarea", "n_blur"),
)
def validate_parameters_text(parameters_text, _):
    try:
        Parameters.from_text(parameters_text)
    except ValidationError as e:
        print(e)
        return False, True
    return True, False


configure_app(app)
