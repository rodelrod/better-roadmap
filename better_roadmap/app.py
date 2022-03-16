import os
from base64 import b64decode
from datetime import datetime
from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, ClientsideFunction
from pydantic import ValidationError
from yaml.parser import ParserError

from better_roadmap.models.config_type import ConfigType
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
        ElapsedFeatureList.get_default_text(),
        FeatureList.get_default_text(),
        Parameters.get_default_text(),
    )


@app.callback(
    Output("roadmap-graph", "figure"),
    State("elapsed-textarea", "value"),
    State("features-textarea", "value"),
    State("parameters-textarea", "value"),
    Input("select-chart-height", "value"),
    Input("elapsed-textarea", "n_blur"),
    Input("features-textarea", "n_blur"),
    Input("parameters-textarea", "n_blur"),
    Input("update-chart-button", "n_clicks"),
)
def update_graph(
    elapsed_text,
    features_text,
    parameters_text,
    chart_height,
    _elapsed_blur,
    _features_blur,
    _parameters_blur,
    _update_clicks,
):
    fig = RoadmapChart(elapsed_text, features_text, parameters_text).figure
    fig.update_layout(height=int(chart_height))
    return fig


app.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="feature_search",
    ),
    Output("search-dummy-output", "children"),
    Input("search-features-input", "value"),
    prevent_initial_call=True,
)


def register_download_action(config_type):
    @app.callback(
        Output(f"{config_type}-download", "data"),
        Input(f"{config_type}-download-button", "n_clicks"),
        State(f"{config_type}-textarea", "value"),
        prevent_initial_call=True,
    )
    def download_config(_, config_text: str):
        now = datetime.now()
        filename = f"{config_type}_{now:%Y%m%dT%H%M}.yml"
        return {"content": config_text, "filename": filename}


def register_upload_action(config_type):
    @app.callback(
        Output(f"{config_type}-textarea", "value"),
        Input(f"{config_type}-upload", "contents"),
        prevent_initial_call=True,
    )
    def upload_config(content):
        if not content:
            return
        _content_type, content_string = content.split(",")
        return b64decode(content_string).decode("utf-8")


def register_config_validator(config_type: str, config_model: ConfigType):
    @app.callback(
        Output(f"{config_type}-textarea", "valid"),
        Output(f"{config_type}-textarea", "invalid"),
        Output(f"{config_type}-validation-alert", "is_open"),
        Output(f"{config_type}-validation-alert-text", "children"),
        State(f"{config_type}-textarea", "value"),
        Input(f"{config_type}-textarea", "n_blur"),
    )
    def validate_config(config_text: str, _):
        try:
            config_model.from_text(config_text)
        except ParserError:
            return False, True, True, "Yaml parsing error"
        except ValidationError as e:
            return False, True, True, str(e)
        return True, False, False, ""


CONFIG_MODELS = {
    "elapsed": ElapsedFeatureList,
    "features": FeatureList,
    "parameters": Parameters,
}

for config_type in ["elapsed", "features", "parameters"]:
    register_download_action(config_type)
    register_upload_action(config_type)
    register_config_validator(config_type, CONFIG_MODELS[config_type])

configure_app(app)
