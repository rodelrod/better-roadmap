from base64 import b64decode
from datetime import datetime
import os
from pathlib import Path

import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import yaml

from .scheduler import Scheduler
from .feature import Feature
from .parameters import Parameters, Phase, SprintDuration
from .span import FeatureDateSpans, GraphSegment

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
FEATURES_FILE = APP_DIR / "data" / "features.yml"
PARAMETERS_FILE = APP_DIR / "data" / "parameters.yml"
ASSETS_FOLDER = APP_DIR / "assets"

app = Dash(
    __name__,
    title="Better Roadmap",
    assets_folder=ASSETS_FOLDER,
    external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.BOOTSTRAP],
)


def configure_app(someapp: Dash):
    fig = update_graph()
    someapp.layout = layout(fig)


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
        return update_graph(features_text, parameters_text)
    if trigger_id == "parameters-update-button":
        return update_graph(parameters_text=parameters_text)
    else:
        return update_graph(features_text=features_text)


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


def update_graph(features_text=None, parameters_text=None):
    graph_segments = []
    parameters = parse_parameters(parameters_text)
    scheduler = Scheduler(parameters.phases)
    for feature in parse_features(features_text):
        graph_segments.extend(
            schedule_feature(feature, parameters.project_start, scheduler)
        )
    df = pd.DataFrame(graph_segments)
    fig = chart(df)
    return fig


def chart(df: pd.DataFrame):
    fig = px.timeline(df, x_start="start", x_end="end", y="feature", color="phase")
    fig.update_yaxes(autorange="reversed")
    return fig


def layout(fig):
    tab_chart = dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="roadmap-graph", figure=fig),
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="📅 Roadmap",
    )
    tab_features = dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        children=[
                            dbc.Col(
                                dbc.Textarea(
                                    id="features-textarea",
                                    value=get_default_features_as_text(),
                                    rows=30,
                                    persistence=True,
                                    persistence_type="local",
                                ),
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Update",
                                                            html.I(
                                                                className="bi bi-bar-chart-steps ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="features-update-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                                dcc.Download(id="features-download"),
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Download",
                                                            html.I(
                                                                className="bi bi-download ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="features-download-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                            ]
                                        ),
                                    ),
                                    dbc.Row(
                                        className="mt-3",
                                        children=dbc.Col(
                                            dbc.Button(
                                                outline=True,
                                                color="primary",
                                                className="text-center d-grid gap-2 col-8 mx-auto",
                                                children=dcc.Upload(
                                                    id="features-upload",
                                                    children=[
                                                        html.I(
                                                            className="bi bi-cloud-upload me-2",
                                                            style={
                                                                "fontSize": "xx-large"
                                                            },
                                                        ),
                                                        html.Br(),
                                                        "drag & drop or select file",
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="🏆 Features",
    )
    tab_parameters = dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Textarea(
                                    id="parameters-textarea",
                                    value=get_default_parameters_as_text(),
                                    rows=20,
                                    persistence=True,
                                    persistence_type="local",
                                ),
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Update",
                                                            html.I(
                                                                className="bi bi-bar-chart-steps ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="parameters-update-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                                dcc.Download(id="parameters-download"),
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Download",
                                                            html.I(
                                                                className="bi bi-download ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="parameters-download-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                            ]
                                        ),
                                    ),
                                    dbc.Row(
                                        className="mt-3",
                                        children=dbc.Col(
                                            dbc.Button(
                                                outline=True,
                                                color="primary",
                                                className="text-center d-grid gap-2 col-8 mx-auto",
                                                children=dcc.Upload(
                                                    id="parameters-upload",
                                                    children=[
                                                        html.I(
                                                            className="bi bi-cloud-upload me-2",
                                                            style={
                                                                "fontSize": "xx-large"
                                                            },
                                                        ),
                                                        html.Br(),
                                                        "drag & drop or select file",
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="⚙ ️Parameters",
    )
    layout = (
        html.Div(
            [
                html.H1(children="Better Roadmap", className="display-3"),
                html.P(
                    """
                        Estimate your "agile sprints" until the end of days to please the PHBs.
                    """,
                    className="lead",
                ),
                dbc.Tabs([tab_chart, tab_features, tab_parameters]),
            ]
        ),
    )
    return dbc.Container(layout, fluid=True)


def parse_features(features_text) -> list[Feature]:
    if features_text:
        feature_dicts = yaml.safe_load(features_text)
    else:
        with FEATURES_FILE.open() as features_file:
            feature_dicts = yaml.safe_load(features_file)
    features = [Feature.from_dict(d) for d in feature_dicts]
    return features


def get_default_features_as_text() -> str:
    with FEATURES_FILE.open() as features_file:
        default_features = features_file.read()
    return default_features


def parse_parameters(parameters_text) -> Parameters:
    if parameters_text:
        parameters_dict = yaml.safe_load(parameters_text)
    else:
        with PARAMETERS_FILE.open() as parameters_file:
            parameters_dict = yaml.safe_load(parameters_file)
    parameters = Parameters.from_dict(
        {
            "project_start": parameters_dict["project_start"],
            "default_sprint_duration": parameters_dict["default_sprint_duration"],
            "phases": [Phase.from_dict(p) for p in parameters_dict["phases"]],
            "sprint_durations": [
                SprintDuration.from_dict(s) for s in parameters_dict["sprints"]
            ],
        }
    )
    return parameters


def get_default_parameters_as_text() -> str:
    with PARAMETERS_FILE.open() as parameters_file:
        default_parameters = parameters_file.read()
    return default_parameters


def schedule_feature(
    feature: Feature, project_start: datetime, scheduler: Scheduler = None
) -> list[GraphSegment]:
    if not scheduler:
        scheduler = Scheduler()
    feature_sprint_spans = scheduler.schedule_feature(feature)
    feature_data_spans = FeatureDateSpans.from_feature_sprint_spans(
        feature_sprint_spans, project_start=project_start
    )
    return feature_data_spans.get_graph_segments()


configure_app(app)
